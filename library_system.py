# Author: Llobrera, John Aaron B.
    # Affiliation: BS Statistics, Institute of Statistics, University of the Philippines Los Baños
    # E-Mail: jbllobrera@up.edu.ph
# Description:
"""
    This Library Inventory and Logging System serves as a comprehensive solution for managing library 
    operations efficiently, including:
        - Adding, deleting, editing, and viewing books in the library inventory.
        - Facilitating book borrowing and returns, ensuring smooth circulation of library resources.
        - Offering features like log viewing, visit recording, and transaction tracking to provide insights into library activities and operations.
        - Prioritizing data security through encryption, safeguarding sensitive information stored within the system.
    For inquiries or further information, you may contact the author at jbllobrera@up.edu.ph.
"""

# Usage of cryptography fucntionality
from cryptography.fernet import Fernet #Main function for encryption and decryption
import datetime #Function within the cryptography library to help validate time and date

# Generates a key for encryption
def generate_key():
    return Fernet.generate_key()

# Loads the encryption key from a file
def load_key(key_file):
    with open(key_file, "rb") as file:
        return file.read()

# Saves the encryption key to a file
def save_key(key, key_file):
    with open(key_file, "wb") as file:
        file.write(key)

# Encrypts data using the encryption key
def encrypt(data, key):
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())

# Decrypts data using the encryption key
def decrypt(encrypted_data, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data).decode()

# Encrypts data and save it to a file
def encrypt_and_save(data, key, key_file):
    encrypted_data = encrypt(data, key)
    with open(key_file, "wb") as file:
        file.write(encrypted_data)

# Loads encrypted data from a file and decrypts it
def load_and_decrypt(key_file, key):
    with open(key_file, "rb") as file:
        encrypted_data = file.read()
    return decrypt(encrypted_data, key)

# Constants for file paths
ENCRYPTED_BOOKS_FILE = 'books.txt'
ENCRYPTED_BORROW_LIST_FILE = 'borrow_list.txt'
ENCRYPTED_LOGBOOK_FILE = 'logbook.txt'

# Generates or loads encryption key
key_file = "encryption_key.key"
try:
    key = load_key(key_file)
except FileNotFoundError:
    key = generate_key()
    save_key(key, key_file)

# Modify the function to encrypt data before saving
def save_data(data, key_file):
    """
    Encrypts and saves data from the dictionary to the specified file.

    Args:
        data (dict): The data to be saved.
        key_file (str): The path to the file where encrypted data is to be saved.
    """
    try:
        # Convert data to string before encrypting (if necessary)
        data_str = str(data)
        encrypt_and_save(data_str, key, key_file)
    except Exception as e:
        print("Error encrypting and saving data:", e)

# Modify the functions to encrypt and decrypt data before saving and loading
def load_data(key_file):
    """
    Loads and decrypts data from the specified file into a dictionary.
    If the file is not found or decryption fails, an empty dictionary is returned.

    Args:
        key_file (str): The path to the file from which data is to be loaded.

    Returns:
        dict: A dictionary containing the decrypted data loaded from the file or an empty dictionary if file is not found or decryption fails.
    """
    try:
        decrypted_data = load_and_decrypt(key_file, key)
        return eval(decrypted_data)  # Use eval to convert string representation of dictionary back to dictionary
    except Exception as e:
        print("--------CREATING FILE--------")
        return {}

# Initializes dictionaries
books = load_data(ENCRYPTED_BOOKS_FILE) or {}
borrow_list = load_data(ENCRYPTED_BORROW_LIST_FILE) or {}
logbook = load_data(ENCRYPTED_LOGBOOK_FILE) or {}

# Creates files if not present yet
if not books:
    save_data({}, ENCRYPTED_BOOKS_FILE)
if not borrow_list:
    save_data({}, ENCRYPTED_BORROW_LIST_FILE)
if not logbook:
    save_data({}, ENCRYPTED_LOGBOOK_FILE)
if not logbook:
    save_data({}, ENCRYPTED_LOGBOOK_FILE)
    
# Functions to validate date and time format

def validate_date(date_str):
    """
    Validates if the input date string is in the correct format.
    
    Args:
        date_str (str): The input date string.
        
    Returns:
        bool: True if the date string is in the correct format, False otherwise.
    """
    try:
        datetime.datetime.strptime(date_str, '%d %b %Y')
        return True
    except ValueError:
        return False

def validate_time(time_str):
    """
    Validates if the input time string is in the correct format.
    
    Args:
        time_str (str): The input time string.
        
    Returns:
        bool: True if the time string is in the correct format, False otherwise.
    """
    try:
        datetime.datetime.strptime(time_str, '%I:%M %p')
        return True
    except ValueError:
        return False


# Book Management Module

def add_book():
    """
    Adds a new book to the library inventory.
    Prompts the user for book details and saves them to the books dictionary.
    """
    title = input("Enter title: ")
    author = input("Enter author: ")
    date_published = input("Enter date published (e.g. 9 Jan 2020): ")
    while not validate_date(date_published):
        print("Invalid date format. Please enter the date in the format 'Day Month Year' (e.g., 9 Jan 2020).")
        date_published = input("Enter date published: ")
        
    book_id = f'B{len(books) + 1}'
    books[book_id] = {
        'Title': title,
        'Author': author,
        'Date Published': date_published,
        'Status': 'Available',
        'List of Borrowers': []
    }
    save_data(books, ENCRYPTED_BOOKS_FILE)
    print(f"Book {book_id} added successfully.")

def delete_book():
    """
    Deletes a book from the library inventory based on title and author.
    Prompts the user for book details and removes it from the books dictionary if found.
    Also deletes any corresponding borrow entries.
    """
    title = input("Enter title of the book to delete: ").strip()  # Remove leading and trailing whitespace
    author = input("Enter author of the book to delete: ").strip()  # Remove leading and trailing whitespace
    book_id = None
    for id, book in books.items():
        # Strip leading and trailing whitespace for comparison
        if book['Title'].strip() == title and book['Author'].strip() == author:
            book_id = id
            break
    if book_id:
        del books[book_id]
        
        # Remove the book from borrow_list as well
        borrow_ids_to_delete = [borrow_id for borrow_id, entry in borrow_list.items() if entry['Book_ID'] == book_id]
        for borrow_id in borrow_ids_to_delete:
            del borrow_list[borrow_id]
        
        save_data(books, ENCRYPTED_BOOKS_FILE)
        save_data(borrow_list, ENCRYPTED_BORROW_LIST_FILE)  # Save updated borrow list

        print(f"Book '{title}' by {author} was deleted successfully.")
    else:
        print("Book not found.")

def delete_all_books():
    """
    Deletes all books from the library inventory.
    Prompts the user for confirmation before clearing the books dictionary.
    Also clears all borrow entries.
    """
    confirm = input("Are you sure you want to delete all books? (yes/no): ")
    if confirm.lower() == 'yes':
        books.clear()
        borrow_list.clear()  # Clear the borrow list as well
        save_data(books, ENCRYPTED_BOOKS_FILE)
        save_data(borrow_list, ENCRYPTED_BORROW_LIST_FILE)  # Save updated (cleared) borrow list
        print("All books were deleted successfully.")
    else:
        print("Operation canceled.")


def view_book():
    """
    Views the details of a book based on the title.
    Prompts the user for the book title and displays its details if found.
    """
    title = input("Enter title of the book to view: ")
    for book in books.values():
        if book['Title'] == title:
            print("-----------------------------------")
            print(f"Title: {book['Title']}")
            print(f"Author: {book['Author']}")
            print(f"Date Published: {book['Date Published']}")
            print(f"Status: {book['Status']}")
            print("List of Borrowers:")
            for borrower_id in book['List of Borrowers']:
                print("-",logbook[borrower_id]['Person Name'])
            print("-----------------------------------")
            return
    print("Book not found.")

def edit_book():
    """
    Edits the details of a book in the library inventory.
    Prompts the user for the book title and new details, and updates the book information.
    """
    title = input("Enter title of the book to edit: ")
    for book_id, book in books.items():
        if book['Title'] == title:
            new_title = input("Enter new title: ")
            new_author = input("Enter new author: ")
            new_date_published = input("Enter new date published (e.g. 9 Jan 2020): ")
            while not validate_date(new_date_published):
                print("Invalid date format. Please enter the date in the format 'Day Month Year' (e.g., 9 Jan 2020).")
                new_date_published = input("Enter new date published: ")
                
            books[book_id] = {
                'Title': new_title,
                'Author': new_author,
                'Date Published': new_date_published,
                'Status': book['Status'],
                'List of Borrowers': book['List of Borrowers']
            }
            save_data(books, ENCRYPTED_BOOKS_FILE)
            print("Book updated successfully.")
            return
    print("Book not found.")

def view_pending():
    """
    Views all books that are currently unavailable (borrowed).
    Displays the book details along with the last borrower's name and expected return date.
    """
    found_pending_books = False  # Flag to track if any pending books are found
    for book_id, book in books.items():
        if book['Status'] == 'Unavailable':
            found_pending_books = True  # Set flag to True if at least one unavailable book is found
            print("-----------------------------------")
            print(f"Title: {book['Title']}")
            print(f"Author: {book['Author']}")
            print(f"Date Published: {book['Date Published']}")
            print(f"Status: {book['Status']}")
            if book['List of Borrowers']:
                last_borrower_id = book['List of Borrowers'][-1]  # Get the ID of the last borrower's log entry
                borrow_key = None
                for bl_id, bl_entry in borrow_list.items():
                    if bl_entry['Log_ID'] == last_borrower_id:
                        borrow_key = bl_id
                        break

                if borrow_key:
                    borrow_info = borrow_list[borrow_key]
                    expected_return_date = borrow_info.get('Date Return')
                    if expected_return_date is not None:
                        print(f"Expected Date of Return: {expected_return_date}")
                        last_borrower_name = logbook[last_borrower_id]['Person Name']
                        print(f"Last Borrower: {last_borrower_name}")
                        print("-----------------------------------")
                    else:
                        print("Error: 'Date Return' not found in borrow list entry.")
                else:
                    print("Error: Borrower information not found in borrow list.")
            else:
                print("No borrower information available.")
    
    if not found_pending_books:
        print("No pending books.")

def view_all_books(): # Extra Functionality written by Aa for Fun
    """
    Views all stored books along with their details.
    """
    if books:
        for book_id, book_info in books.items():
            print("-----------------------------------")
            print(f"Book ID: {book_id}")
            print(f"Title: {book_info['Title']}")
            print(f"Author: {book_info['Author']}")
            print(f"Date Published: {book_info['Date Published']}")
            print(f"Status: {book_info['Status']}")
            print("-----------------------------------")
    else:
        print("No books stored.")

# Borrow and Return Books Module

def borrow_book():
    """
    Allows user to borrow a book from the repository. Makes the status unavailable.
    """
    person_name = input("Enter your name: ")
    date = input("Enter today's date (e.g. 9 Jan 2020): ")
    while not validate_date(date):
        print("Invalid date format. Please enter the date in the format 'Day Month Year' (e.g., 9 Jan 2020).")
        date = input("Enter today's date: ")
    time = input("Enter current time (e.g. 10:30 AM): ")
    while not validate_time(time):
        print("Invalid time format. Please enter the time in the format 'hour:minutes AM/PM' (e.g., 9:30 AM).")
        time = input("Enter current time: ")
    
    purpose = "borrow"
    log_id = f'L{len(logbook) + 1}'
    logbook[log_id] = {
        'Person Name': person_name,
        'Date': date,
        'Time': time,
        'Purpose': purpose
    }
    
    title = input("Enter title of the book to borrow: ")
    author = input("Enter author of the book to borrow: ")
    for book_id, book in books.items():
        if book['Title'] == title and book['Author'] == author and book['Status'] == 'Available':
            date_return = input("Enter date of return (e.g. 9 Jan 2020): ")
            while not validate_date(date_return):
                print("Invalid date format. Please enter the date in the format 'Day Month Year' (e.g., 9 Jan 2020).")
                date_return = input("Enter date of return: ")
            
            borrow_id = f'BL{len(borrow_list) + 1}'
            borrow_list[borrow_id] = {  # Ensure the key is stored as a string
                'Book_ID': book_id,
                'Log_ID': log_id,
                'Date Return': date_return
            }
            # Update book status and list of borrowers
            book['Status'] = 'Unavailable'
            book['List of Borrowers'].append(log_id)
            # Save updated data to files
            save_data(books, ENCRYPTED_BOOKS_FILE)
            save_data(borrow_list, ENCRYPTED_BORROW_LIST_FILE)
            save_data(logbook, ENCRYPTED_LOGBOOK_FILE)
            print(f"Book {book_id} borrowed successfully.")
            return
    print("Book not available or not found.")

def return_book():
    """
    Allows user to return the book they borrowed, making the status available again.
    """
    person_name = input("Enter your name: ")
    date = input("Enter today's date (e.g. 9 Jan 2020): ")
    while not validate_date(date):
        print("Invalid date format. Please enter the date in the format 'Day Month Year' (e.g., 9 Jan 2020).")
        date = input("Enter today's date: ")
    time = input("Enter current time (e.g. 10:30 AM): ")
    while not validate_time(time):
        print("Invalid time format. Please enter the time in the format 'hour:minutes AM/PM' (e.g., 9:30 AM).")
        time = input("Enter current time: ")
    purpose = "return"
    log_id = f'L{len(logbook) + 1}'
    logbook[log_id] = {
        'Person Name': person_name,
        'Date': date,
        'Time': time,
        'Purpose': purpose
    }
    
    title = input("Enter title of the book to return: ")
    author = input("Enter author of the book to return: ")
    for book_id, book in books.items():
        if book['Title'] == title and book['Author'] == author and book['Status'] == 'Unavailable':
            book['Status'] = 'Available'
            save_data(books, ENCRYPTED_BOOKS_FILE)
            save_data(logbook, ENCRYPTED_LOGBOOK_FILE)
            print(f"Book {book_id} returned successfully.")
            return
    print("Book not found or already available.")

def view_all_entries():
    """
    Views all borrow entries in the borrow list.
    Displays details of each borrowed book along with the borrower's name and return date.
    """
    if not borrow_list:
        print("No borrow entries found.")
        return
    
    for borrow_id, entry in borrow_list.items():
        book_id = entry['Book_ID']
        log_id = entry['Log_ID']
        book = books[book_id]
        log_entry = logbook[log_id]
        print("-----------------------------------")
        print(f"Borrow_ID: {borrow_id}")
        print(f"Title: {book['Title']}")
        print(f"Author: {book['Author']}")
        print(f"Date Published: {book['Date Published']}")
        print(f"Date Return: {entry['Date Return']}")
        print(f"Borrower: {log_entry['Person Name']}")
        print("-----------------------------------")

def view_expected_returns():
    """
    Views all books expected to be returned on a specified date.
    Prompts the user for the date and displays details of each book expected to be returned.
    """
    date = input("Enter Date (e.g. 9 Jan 2020): ")
    while not validate_date(date):
        print("Invalid date format. Please enter the date in the format 'Day Month Year' (e.g., 9 Jan 2020).")
        date = input("Enter Date (e.g. 9 Jan 2020): ")
    if not borrow_list:
        print("No expected returns.")
        return
    for borrow_id, entry in borrow_list.items():
        if entry['Date Return'] == date:
            book_id = entry['Book_ID']
            log_id = entry['Log_ID']
            book = books[book_id]
            log_entry = logbook[log_id]
            print("-----------------------------------")
            print(f"Borrow_ID: {borrow_id}")
            print(f"Title: {book['Title']}")
            print(f"Author: {book['Author']}")
            print(f"Date Published: {book['Date Published']}")
            print(f"Status: {book['Status']}")
            print(f"Borrower: {log_entry['Person Name']}")
            print("-----------------------------------")

# Logbook Module

def visit_library():
    """
    Records a visit to the library.
    Prompts the user for their details and logs the visit in the logbook.
    """
    person_name = input("Enter your name: ")
    date = input("Enter today's date (e.g. 9 Jan 2020): ")
    while not validate_date(date):
        print("Invalid date format. Please enter the date in the format 'Day Month Year' (e.g., 9 Jan 2020).")
        date = input("Enter today's date: ")
    time = input("Enter current time (e.g. 10:30 AM): ")
    while not validate_time(time):
        print("Invalid time format. Please enter the time in the format 'hour:minutes AM/PM' (e.g., 9:30 AM).")
        time = input("Enter current time: ")
        
    purpose = "visit"
    log_id = f'L{len(logbook) + 1}'
    logbook[log_id] = {
        'Person Name': person_name,
        'Date': date,
        'Time': time,
        'Purpose': purpose
    }
    save_data(logbook, ENCRYPTED_LOGBOOK_FILE)
    print(f"Visit logged with Log_ID: {log_id}")

def view_all_log_entries():
    """
    Views all entries in the logbook.
    Displays details of each entry including person name, date, time, and purpose.
    """
    for log_id, entry in logbook.items():
        print("-----------------------------------")
        print(f"Log_ID: {log_id}")
        print(f"Person Name: {entry['Person Name']}")
        print(f"Date: {entry['Date']}")
        print(f"Time: {entry['Time']}")
        print(f"Purpose: {entry['Purpose']}")
        print("-----------------------------------")

def view_transactions_per_day():
    """
    Views all transactions for a specified date.
    Prompts the user for the date and displays details of each transaction.
    """
    date = input("Enter Date (e.g. 9 Jan 2020): ")
    while not validate_date(date):
        print("Invalid date format. Please enter the date in the format 'Day Month Year' (e.g., 9 Jan 2020).")
        date = input("Enter Date (e.g. 9 Jan 2020): ")
    for log_id, entry in logbook.items():
        if entry['Date'] == date:
            print("-----------------------------------")
            print(f"Log_ID: {log_id}")
            print(f"Person Name: {entry['Person Name']}")
            print(f"Date: {entry['Date']}")
            print(f"Time: {entry['Time']}")
            print(f"Purpose: {entry['Purpose']}")
            print("-----------------------------------")

# Main Menu

def main():
    while True:
        print("\n" + "=" * 35)
        print("|  Library Inventory and Logging  |")
        print("|  System by Llobrera (May 2024)  |")
        print("=" * 35)
        print("| MANAGE BOOKS                    |")
        print("|    1. Add Book                  |")
        print("|    2. Delete Book               |")
        print("|    3. Delete All Books          |")
        print("|    4. Edit Book                 |")
        print("|    5. View a Book               |")
        print("|    6. View Unavailable Books    |")
        print("|    7. View All Stored Books     |")
        print("| BORROW OR RETURN BOOKS          |")
        print("|    8. Borrow Book               |")
        print("|    9. Return Book               |")
        print("|    10. View All Borrow Entries  |")
        print("|    11. View Expected Returns    |")
        print("| VISITATION & ENTRY LOGS         |")
        print("|    12. Visit Library            |")
        print("|    13. View All Entries         |")
        print("|    14. View Transactions/Day    |")
        print("| EXIT                            |")
        print("|    15. Exit                     |")
        print("=" * 35)

        choice = input("Enter your choice: ")
        if choice == '1':
            add_book()
        elif choice == '2':
            delete_book()
        elif choice == '3':
            delete_all_books()
        elif choice == '4':
            edit_book()
        elif choice == '5':
            view_book()
        elif choice == '6':
            view_pending()
        elif choice == '7':
            view_all_books()
        elif choice == '8':
            borrow_book()
        elif choice == '9':
            return_book()
        elif choice == '10':
            view_all_entries()
        elif choice == '11':
            view_expected_returns()
        elif choice == '12':
            visit_library()
        elif choice == '13':
            view_all_log_entries()
        elif choice == '14':
            view_transactions_per_day()
        elif choice == '15':
            print("Thank you for availing this service!")
            break
        else:
            print("No such option.")
	    
if __name__ == "__main__":
    """
    This block of code will only execute if this script is run directly by the Python interpreter. 
    It will not execute if this script is imported as a module into another Python script.
    """
    main()

################################################################### 

"""
PINAGPUYATAN NI JOHN AARON LLOBRERA (2024). ALL RIGHTS RESERVED.
You may reach out to Aa  via jbllobrera@up.edu.ph.
"""

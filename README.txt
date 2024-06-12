Library Inventory and Logging System

Overview
This Library Inventory and Logging System is a Python-based application. It provides a comprehensive solution for managing library operations efficiently, including book management, borrowing and returning books, logging visits, and tracking transactions. The system prioritizes data security through encryption, ensuring sensitive information stored within the system is protected.

Features
- Book Management:
  - Add, delete, edit, and view books in the library inventory.
  - Each book includes details such as title, author, date published, and status.
  
- Borrow and Return Books:
  - Borrow books from the library, marking them as unavailable.
  - Return borrowed books, marking them as available again.
  - Track borrowers and expected return dates.
  
- Logging:
  - Record visits to the library, including date, time, and purpose.
  - View all log entries to track library visits and activities.
  - View transactions per day to monitor library operations.
  
- Data Security:
  - Utilizes encryption for storing sensitive data such as book inventory, borrow list, and log entries.
  - Encryption keys are generated and managed securely.

Usage
1. Clone the repository to your local machine.
2. Make sure you have Python installed (Python 3.x recommended).
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Run the `library_system.py` script using Python.
5. Follow the on-screen instructions to navigate through different functionalities.

File Structure
- library_system.py: Main Python script containing the library system functionality.
- encryption_key.key: File containing the encryption key. (Automatically generated if not present)
- books.txt: Encrypted file storing the library inventory.
- borrow_list.txt: Encrypted file storing borrow transactions.
- logbook.txt: Encrypted file storing visitation and entry logs.

Contact
For any inquiries or further information, you may contact the author:
- Author: John Aaron B. Llobrera
- Affiliation: BS Statistics, Institute of Statistics, University of the Philippines Los Baños
- E-Mail: jbllobrera@up.edu.ph

Disclaimer
This project is developed by John Aaron B. Llobrera for educational purposes. Use it responsibly and at your own risk.

---
PINAGPUYATAN NI JOHN AARON LLOBRERA (2024). ALL RIGHTS RESERVED.
You may reach out to Aa via jbllobrera@up.edu.ph.

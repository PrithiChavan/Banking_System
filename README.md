#  Banking System (Python Project)

##  Project Description
This is a command-line **Banking System** built in Python.  
It allows users to **create accounts, log in securely, deposit/withdraw money, transfer funds, and view dashboards** with transaction summaries.  
The system uses **file handling** to store account and transaction details in simple text files so data is persistent across sessions.

---

## ✨ Features Implemented
-  Create accounts with password hashing (SHA-256).
-  Secure login with 3 attempts limit.
-  Deposit, withdraw, and transfer money.
-  Update account details (name, password).
-  Dashboard view:
  - Last 3 transactions in tabular format.
  - Monthly deposits vs withdrawals (ASCII bar chart).
  - Category-wise spending summary.
- Data persistence using `accounts.txt` and `transactions.txt`.

---

## Installation Instructions
1. Install **Python 3.7+** on your computer.
2. Install required Python libraries:
   pip install tabulate colorama

## How to Run the Project
1. Clone the repository:
   git clone https://github.com/PrithiChavan/Banking_System.git

## Navigate into the project folder:
cd Banking-System

## Run the program:
python banking_system.py
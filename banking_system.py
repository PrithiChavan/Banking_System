import os
import hashlib
from datetime import datetime
from tabulate import tabulate
from colorama import init, Fore,Style

# Initialize colorama
init(autoreset=True)

# File paths
ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"

# ---------- Utility Functions ----------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_account_number():
    return str(int(datetime.now().timestamp()))[-6:]

# ---------- Account Functions ----------
def create_account():
    print(f"\n{Fore.BLUE}\U0001F4DD Creating a New Account")
    name = input("Enter your name: ")
    try:
        balance = float(input("Enter initial deposit: "))
    except ValueError:
        print(f"{Fore.RED}\u274C Invalid amount!")
        return
    password = input("Enter password: ")
    acc_no = generate_account_number()
    with open(ACCOUNTS_FILE, "a") as f:
        f.write(f"{acc_no},{name},{hash_password(password)},{balance}\n")
    print(f"{Fore.GREEN}\u2705 Account created successfully! Your Account Number: {acc_no}\n")

def login():
    print(f"\n\U0001F511 Logging In...")
    if not os.path.exists(ACCOUNTS_FILE):
        print(f"{Fore.RED}\u274C No accounts found.")
        return None, None, None

    attempts = 0
    while attempts < 3:
        acc_no = input("Enter account number: ")
        password = input("Enter password: ")
        with open(ACCOUNTS_FILE, "r") as f:
            for line in f:
                a_no, name, hashed_pwd, balance = line.strip().split(",")
                if a_no == acc_no and hashed_pwd == hash_password(password):
                    print(f"{Fore.GREEN}\u2705 Login successful! Welcome {name}\n")
                    return acc_no, name, float(balance)
        attempts += 1
        print(f"{Fore.RED}\u274C Invalid account number or password. Attempts left: {3-attempts}\n")
    print(f"{Fore.RED}\u274C Maximum login attempts exceeded.\n")
    return None, None, None

def update_account(acc_no):
    lines = []
    if not os.path.exists(ACCOUNTS_FILE):
        return
    print("\nUpdate Account Info")
    new_name = input("Enter new name (leave blank to keep unchanged): ")
    new_password = input("Enter new password (leave blank to keep unchanged): ")

    with open(ACCOUNTS_FILE, "r") as f:
        for line in f:
            a_no, name, hashed_pwd, balance = line.strip().split(",")
            if a_no == acc_no:
                if new_name.strip() != "":
                    name = new_name
                if new_password.strip() != "":
                    hashed_pwd = hash_password(new_password)
                line = f"{a_no},{name},{hashed_pwd},{balance}\n"
            lines.append(line)
    with open(ACCOUNTS_FILE, "w") as f:
        f.writelines(lines)
    print(f"{Fore.GREEN}\u2705 Account updated successfully!\n")

# ---------- Transaction Functions ----------
def record_transaction(acc_no, t_type, amount, balance_after, category="General"):
    with open(TRANSACTIONS_FILE, "a") as f:
        f.write(f"{acc_no},{t_type},{amount},{balance_after},{datetime.now().strftime('%Y-%m-%d %H:%M:%S')},{category}\n")

def update_balance(acc_no, new_balance):
    lines = []
    with open(ACCOUNTS_FILE, "r") as f:
        for line in f:
            a_no, name, hashed_pwd, balance = line.strip().split(",")
            if a_no == acc_no:
                line = f"{a_no},{name},{hashed_pwd},{new_balance}\n"
            lines.append(line)
    with open(ACCOUNTS_FILE, "w") as f:
        f.writelines(lines)

# ---------- Dashboard Functions ----------
def show_dashboard(acc_no, name, balance):
    print("="*60)
    print(f"\U0001F3E6 Dashboard - {name}")
    print("="*60)
    # Last 3 Transactions
    rows = []
    if os.path.exists(TRANSACTIONS_FILE):
        for line in open(TRANSACTIONS_FILE):
            parts = line.strip().split(",")
            if len(parts) < 6:
                continue
            a_no, t_type, amount, bal_after, date_str, category = parts
            if a_no == acc_no:
                # Color the transaction type
                if t_type == "Deposit":
                    t_type_colored = Fore.GREEN + t_type + Style.RESET_ALL
                elif t_type == "Withdrawal":
                    t_type_colored = Fore.RED + t_type + Style.RESET_ALL
                elif t_type == "Transfer":
                    t_type_colored = Fore.YELLOW + t_type + Style.RESET_ALL
                else:
                    t_type_colored = t_type
                rows.append([t_type_colored, amount, bal_after, date_str, category])
    if rows:
        print("\nLast 3 Transactions:")
        print(tabulate(rows[-3:], headers=["Type","Amount","Balance After","Date/Time","Category"], tablefmt="grid"))
    else:
        print("No transactions yet.")

    monthly_transaction_chart(acc_no)
    monthly_category_chart(acc_no)
    print("="*60 + "\n")


def monthly_transaction_chart(account_number):
    deposits = 0
    withdrawals = 0
    now = datetime.now()
    month_str = now.strftime("%Y-%m")
    if not os.path.exists(TRANSACTIONS_FILE):
        return
    for line in open(TRANSACTIONS_FILE):
        parts = line.strip().split(",")
        if len(parts) < 6:
            continue
        acc_no, t_type, amount, bal_after, date_str, category = parts
        if acc_no != account_number or not date_str.startswith(month_str):
            continue
        amt = float(amount)
        if t_type == "Deposit":
            deposits += amt
        elif t_type == "Withdrawal":
            withdrawals += amt
    max_len = 30
    max_val = max(deposits, withdrawals, 1)
    def make_bar(val):
        return "█" * int((val/max_val)*max_len)
    print("\nMonthly Summary (ASCII Chart):")
    print(f"Deposits   : {make_bar(deposits)} {deposits}")
    print(f"Withdrawals: {make_bar(withdrawals)} {withdrawals}")

def monthly_category_chart(account_number):
    now = datetime.now()
    month_str = now.strftime("%Y-%m")
    categories = {}
    if not os.path.exists(TRANSACTIONS_FILE):
        return
    for line in open(TRANSACTIONS_FILE):
        parts = line.strip().split(",")
        if len(parts) < 6:
            continue
        acc_no, t_type, amount, bal_after, date_str, category = parts
        if acc_no != account_number or not date_str.startswith(month_str):
            continue
        if category not in categories:
            categories[category] = 0
        categories[category] += float(amount)
    if not categories:
        return
    max_len = 30
    max_val = max(categories.values())
    print("\nMonthly Summary by Category:")
    for cat, val in categories.items():
        bar_len = int((val / max_val) * max_len)
        print(f"{cat:<10}: {'█'*bar_len} {val}")
    print()

# ---------- Banking Menu ----------
def banking_menu(acc_no, name, balance):
    while True:
        print("="*40)
        print(f" \U0001F4B0 Banking Menu - {name}")
        print("="*40)
        print("1.\U0001F4B5 Deposit Money")
        print("2.\U0001F4B8 Withdraw Money")
        print("3.\U0001F4B3 Transfer Money")
        print("4. Update Account Info")
        print("5.\U0001F4CA Show Dashboard")
        print("6.\U0001F44B Logout")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            try:
                amount = float(input("Enter deposit amount: "))
                if amount <= 0:
                    print(f"{Fore.RED}\u274C Amount must be positive!")
                    continue
            except ValueError:
                print(f"{Fore.RED}\u274C Invalid input!")
                continue
            category = input("Enter category for this deposit (Food/Rent/Bills/Other): ") or "General"
            balance += amount
            update_balance(acc_no, balance)
            record_transaction(acc_no, "Deposit", amount, balance, category)
            print(f"{Fore.GREEN}\u2705 Deposit successful! Current balance: {balance}\n")
        elif choice == "2":
            try:
                amount = float(input("Enter withdrawal amount: "))
                if amount <= 0:
                    print(f"{Fore.RED}\u274C Amount must be positive!")
                    continue
            except ValueError:
                print(f"{Fore.RED}\u274C Invalid input!")
                continue
            if amount > balance:
                print(f"{Fore.RED}\u274C Insufficient balance!\n")
            else:
                category = input("Enter category for this withdrawal (Food/Rent/Bills/Other): ") or "General"
                balance -= amount
                update_balance(acc_no, balance)
                record_transaction(acc_no, "Withdrawal", amount, balance, category)
                print(f"{Fore.GREEN}\u2705 Withdrawal successful! Current balance: {balance}\n")
        elif choice == "3":
            recipient_acc = input("Enter recipient account number: ")
            try:
                amount = float(input("Enter amount to transfer: "))
            except ValueError:
                print(f"{Fore.RED}\u274C Invalid amount!")
                continue
            if amount <= 0:
                print(f"{Fore.RED}\u274C Amount must be positive!")
                continue
            if amount > balance:
                print(f"{Fore.RED}\u274C Insufficient balance!\n")
                continue
            recipient_found = False
            lines = []
            with open(ACCOUNTS_FILE, "r") as f:
                for line in f:
                    a_no, r_name, r_hashed_pwd, r_balance = line.strip().split(",")
                    if a_no == recipient_acc:
                        recipient_found = True
                        r_balance = float(r_balance) + amount
                        line = f"{a_no},{r_name},{r_hashed_pwd},{r_balance}\n"
                    lines.append(line)
            if not recipient_found:
                print(f"{Fore.RED}\u274C Recipient account not found!\n")
                continue
            # Update sender balance
            balance -= amount
            update_balance(acc_no, balance)
            # Update recipient balance
            with open(ACCOUNTS_FILE, "w") as f:
                f.writelines(lines)
            # Record transactions
            record_transaction(acc_no, "Withdrawal", amount, balance, "Transfer")
            record_transaction(recipient_acc, "Deposit", amount, r_balance, "Transfer")
            print(f"{Fore.GREEN}\u2705 Transfer successful! New balance: {balance}\n")
        elif choice == "4":
            update_account(acc_no)
        elif choice == "5":
            show_dashboard(acc_no, name, balance)
        elif choice == "6":
            print(f"{Fore.GREEN}\U0001F44B Logging out... Thank You\n")
            break
        else:
            print(f"{Fore.RED}\u274C Invalid choice! Try again.\n")

# ---------- Main Menu ----------
def main():
    while True:
        print("="*50)
        print(f"\U0001F3E6 Welcome to the Banking System")
        print("="*50)
        print("1. \U0001F4DD Create Account")
        print("2. \U0001F511 Login")
        print("3. \u274C Exit")
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            create_account()
        elif choice == "2":
            acc_no, name, balance = login()
            if acc_no:
                banking_menu(acc_no, name, balance)
        elif choice == "3":
            print(f"{Fore.GREEN}\U0001F44B Thank you for using the Banking System!")
            break
        else:
            print(f"{Fore.RED}\u274C Invalid choice! Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()
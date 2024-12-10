import csv
import os
from constants import EXCEL_FILE  # Still using the same file name, but it will be CSV

def initialize_csv():
    """Creates the CSV file with appropriate headers if it doesn't already exist."""
    try:
        if not os.path.exists(EXCEL_FILE):
            with open(EXCEL_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["First Name", "Last Name", "PIN", "Account Type", "Balance"])  # Headers
    except Exception as e:
        print(f"Error initializing CSV file: {e}")
        raise


def get_account(first_name, last_name, pin):
    """Retrieves account details if First Name, Last Name, and PIN match."""
    try:
        with open(EXCEL_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if row[0] == first_name and row[1] == last_name and row[2] == pin:
                    return {
                        "First Name": row[0],
                        "Last Name": row[1],
                        "PIN": row[2],
                        "Account Type": row[3],
                        "Balance": float(row[4]),
                    }
    except Exception as e:
        print(f"Error retrieving account: {e}")
    return None  # No matching account found


def add_account(first_name, last_name, pin, account_type, balance):
    """Adds a new account to the CSV file."""
    try:
        # Check if the PIN already exists
        accounts = get_all_accounts()
        if any(account["PIN"] == pin for account in accounts):
            return False  # Duplicate PIN

        # Append the new account data
        with open(EXCEL_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_name, pin, account_type, balance])
        return True
    except Exception as e:
        print(f"Error adding account: {e}")
        return False


def update_account(pin, new_balance):
    """Updates the balance of an account identified by its PIN."""
    try:
        accounts = get_all_accounts()
        updated = False
        with open(EXCEL_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["First Name", "Last Name", "PIN", "Account Type", "Balance"])  # Header
            for account in accounts:
                if account["PIN"] == pin:
                    account["Balance"] = new_balance
                    updated = True
                writer.writerow([account["First Name"], account["Last Name"], account["PIN"], account["Account Type"], account["Balance"]])
        return updated
    except Exception as e:
        print(f"Error updating account: {e}")
    return False  # Account not found

def get_all_accounts():
    """Retrieves all accounts as a list of dictionaries."""
    accounts = []
    try:
        with open(EXCEL_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                accounts.append({
                    "First Name": row[0],
                    "Last Name": row[1],
                    "PIN": row[2],
                    "Account Type": row[3],
                    "Balance": float(row[4]),
                })
    except Exception as e:
        print(f"Error retrieving all accounts: {e}")
    return accounts

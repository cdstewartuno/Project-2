import tkinter as tk
from tkinter import messagebox
from accounts import CheckingAccount, SavingAccount
from data_handler import add_account, get_account, update_account
from validation import is_valid_pin, is_valid_name, is_valid_amount
from constants import ERROR_PIN, ERROR_NAME, ERROR_AMOUNT, ERROR_CREDENTIALS

class BankApp:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Bank App")

        self.first_name_entry = None
        self.last_name_entry = None
        self.pin_entry = None
        self.account_type_var = tk.StringVar(value="Checking")  # Default to Checking

    def create_account(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        pin = self.pin_entry.get().strip()
        account_type = self.account_type_var.get()

        # Validate inputs
        if not is_valid_name(first_name) or not is_valid_name(last_name):
            messagebox.showerror("Error", ERROR_NAME)
            return
        if not is_valid_pin(pin):
            messagebox.showerror("Error", ERROR_PIN)
            return

        # Check if the account already exists
        existing_account = get_account(first_name, last_name, pin)
        if existing_account:
            messagebox.showerror("Error", "An account with this information already exists.")
            return

        # Ask user if they are sure about entering this data
        if messagebox.askyesno("Confirm", f"Are you sure you want to create this account?\nName: {first_name} {last_name}, Pin: {pin}, Account Type: {account_type}"):
            initial_balance = 100 if account_type == "Saving" else 0  # Saving accounts start with 100 balance
            success = add_account(first_name, last_name, pin, account_type, initial_balance)
            if success:
                messagebox.showinfo("Success", "Account created successfully!")
                # Clear input fields
                self.first_name_entry.delete(0, tk.END)
                self.last_name_entry.delete(0, tk.END)
                self.pin_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "An account with this PIN already exists.")

    def login(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        pin = self.pin_entry.get().strip()

        if not is_valid_name(first_name) or not is_valid_name(last_name):
            messagebox.showerror("Error", ERROR_NAME)
            return
        if not is_valid_pin(pin):
            messagebox.showerror("Error", ERROR_PIN)
            return

        # Retrieve account details for login
        account_data = get_account(first_name, last_name, pin)
        if not account_data:
            messagebox.showerror("Error", ERROR_CREDENTIALS)
            return

        # Create account object based on selected account type
        account = (
            SavingAccount(account_data["First Name"], account_data["Last Name"], pin, account_data["Balance"])
            if account_data["Account Type"] == "Saving"
            else CheckingAccount(account_data["First Name"], account_data["Last Name"], pin, account_data["Balance"])
        )

        self.transaction_window(account)

    def transaction_window(self, account):
        def perform_transaction():
            action = action_var.get()
            amount_str = amount_entry.get().strip()

            # Validate amount input
            try:
                amount = float(amount_str)
                if amount <= 0 or round(amount, 2) != amount:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Amount must be a positive number with up to 2 decimal places.")
                return

            if action == "Deposit":
                success = account.deposit(amount)
            else:
                success = account.withdraw(amount)

            if success:
                update_account(account.get_pin(), account.get_balance())
                messagebox.showinfo("Success", f"Transaction successful! New Balance: ${account.get_balance():.2f}")
            else:
                messagebox.showerror("Error", "Transaction failed. Check balance or input.")

        transaction = tk.Toplevel(self.app)
        transaction.title("Transaction")

        tk.Label(transaction, text=f"Welcome {account.get_full_name()}").pack(pady=5)
        tk.Label(transaction, text=f"Balance: ${account.get_balance():.2f}").pack(pady=5)

        action_var = tk.StringVar(value="Deposit")
        tk.Radiobutton(transaction, text="Deposit", variable=action_var, value="Deposit").pack(anchor="w")
        tk.Radiobutton(transaction, text="Withdraw", variable=action_var, value="Withdraw").pack(anchor="w")

        tk.Label(transaction, text="Amount:").pack()
        amount_entry = tk.Entry(transaction)
        amount_entry.pack()

        tk.Button(transaction, text="Submit", command=perform_transaction).pack(pady=10)

    def initialize_gui(self):
        """Initialize the GUI components."""

        # Create Account Section
        tk.Label(self.app, text="First Name:").grid(row=0, column=0)
        self.first_name_entry = tk.Entry(self.app)
        self.first_name_entry.grid(row=0, column=1)

        tk.Label(self.app, text="Last Name:").grid(row=1, column=0)
        self.last_name_entry = tk.Entry(self.app)
        self.last_name_entry.grid(row=1, column=1)

        tk.Label(self.app, text="PIN:").grid(row=2, column=0)
        self.pin_entry = tk.Entry(self.app, show="*")
        self.pin_entry.grid(row=2, column=1)

        tk.Label(self.app, text="Account Type:").grid(row=3, column=0)

        # Radio buttons for account selection
        tk.Radiobutton(self.app, text="Checking", variable=self.account_type_var, value="Checking").grid(row=3, column=1, sticky="w")
        tk.Radiobutton(self.app, text="Saving", variable=self.account_type_var, value="Saving").grid(row=4, column=1, sticky="w")

        tk.Button(self.app, text="Create Account", command=self.create_account).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.app, text="Login", command=self.login).grid(row=6, column=0, columnspan=2, pady=10)
        tk.Button(self.app, text="Exit", command=self.app.quit).grid(row=7, column=0, columnspan=2, pady=10)

    def run(self):
        """Method to run the main GUI loop."""
        self.initialize_gui()
        self.app.mainloop()  # This starts the GUI event loop


class Account:
    def __init__(self, first_name, last_name, pin, balance=0):
        self.__first_name = first_name
        self.__last_name = last_name
        self.__pin = pin
        self.__balance = balance if balance >= 0 else 0

    def deposit(self, amount):
        """Deposits the specified amount into the account if valid."""
        if amount > 0:
            self.__balance += amount
            return True
        return False

    def withdraw(self, amount):
        """Withdraws the specified amount if it does not exceed the current balance."""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

    def get_balance(self):
        """Returns the current balance of the account."""
        return self.__balance

    def get_full_name(self):
        """Returns the full name of the account holder."""
        return f"{self.__first_name} {self.__last_name}"

    def get_pin(self):
        """Returns the account's PIN (for authentication purposes)."""
        return self.__pin

    def __str__(self):
        """Returns a string representation of the account."""
        return f"Account holder: {self.get_full_name()}, Balance: ${self.__balance:.2f}"


class SavingAccount(Account):
    MINIMUM_BALANCE = 100
    INTEREST_RATE = 0.02

    def __init__(self, first_name, last_name, pin, balance=MINIMUM_BALANCE):
        super().__init__(first_name, last_name, pin, balance)
        self.__deposit_count = 0

    def deposit(self, amount):
        """Deposits an amount and applies interest after every fifth deposit."""
        if super().deposit(amount):
            self.__deposit_count += 1
            if self.__deposit_count >= 5:
                self.__apply_interest()
                self.__deposit_count = 0
            return True
        return False

    def withdraw(self, amount):
        """Withdraws only if the remaining balance meets or exceeds the minimum."""
        if self.get_balance() - amount >= self.MINIMUM_BALANCE:
            return super().withdraw(amount)
        return False

    def __apply_interest(self):
        """Applies interest to the account."""
        new_balance = self.get_balance() * (1 + self.INTEREST_RATE)
        self.set_balance(new_balance)

    def set_balance(self, amount):
        """Sets the balance, ensuring it does not fall below the minimum."""
        super().set_balance(max(amount, self.MINIMUM_BALANCE))

    def __str__(self):
        """Returns a string representation of the savings account."""
        return f"SAVING ACCOUNT: {super().__str__()}, Minimum Balance: ${self.MINIMUM_BALANCE:.2f}"


class CheckingAccount(Account):
    OVERDRAFT_LIMIT = -500

    def __init__(self, first_name, last_name, pin, balance=0):
        super().__init__(first_name, last_name, pin, balance)

    def withdraw(self, amount):
        """Allows withdrawal up to the overdraft limit."""
        if self.get_balance() - amount >= self.OVERDRAFT_LIMIT:
            return super().withdraw(amount)
        return False

    def __str__(self):
        """Returns a string representation of the checking account."""
        return f"CHECKING ACCOUNT: {super().__str__()}, Overdraft Limit: ${self.OVERDRAFT_LIMIT:.2f}"

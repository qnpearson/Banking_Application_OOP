import sys
from datetime import datetime
from rich.console import Console
from rich.table import Table

class BankAccount:
    def __init__(self, name, pin):
        self.name = name
        self.pin = pin
        self.checking_account = 0.0  # Balance for checking account
        self.savings_account = 0.0  # Balance for savings account
        self.transaction_history = {}  # Dictionary to store transaction history

    def record_transaction(self, transaction_type, amount, account_type):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history[timestamp] = f"{transaction_type} ${amount:.2f} - {account_type}"

    def deposit(self, amount, account_type):
        if amount <= 0:
            return "Deposit amount must be positive."
        if account_type == "checking":
            self.checking_account += amount
            self.record_transaction("Deposit", amount, "Checking Account")
        elif account_type == "savings":
            self.savings_account += amount
            self.record_transaction("Deposit", amount, "Savings Account")
        else:
            return "Invalid account type. Choose 'checking' or 'savings'."
        return f"Deposit successful. New {account_type.capitalize()} Balance: ${self.get_balance(account_type):.2f}"

    def withdraw(self, amount, account_type):
        if amount <= 0:
            return "Withdrawal amount must be positive."
        if account_type == "checking":
            if self.checking_account >= amount:
                self.checking_account -= amount
                self.record_transaction("Withdrawal", amount, "Checking Account")
            else:
                return "Insufficient funds in Checking Account."
        elif account_type == "savings":
            if self.savings_account >= amount:
                self.savings_account -= amount
                self.record_transaction("Withdrawal", amount, "Savings Account")
            else:
                return "Insufficient funds in Savings Account."
        else:
            return "Invalid account type. Choose 'checking' or 'savings'."
        return f"Withdrawal successful. New {account_type.capitalize()} Balance: ${self.get_balance(account_type):.2f}"

    def transfer(self, amount, from_account, to_account):
        if amount <= 0:
            return "Transfer amount must be positive."
        if from_account == "checking" and to_account == "savings":
            if self.checking_account >= amount:
                self.checking_account -= amount
                self.savings_account += amount
                self.record_transaction("Transfer", amount, "Savings Account from Checking Account")
            else:
                return "Insufficient funds in Checking Account."
        elif from_account == "savings" and to_account == "checking":
            if self.savings_account >= amount:
                self.savings_account -= amount
                self.checking_account += amount
                self.record_transaction("Transfer", amount, "Checking Account from Savings Account")
            else:
                return "Insufficient funds in Savings Account."
        else:
            return "Invalid account types. Choose 'checking' or 'savings' for both accounts."
        return f"Transfer successful. {from_account.capitalize()} Balance: ${self.get_balance(from_account):.2f}, {to_account.capitalize()} Balance: ${self.get_balance(to_account):.2f}"

    def get_balance(self, account_type):
        if account_type == "checking":
            return self.checking_account
        elif account_type == "savings":
            return self.savings_account
        else:
            return None

    def show_transaction_history(self):
        console = Console()
        table = Table(title=f"{self.name.capitalize()}'s Transaction History")
        table.add_column("Timestamp", justify="center", style="cyan", no_wrap=True)
        table.add_column("Details", justify="left", style="magenta", no_wrap=True)
        for timestamp, details in self.transaction_history.items():
            table.add_row(timestamp, details)
        console.print(table)


def main():
    # Create a placeholder for the user's account
    account = None

    while True:
        # Display menu
        console = Console()
        table = Table(title="Welcome to QP Bank. Select an option number.")
        table.add_column("Number", justify="center", style="cyan", no_wrap=True)
        table.add_column("Option", justify="left", style="magenta", no_wrap=True)
        table.add_row("[1]", "Create an account.")
        table.add_row("[2]", "Access your account information.")
        table.add_row("[3]", "Make a deposit.")
        table.add_row("[4]", "Make a withdrawal.")
        table.add_row("[5]", "Transfer money.")
        table.add_row("[6]", "View transaction history.")
        table.add_row("[7]", "Quit system.")
        console.print(table)

        choice = input("Input option number: ").strip()
        match choice:
            case "1":
                name = input("Enter your full name (First Last): ").lower()
                pin = input("Create a 4-digit PIN: ")
                account = BankAccount(name, pin)
                print("Account created successfully!")
            case "2":
                if not account:
                    print("No account exists. Please create an account first.")
                else:
                    print(f"Account Holder: {account.name.capitalize()}")
                    print(f"Checking Balance: ${account.checking_account:.2f}")
                    print(f"Savings Balance: ${account.savings_account:.2f}")
            case "3":
                if not account:
                    print("No account exists. Please create an account first.")
                else:
                    account_type = input("Deposit to (checking/savings): ").lower()
                    amount = float(input("Enter deposit amount: $"))
                    print(account.deposit(amount, account_type))
            case "4":
                if not account:
                    print("No account exists. Please create an account first.")
                else:
                    account_type = input("Withdraw from (checking/savings): ").lower()
                    amount = float(input("Enter withdrawal amount: $"))
                    print(account.withdraw(amount, account_type))
            case "5":
                if not account:
                    print("No account exists. Please create an account first.")
                else:
                    from_account = input("Transfer from (checking/savings): ").lower()
                    to_account = input("Transfer to (checking/savings): ").lower()
                    amount = float(input("Enter transfer amount: $"))
                    print(account.transfer(amount, from_account, to_account))
            case "6":
                if not account:
                    print("No account exists. Please create an account first.")
                else:
                    account.show_transaction_history()
            case "7":
                sys.exit(f"Quitting system. Thank you for banking with us!\n Transaction History:\n {account.show_transaction_history()}")
            case _:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

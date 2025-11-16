# Copyleft 🄯 2025, Germano Castanho
# Free software under the GNU GPL v3


import datetime
from abc import ABC, abstractmethod

WITHDRAWAL_LIMIT = 3
WITHDRAWAL_AMOUNT_LIMIT = 500.0


class Transaction(ABC):
    @property
    @abstractmethod
    def amount(self):
        pass

    @abstractmethod
    def register(self, account):
        pass


class Deposit(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        success = account.deposit(self.amount)
        if success:
            account.history.add_transaction(self)


class Withdrawal(Transaction):
    def __init__(self, amount):
        self._amount = amount

    @property
    def amount(self):
        return self._amount

    def register(self, account):
        success = account.withdraw(self.amount)
        if success:
            account.history.add_transaction(self)


class History:
    def __init__(self):
        self._transactions = []

    def add_transaction(self, transaction):
        self._transactions.append(
            {
                "type": transaction.__class__.__name__,
                "amount": transaction.amount,
                "date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    def generate_report(self):
        report = ""
        for transaction in self._transactions:
            report += f"[{transaction['date']}] {transaction['type']}: $ {transaction['amount']:.2f}\n"
        return report


class Account:
    def __init__(self, number, client):
        self._balance = 0.0
        self._number = number
        self._agency = "0001"
        self._client = client
        self._history = History()

    @classmethod
    def new_account(cls, client, number):
        return cls(number, client)

    @property
    def balance(self):
        return self._balance

    @property
    def number(self):
        return self._number

    @property
    def agency(self):
        return self._agency

    @property
    def client(self):
        return self._client

    @property
    def history(self):
        return self._history

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"\n✓ Deposit of $ {amount:.2f} completed successfully!")
            return True

        else:
            print("\n✗ Operation failed! Invalid amount.")
            return False

    def withdraw(self, amount):
        balance = self.balance

        if amount > balance:
            print("\n✗ Operation failed! Insufficient balance.")
            return False

        elif amount > 0:
            self._balance -= amount
            print(f"\n✓ Withdrawal of $ {amount:.2f} completed successfully!")
            return True

        else:
            print("\n✗ Operation failed! Invalid amount.")
            return False


class CheckingAccount(Account):
    def __init__(self, number, client):
        super().__init__(number, client)
        self._limit = WITHDRAWAL_AMOUNT_LIMIT
        self._withdrawal_limit = WITHDRAWAL_LIMIT

    def withdraw(self, amount):
        withdrawals_num = len(
            [t for t in self.history._transactions if t["type"] == "Withdrawal"]
        )

        exceeded_limit = amount > self._limit
        exceeded_withdrawals = withdrawals_num >= self._withdrawal_limit

        if exceeded_limit:
            print("\n✗ Operation failed! Withdrawal amount exceeds limit.")
            return False

        elif exceeded_withdrawals:
            print(
                "\n✗ Operation failed! Maximum number of withdrawals exceeded."
            )
            return False

        else:
            success = super().withdraw(amount)
            if success:
                print(
                    f" Remaining withdrawals: {self._withdrawal_limit - withdrawals_num - 1}"
                )
            return success

    def __str__(self):
        return f"""\
            Agency:     {self.agency}
            Account:    {self.number}
            Holder:     {self.client.name}
        """


class Client:
    def __init__(self, address):
        self.address = address
        self.accounts = []

    def perform_transaction(self, account, transaction):
        transaction.register(account)

    def add_account(self, account):
        self.accounts.append(account)


class Individual(Client):
    def __init__(self, cpf, name, birth_date, address):
        super().__init__(address)
        self.cpf = cpf
        self.name = name
        self.birth_date = birth_date


def filter_client(cpf, clients):
    filtered_clients = [client for client in clients if client.cpf == cpf]
    return filtered_clients[0] if filtered_clients else None


def retrieve_client_account(client):
    if not client.accounts:
        print("\n✗ Client has no accounts!")
        return None

    return client.accounts[0]


def deposit(clients):
    print("\n--- DEPOSIT ---")
    try:
        cpf = input("Enter CPF (numbers only): ")
        client = filter_client(cpf, clients)

        if not client:
            print("\n✗ Client not found!")
            return None

        amount = float(input("Enter deposit amount: $ "))
        transaction = Deposit(amount)

        account = retrieve_client_account(client)
        if not account:
            return None

        client.perform_transaction(account, transaction)

    except ValueError:
        print("\n✗ Error! Please enter a valid numeric value.")


def withdraw(clients):
    print("\n--- WITHDRAWAL ---")
    try:
        cpf = input("Enter CPF (numbers only): ")
        client = filter_client(cpf, clients)

        if not client:
            print("\n✗ Client not found!")
            return None

        amount = float(input("Enter withdrawal amount: $ "))
        transaction = Withdrawal(amount)

        account = retrieve_client_account(client)
        if not account:
            return None

        client.perform_transaction(account, transaction)

    except ValueError:
        print("\n✗ Error! Please enter a valid numeric value.")


def display_statement(clients):
    cpf = input("Enter CPF (numbers only): ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n✗ Client not found!")
        return None

    account = retrieve_client_account(client)
    if not account:
        return None

    print("\n" + "=" * 45)
    print("                 BANK STATEMENT")
    print("=" * 45)

    transactions = account.history.generate_report()

    if not transactions:
        print("\nNo transactions found.")

    else:
        print(transactions)

    print("-" * 45)
    print(f"Current balance: $ {account.balance:.2f}")
    print("=" * 45)


def create_client(clients):
    cpf = input("Enter CPF (numbers only): ")
    client = filter_client(cpf, clients)

    if client:
        print("\n✗ Client with this CPF already exists!")
        return None

    name = input("Enter full name: ")
    birth_date = input("Enter birth date (dd-mm-yyyy): ")
    address = input("Enter address (street, number - district - city/state): ")

    client = Individual(
        cpf=cpf,
        name=name,
        birth_date=birth_date,
        address=address,
    )

    clients.append(client)
    print("\n✓ Client created successfully!")


def create_account(account_number, clients, accounts):
    cpf = input("Enter client's CPF: ")
    client = filter_client(cpf, clients)

    if not client:
        print("\n✗ Client not found!")
        return None

    account = CheckingAccount.new_account(client=client, number=account_number)
    accounts.append(account)
    client.add_account(account)

    print("\n✓ Account created successfully!")


def list_accounts(accounts):
    if not accounts:
        print("\n✗ No accounts registered!")
        return None

    for account in accounts:
        print("=" * 50)
        print(str(account))


def display_menu():
    menu = """
╔════════════════════════════════════╗
║           BANK SYSTEM 🏦           ║
╠════════════════════════════════════╣
║  [1] Deposit 💰                    ║
║  [2] Withdraw 💸                   ║
║  [3] Statement 🧾                  ║
║  [4] New Account 💳                ║
║  [5] List Accounts 📋              ║
║  [6] New User 👤                   ║
║  [q] Quit 👋                       ║
╚════════════════════════════════════╝

=> Choose an option: """

    return input(menu).lower().strip()


def main():
    clients = []
    accounts = []

    print("\n✓ Banking System Started")
    print(f"Daily withdrawal limit: {WITHDRAWAL_LIMIT}")
    print(f"Maximum amount per withdrawal: $ {WITHDRAWAL_AMOUNT_LIMIT:.2f}")

    while True:
        option = display_menu()

        if option == "1":
            deposit(clients)

        elif option == "2":
            withdraw(clients)

        elif option == "3":
            display_statement(clients)

        elif option == "4":
            account_number = len(accounts) + 1
            create_account(account_number, clients, accounts)

        elif option == "5":
            list_accounts(accounts)

        elif option == "6":
            create_client(clients)

        elif option == "q":
            print("\n" + "=" * 45)
            print("Thank you for using our banking system!")
            print("Goodbye! 👋")
            print("=" * 45 + "\n")
            break

        else:
            print("\n✗ Invalid operation! Please select again.")


if __name__ == "__main__":
    main()

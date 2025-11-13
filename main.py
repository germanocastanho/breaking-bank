import datetime

WITHDRAWAL_LIMIT = 3
WITHDRAWAL_AMOUNT_LIMIT = 500.0


def deposit(balance, amount, statement):
    if amount > 0:
        balance += amount
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        statement += f"[{timestamp}] Deposit: $ {amount:.2f}\n"
        print(f"\n✓ Deposit of $ {amount:.2f} completed successfully!")

    else:
        print("\n✗ Operation failed! Invalid amount.")

    return balance, statement


def withdraw(
    *,
    balance,
    amount,
    statement,
    limit,
    withdrawals_num,
    withdrawal_limit,
):
    exceeded_balance = amount > balance
    exceeded_limit = amount > limit
    exceeded_withdrawals = withdrawals_num >= withdrawal_limit

    if exceeded_balance:
        print("\n✗ Operation failed! Insufficient balance.")

    elif exceeded_limit:
        print("\n✗ Operation failed! Withdrawal amount exceeds limit.")

    elif exceeded_withdrawals:
        print("\n✗ Operation failed! Maximum number of withdrawals exceeded.")

    elif amount > 0:
        balance -= amount
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        statement += f"[{timestamp}] Withdrawal: $ {amount:.2f}\n"
        withdrawals_num += 1
        print(f"\n✓ Withdrawal of $ {amount:.2f} completed successfully!")
        print(f" Remaining withdrawals: {withdrawal_limit - withdrawals_num}")

    else:
        print("\n✗ Operation failed! Invalid amount.")

    return balance, statement, withdrawals_num


def display_statement(balance, *, statement):
    print("\n" + "=" * 45)
    print("                 BANK STATEMENT")
    print("=" * 45)

    if not statement:
        print("\nNo transactions found.")

    else:
        print(statement)

    print("-" * 45)
    print(f"Current balance: $ {balance:.2f}")
    print("=" * 45)


def display_menu():
    menu = """
    ╔════════════════════════════════════╗
    ║           BANK SYSTEM 🏦           ║
    ╠════════════════════════════════════╣
    ║  [1] Deposit 💰                    ║
    ║  [2] Withdraw 💸                   ║
    ║  [3] Statement 🧾                  ║
    ║  [q] Quit 👋                       ║
    ╚════════════════════════════════════╝
    
    => Choose an option: """

    return input(menu).lower().strip()


def main():
    balance = 0.0
    statement = ""
    withdrawals_num = 0

    print("\n✓ Banking System Started")
    print(f"Daily withdrawal limit: {WITHDRAWAL_LIMIT}")
    print(f"Maximum amount per withdrawal: $ {WITHDRAWAL_AMOUNT_LIMIT:.2f}")

    while True:
        option = display_menu()

        if option == "1":
            print("\n--- DEPOSIT ---")
            try:
                amount = float(input("Enter deposit amount: $ "))
                balance, statement = deposit(balance, amount, statement)

            except ValueError:
                print("\n✗ Error! Please enter a valid numeric value.")

        elif option == "2":
            print("\n--- WITHDRAWAL ---")
            try:
                amount = float(input("Enter withdrawal amount: $ "))
                balance, statement, withdrawals_num = withdraw(
                    balance=balance,
                    amount=amount,
                    statement=statement,
                    limit=WITHDRAWAL_AMOUNT_LIMIT,
                    withdrawals_num=withdrawals_num,
                    withdrawal_limit=WITHDRAWAL_LIMIT,
                )

            except ValueError:
                print("\n✗ Error! Please enter a valid numeric value.")

        elif option == "3":
            display_statement(balance, statement=statement)

        elif option == "q":
            print("\n" + "=" * 50)
            print("Thank you for using our banking system!")
            print("Goodbye! 👋")
            print("=" * 50 + "\n")
            break

        else:
            print("\n✗ Invalid operation! Please select again.")


if __name__ == "__main__":
    main()

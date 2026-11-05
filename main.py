import json
class Wallet:
    def __init__(self, owner, pin, balance=0):
        self.owner = owner
        self.pin = pin
        self.balance = balance
        self.transactions = []
        self.wrong_pin_attempts = 0
        self.locked = False

    def verify_pin(self, entered_pin):
        if self.locked:
            print("Your wallet is locked.")
            return False

        if entered_pin == self.pin:
            self.wrong_pin_attempts = 0
            print("Login successful!")
            return True

        self.wrong_pin_attempts += 1
        print("Incorrect PIN!")

        if self.wrong_pin_attempts == 3:
            self.locked = True
            print("Your wallet has been locked!")
        else:
            print("Attempts remaining:", 3 - self.wrong_pin_attempts)

        return False

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        self.balance = round(self.balance + amount, 2)
        self.transactions.append({
            "type": "Deposit",
            "amount": amount
        })

        print("Deposit successful!")
        print("New balance: $", self.balance)

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        fee = 0.50
        total = round(amount + fee, 2)

        if total > self.balance:
            print("Insufficient balance!")
            return

        self.balance = round(self.balance - total, 2)

        self.transactions.append({
            "type": "Withdrawal",
            "amount": amount,
            "fee": fee
        })

        print("Withdrawal successful!")
        print("Fee: $", fee)
        print("New balance: $", self.balance)

    def transfer(self, recipient, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        if self == recipient:
            print("You cannot transfer to your own wallet.")
            return

        if recipient.locked:
            print("The receiving wallet is locked.")
            return

        fee = 0.50
        total = round(amount + fee, 2)

        if total > self.balance:
            print("Insufficient balance!")
            return

        self.balance = round(self.balance - total, 2)
        recipient.balance = round(recipient.balance + amount, 2)

        self.transactions.append({
            "type": "Transfer sent",
            "amount": amount,
            "fee": fee,
            "recipient": recipient.owner
        })

        recipient.transactions.append({
            "type": "Transfer received",
            "amount": amount,
            "sender": self.owner
        })

        print("Transfer successful!")
        print("You sent: $", amount)
        print("Fee: $", fee)
        print("New balance: $", self.balance)

    def display_wallet(self):
        print("\n----- WALLET DETAILS -----")
        print("Owner:", self.owner)
        print("Balance: $", self.balance)
        print("Wallet Locked:", self.locked)

    def display_history(self):
        print("\n===== TRANSACTION HISTORY =====")
        print("Customer:", self.owner)

        if not self.transactions:
            print("No transactions found.")
            return

        for number, transaction in enumerate(self.transactions, 1):
            print("\nTransaction", number)
            print("Type:", transaction["type"])
            print("Amount: $", transaction["amount"])

            if "fee" in transaction:
                print("Fee: $", transaction["fee"])

            if "recipient" in transaction:
                print("Sent to:", transaction["recipient"])

            if "sender" in transaction:
                print("Received from:", transaction["sender"])

        print("\nCurrent balance: $", self.balance)


wallets = []


def save_wallets():
    data = []

    for wallet in wallets:
        details = {
            "owner": wallet.owner,
            "pin": wallet.pin,
            "balance": wallet.balance,
            "transactions": wallet.transactions,
            "wrong_pin_attempts": wallet.wrong_pin_attempts,
            "locked": wallet.locked
        }
        data.append(details)

    with open("wallet_data.json", "w") as file:
        json.dump(data, file, indent=4)


def load_wallets():
    try:
        with open("wallet_data.json", "r") as file:
            data = json.load(file)

        for details in data:
            wallet = Wallet(
                details["owner"],
                details["pin"],
                details["balance"]
            )

            wallet.transactions = details["transactions"]
            wallet.wrong_pin_attempts = details["wrong_pin_attempts"]
            wallet.locked = details["locked"]

            wallets.append(wallet)

        print("Saved wallets loaded successfully!")

    except FileNotFoundError:
        print("No previous wallet records found.")

    except json.JSONDecodeError:
        print("The wallet data file is empty or damaged.")


def find_wallet(owner):
    for wallet in wallets:
        if wallet.owner.lower() == owner.lower():
            return wallet
    return None


def login_wallet():
    owner = input("Enter your name: ").strip()
    wallet = find_wallet(owner)

    if wallet is None:
        print("Wallet not found.")
        return None

    if wallet.locked:
        print("This wallet is locked.")
        return None

    pin = input("Enter your PIN: ")

    if wallet.verify_pin(pin):
        return wallet

    return None


def create_wallet():
    print("\n===== CREATE NEW WALLET =====")

    owner = input("Enter customer name: ").strip()
    pin = input("Create a 4-digit PIN: ")

    if not owner:
        print("Name cannot be empty.")
        return

    if len(pin) != 4 or not pin.isdigit():
        print("PIN must contain exactly 4 digits.")
        return

    if find_wallet(owner):
        print("Customer already has a wallet.")
        return

    wallets.append(Wallet(owner, pin))
    print("Wallet created successfully!")


def deposit_money():
    print("\n===== DEPOSIT MONEY =====")
    wallet = login_wallet()

    if wallet:
        try:
            amount = float(input("Enter amount to deposit: $"))
            wallet.deposit(amount)
        except ValueError as error:
            print("Error:", error)


def withdraw_money():
    print("\n===== WITHDRAW MONEY =====")
    wallet = login_wallet()

    if wallet:
        try:
            amount = float(input("Enter amount to withdraw: $"))
            wallet.withdraw(amount)
        except ValueError as error:
            print("Error:", error)


def transfer_money():
    print("\n===== SEND MONEY =====")
    sender = login_wallet()

    if sender:
        recipient_name = input("Enter receiver's name: ").strip()
        recipient = find_wallet(recipient_name)

        if recipient is None:
            print("Receiving wallet not found.")
            return

        try:
            amount = float(input("Enter amount to send: $"))
            sender.transfer(recipient, amount)
        except ValueError as error:
            print("Error:", error)


def check_balance():
    print("\n===== CHECK WALLET BALANCE =====")
    wallet = login_wallet()

    if wallet:
        wallet.display_wallet()


def view_history():
    print("\n===== VIEW TRANSACTION HISTORY =====")
    wallet = login_wallet()

    if wallet:
        wallet.display_history()


def main_menu():
    load_wallets()

    while True:
        print("\n===================================")
        print("     MOBILE MONEY WALLET SYSTEM")
        print("===================================")
        print("1. Create a new wallet")
        print("2. Check wallet balance")
        print("3. Deposit money")
        print("4. Withdraw money")
        print("5. Transfer money")
        print("6. View transaction history")
        print("7. Exit")
        print("===================================")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            create_wallet()
        elif choice == "2":
            check_balance()
        elif choice == "3":
            deposit_money()
        elif choice == "4":
            withdraw_money()
        elif choice == "5":
            transfer_money()
        elif choice == "6":
            view_history()
        elif choice == "7":
            save_wallets()
            print("Thank you for using our wallet system!")
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1 to 7.")

        save_wallets()


main_menu()

import json
from datetime import datetime


class BudgetTracker:
    def __init__(self, filename='budget_data.json'):
        self.filename = filename
        self.transactions = self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_transactions(self):
        with open(self.filename, 'w') as file:
            json.dump(self.transactions, file, indent=4)

    def add_transaction(self, amount, category, transaction_type):
        transaction = {
            'id': len(self.transactions) + 1,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': float(amount),
            'category': category,
            'type': transaction_type
        }
        self.transactions.append(transaction)
        self.save_transactions()
        print(f"Transaction added successfully: {transaction}")

    def get_balance(self):
        income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        expenses = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        return income - expenses

    def get_category_summary(self):
        category_summary = {}
        for transaction in self.transactions:
            if transaction['type'] == 'expense':
                category = transaction['category']
                amount = transaction['amount']
                category_summary[category] = category_summary.get(category, 0) + amount
        return category_summary

    def view_transactions(self, transaction_type=None):
        if transaction_type:
            filtered_transactions = [t for t in self.transactions if t['type'] == transaction_type]
        else:
            filtered_transactions = self.transactions

        for transaction in filtered_transactions:
            print(f"ID: {transaction['id']} | Date: {transaction['date']} | "
                  f"Amount: ${transaction['amount']:.2f} | "
                  f"Category: {transaction['category']} | "
                  f"Type: {transaction['type']}")


def main():
    tracker = BudgetTracker()

    while True:
        print("\n--- Personal Budget Tracker ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. View Income Transactions")
        print("5. View Expense Transactions")
        print("6. Check Balance")
        print("7. Category Summary")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        try:
            match choice:
                case '1':
                    amount = float(input("Enter income amount: "))
                    category = input("Enter income category: ")
                    tracker.add_transaction(amount, category, 'income')

                case '2':
                    amount = float(input("Enter expense amount: "))
                    category = input("Enter expense category: ")
                    tracker.add_transaction(amount, category, 'expense')

                case '3':
                    tracker.view_transactions()

                case '4':
                    tracker.view_transactions('income')

                case '5':
                    tracker.view_transactions('expense')

                case '6':
                    print(f"Current Balance: ${tracker.get_balance():.2f}")

                case '7':
                    summary = tracker.get_category_summary()
                    print("\nExpense Category Summary:")
                    for category, total in summary.items():
                        print(f"{category}: ₹{total:.2f}")

                case '8':
                    print("Thank you for using Budget Tracker!")
                    break

                case _:
                    print("Invalid choice. Please try again.")

        except ValueError:
            print("Invalid input. Please enter correct values.")


if __name__ == "__main__":
    main()
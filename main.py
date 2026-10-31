import argparse
import json
from dataclasses import dataclass, asdict
from datetime import date, datetime
from pathlib import Path

import requests
from pydantic import BaseModel, Field, ValidationError


FILE_NAME = "expenses.json"


# Store expense information
@dataclass
class Expense:
    id: int
    amount: float
    category: str
    date: str
    description: str


# Validate expense information
class ExpenseValidator(BaseModel):
    amount: float = Field(gt=0)
    category: str = Field(min_length=1)
    date: date
    description: str = Field(min_length=1)


# Read expenses from JSON file
def load_expenses() -> list[dict]:
    file = Path(FILE_NAME)

    if not file.exists():
        return []

    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Error: Could not read expenses file.")
        return []


# Save expenses to JSON file
def save_expenses(expenses: list[dict]) -> None:
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=4)


# Add a new expense
def add_expense(args):
    try:
        expense_data = ExpenseValidator(
            amount=args.amount,
            category=args.category.strip(),
            date=args.date,
            description=args.description.strip()
        )

        expenses = load_expenses()

        new_id = max(
            [e["id"] for e in expenses],
            default=0
        ) + 1

        expense = Expense(
            id=new_id,
            amount=expense_data.amount,
            category=expense_data.category,
            date=expense_data.date.isoformat(),
            description=expense_data.description
        )

        expenses.append(asdict(expense))
        save_expenses(expenses)

        print("Expense added successfully!")
        print("Expense ID:", new_id)

    except ValidationError as error:
        print("Invalid expense details:")
        for item in error.errors():
            print("-", item["msg"])

    except (OSError, TypeError, ValueError) as error:
        print("Error saving expense:", error)


# List and filter expenses
def list_expenses(args):
    expenses = load_expenses()

    if args.category:
        expenses = [
            e for e in expenses
            if e["category"].lower() == args.category.lower()
        ]

    if args.start:
        expenses = [
            e for e in expenses
            if e["date"] >= args.start
        ]

    if args.end:
        expenses = [
            e for e in expenses
            if e["date"] <= args.end
        ]

    if not expenses:
        print("No expenses found.")
        return

    print("\nID | Date | Category | Amount | Description")
    print("-" * 60)

    for e in expenses:
        print(
            f"{e['id']} | {e['date']} | "
            f"{e['category']} | {e['amount']:.2f} | "
            f"{e['description']}"
        )


# Delete an expense
def delete_expense(args):
    expenses = load_expenses()

    remaining = [
        e for e in expenses
        if e["id"] != args.id
    ]

    if len(remaining) == len(expenses):
        print("Expense ID not found.")
        return

    try:
        save_expenses(remaining)
        print("Expense deleted successfully!")
    except OSError as error:
        print("Error deleting expense:", error)


# Show monthly totals by category
def monthly_summary(args):
    expenses = load_expenses()
    totals = {}

    for expense in expenses:
        if expense["date"].startswith(args.month):
            category = expense["category"]

            totals[category] = (
                totals.get(category, 0) + expense["amount"]
            )

    if not totals:
        print("No expenses found for this month.")
        return

    print("\nMonthly Summary:", args.month)

    for category, amount in sorted(totals.items()):
        print(f"{category}: {amount:.2f}")

    print("-" * 30)
    print(f"Total: {sum(totals.values()):.2f}")


# Convert total expenses to another currency
def convert_currency(args):
    expenses = load_expenses()

    total = sum(e["amount"] for e in expenses)

    url = (
        "https://open.er-api.com/v6/latest/"
        + args.from_currency.upper()
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("result") != "success":
            print("Could not get currency rates.")
            return

        target = args.to_currency.upper()
        rates = data.get("rates", {})

        if target not in rates:
            print("Invalid target currency code.")
            return

        converted = total * rates[target]

        print(f"Total expenses: {total:.2f} "
              f"{args.from_currency.upper()}")

        print(f"Converted total: {converted:.2f} {target}")

    except requests.RequestException:
        print("Network error. Check your internet connection.")

    except (KeyError, TypeError, ValueError):
        print("Error reading currency data.")


# Check date format
def check_date(value):
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Date must use YYYY-MM-DD format."
        )


# Check month format
def check_month(value):
    try:
        datetime.strptime(value, "%Y-%m")
        return value
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Month must use YYYY-MM format."
        )


# Main program and commands
def main():
    parser = argparse.ArgumentParser(
        description="Smart Expense Tracker CLI"
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Add expense command
    add = commands.add_parser("add", help="Add an expense")

    add.add_argument("--amount", type=float, required=True)
    add.add_argument("--category", required=True)
    add.add_argument(
        "--date",
        type=check_date,
        default=date.today().isoformat()
    )
    add.add_argument("--description", required=True)

    add.set_defaults(func=add_expense)

    # List expenses command
    listing = commands.add_parser("list", help="List expenses")

    listing.add_argument("--category")
    listing.add_argument("--start", type=check_date)
    listing.add_argument("--end", type=check_date)

    listing.set_defaults(func=list_expenses)

    # Delete expense command
    delete = commands.add_parser(
        "delete", help="Delete an expense"
    )

    delete.add_argument("--id", type=int, required=True)
    delete.set_defaults(func=delete_expense)

    # Monthly summary command
    summary = commands.add_parser(
        "summary", help="Show monthly summary"
    )

    summary.add_argument(
        "--month",
        type=check_month,
        required=True
    )

    summary.set_defaults(func=monthly_summary)

    # Currency conversion command
    convert = commands.add_parser(
        "convert", help="Convert total expenses"
    )

    convert.add_argument(
        "--from-currency",
        default="INR"
    )

    convert.add_argument(
        "--to-currency",
        required=True
    )

    convert.set_defaults(func=convert_currency)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

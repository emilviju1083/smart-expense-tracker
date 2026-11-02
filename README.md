# Smart Expense Tracker CLI

A beginner-friendly Python command-line application for managing daily expenses. It stores expense records in a JSON file and supports filtering, monthly summaries, currency conversion, and CSV export.

## Features

- Add new expenses.
- List and filter expenses by category and date range.
- Delete expenses using their IDs.
- View monthly spending totals by category.
- Convert the total expenses to another currency using an exchange-rate API.
- Export expenses to a CSV file that can be opened in Excel.
- Validate expense details and display error messages for invalid input.
- Store expense records locally in JSON format.

## Technologies Used

- Python
- argparse
- JSON
- CSV
- requests
- Pydantic
- Dataclasses
- Exchange Rate API

## Requirements

- Python 3.10 or newer
- pip
- Internet connection for currency conversion

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/emilviju1083/smart-expense-tracker.git
   ```

2. Open the project folder:

   ```bash
   cd smart-expense-tracker
   ```

3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate the environment on Windows:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Usage

Run all commands from the project folder.

### Show available commands

```bash
python main.py --help
```

### Add an expense

```bash
python main.py add --amount 250 --category Food --description "Lunch" --date 2026-11-02
```

The date is optional. If omitted, the application uses today's date.

### List expenses

```bash
python main.py list
```

### Filter by category

```bash
python main.py list --category Food
```

### Filter by date range

```bash
python main.py list --start 2026-11-01 --end 2026-11-30
```

### Delete an expense

Replace `1` with the ID of the expense you want to delete.

```bash
python main.py delete --id 1
```

### View a monthly summary

```bash
python main.py summary --month 2026-11
```

### Convert total expenses to another currency

For example, convert the total from INR to USD:

```bash
python main.py convert --from-currency INR --to-currency USD
```

Currency conversion requires an internet connection and uses the exchange-rate API.

### Export expenses to CSV

```bash
python main.py export
```

This creates an `expenses.csv` file in the project folder.

## Data Storage

Expense records are stored in `expenses.json`. The exported CSV file is named `expenses.csv`.

Both files are excluded from Git using `.gitignore` so that personal expense records are not accidentally published.

## Project Structure

```text
smart-expense-tracker/
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── expenses.json       # Local data; not committed
```

## Learning Goals

This project demonstrates Python fundamentals, command-line argument parsing, data validation, JSON file handling, CSV export, API requests, exception handling, and Git/GitHub collaboration workflows.

## Author

Emil Viju

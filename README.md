
# Personal Financer

## Overview

Personal Financer is a powerful and user-friendly Python application designed to simplify personal finance management. Whether you're a budgeting enthusiast, a freelancer tracking income, or someone looking to gain better control over your financial health, this tool empowers you to monitor your income, expenses, and savings with ease. Built with a lightweight SQLite database, it offers robust functionality to categorize transactions, generate insightful summaries, and export data to CSV for advanced analysis in tools like Excel or Google Sheets. Its modular design makes it ideal for standalone use or integration into custom financial dashboards and applications.

Key highlights include:
- **Intuitive Transaction Management**: Add, view, edit, or delete transactions effortlessly.
- **Flexible Categorization**: Organize your finances by custom categories (e.g., groceries, utilities, salary).
- **Insightful Summaries**: Generate detailed reports by month or category to understand spending patterns.
- **Data Portability**: Export transactions to CSV for external analysis or record-keeping.
- **Developer-Friendly**: Easily extend or integrate with other systems using the `FinanceDataHandler` class.

Personal Financer is perfect for individuals seeking a lightweight, open-source solution to track their finances or for developers looking to build custom financial tools.

## Features

- Add, view, edit, and delete transactions with date, amount, and category details
- Categorize transactions into income, expenses, or savings
- Generate monthly and category-wise financial summaries
- Export transaction data to CSV for external use
- SQLite database for efficient and reliable data storage
- Modular Python codebase for easy customization or integration

## Requirements

- Python 3.x
- pandas (`pip install pandas`)
- SQLite (included with Python)

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/personal-financer.git
   cd personal-financer
   ```

2. **Install dependencies:**
   ```bash
   pip install pandas
   ```

3. **Run the application:**
   ```bash
   python data_handler.py
   ```

4. **Optional**: Integrate the `FinanceDataHandler` class into your own UI or scripts for custom workflows.

## Usage

- Use the `FinanceDataHandler` class to manage transactions programmatically:
  ```python
  from data_handler import FinanceDataHandler
  handler = FinanceDataHandler()
  handler.add_transaction(date="2025-04-20", amount=100.50, category="Salary", type="Income")
  handler.get_monthly_summary(month="04", year="2025")
  handler.export_to_csv("transactions.csv")
  ```
- Explore summaries by category or month to gain insights into your financial habits.
- Export data to CSV for further analysis in spreadsheets or visualization tools.

## Project Structure

- `data_handler.py`: Core logic for managing transactions and database operations
- `finance.db`: SQLite database storing transaction data
- `requirements.txt`: List of dependencies

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to enhance functionality, fix bugs, or improve documentation. To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -m "Add feature"`)
4. Push to the branch (`git push origin feature-name`)
5. Open a pull request

## License

MIT License

## Future Enhancements

- Web or GUI interface for easier interaction
- Support for recurring transactions
- Integration with external APIs for real-time bank data
- Advanced analytics (e.g., budgeting goals, forecasting)


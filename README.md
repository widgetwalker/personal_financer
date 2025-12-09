# 💰 Personal Financer

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

A powerful Python tool for personal finance management with transaction tracking, category-wise analysis, and CSV export capabilities. Built with SQLite for efficient data storage and Pandas for advanced analytics.

---

## ✨ Features

- 💳 **Transaction Management** - Add, view, edit, and delete transactions
- 📊 **Category Organization** - Organize by income, expenses, or savings
- 📈 **Financial Summaries** - Monthly and category-wise reports
- 📁 **CSV Export** - Export data for external analysis
- 💾 **SQLite Database** - Reliable, lightweight data storage
- 📉 **Data Visualization** - Charts and graphs for spending patterns
- 🔄 **Modular Design** - Easy integration with custom applications
- 🎯 **Developer-Friendly** - Clean API for programmatic access

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/widgetwalker/personal_financer.git
cd personal_financer

# Install dependencies
pip install pandas matplotlib
```

### Run the Application

```bash
# Run main application
python main.py

# Or use the data handler directly
python data_handler.py
```

---

## 📦 Dependencies

```
pandas>=1.5.0
matplotlib>=3.6.0
sqlite3 (included with Python)
```

---

## 🎮 Usage

### Interactive CLI

```bash
python main.py
```

Follow the menu prompts to:
- Add new transactions
- View transaction history
- Generate summaries
- Export to CSV

### Programmatic API

```python
from data_handler import FinanceDataHandler

# Initialize handler
handler = FinanceDataHandler()

# Add transaction
handler.add_transaction(
    date="2025-04-20",
    amount=100.50,
    category="Salary",
    type="Income"
)

# Get monthly summary
summary = handler.get_monthly_summary(month="04", year="2025")

# Export to CSV
handler.export_to_csv("transactions.csv")
```

---

## 📂 Project Structure

```
personal_financer/
├── main.py                  # Main application with CLI interface
├── data_handler.py          # Core transaction management logic
├── db_setup.py              # Database initialization
├── visualizer.py            # Data visualization utilities
├── finance.db               # SQLite database (auto-created)
├── finance_tracker.db       # Backup database
└── README.md                # This file
```

---

## 🔧 Core Components

### FinanceDataHandler
Main class for transaction management:
- `add_transaction()` - Add new transaction
- `get_all_transactions()` - Retrieve all records
- `update_transaction()` - Modify existing transaction
- `delete_transaction()` - Remove transaction
- `get_monthly_summary()` - Generate monthly report
- `get_category_summary()` - Analyze by category
- `export_to_csv()` - Export data

### Database Schema

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 📊 Features in Detail

### Transaction Categories
- **Income**: Salary, Freelance, Investments, Other
- **Expenses**: Groceries, Utilities, Rent, Entertainment, Transport
- **Savings**: Emergency Fund, Retirement, Goals

### Summary Reports
- **Monthly**: Total income, expenses, and savings per month
- **Category-wise**: Spending breakdown by category
- **Yearly**: Annual financial overview
- **Custom**: Filter by date range or category

### Data Export
- **CSV Format**: Compatible with Excel, Google Sheets
- **Filtered Exports**: Export specific date ranges or categories
- **Backup**: Regular database backups

---

## 🎨 Visualization

```python
from visualizer import FinanceVisualizer

viz = FinanceVisualizer()

# Generate spending pie chart
viz.plot_category_distribution()

# Create monthly trend line
viz.plot_monthly_trends()

# Compare income vs expenses
viz.plot_income_vs_expenses()
```

---

## 💡 Use Cases

### Personal Finance Tracking
- Monitor daily expenses
- Track income sources
- Analyze spending patterns

### Budgeting
- Set category budgets
- Compare actual vs planned spending
- Identify cost-saving opportunities

### Tax Preparation
- Export transaction history
- Categorize deductible expenses
- Generate annual summaries

---

## 🐛 Troubleshooting

### Database Issues
```bash
# Reset database
rm finance.db
python db_setup.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade pandas matplotlib
```

### CSV Export Problems
- Check file permissions
- Ensure output directory exists
- Verify data format

---

## 🚀 Future Enhancements

- 🌐 **Web Interface** - Browser-based UI with Flask/Django
- 📱 **Mobile App** - Cross-platform mobile application
- 🔄 **Recurring Transactions** - Auto-add monthly bills
- 🏦 **Bank Integration** - Import transactions from banks
- 📊 **Advanced Analytics** - Budgeting goals and forecasting
- 🔔 **Notifications** - Alerts for budget limits
- 🌍 **Multi-currency** - Support for multiple currencies

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Links

- **Repository:** [github.com/widgetwalker/personal_financer](https://github.com/widgetwalker/personal_financer)
- **Issues:** [Report a bug](https://github.com/widgetwalker/personal_financer/issues)
- **Author:** [@widgetwalker](https://github.com/widgetwalker)

---

## 📧 Contact

**Dheeraj Pilli**
- GitHub: [@widgetwalker](https://github.com/widgetwalker)
- Email: dheeraj5765483@gmail.com

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

*Built with ❤️ using Python, SQLite, and Pandas*

</div>

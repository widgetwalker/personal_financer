import sqlite3
import pandas as pd
import os

class FinanceDataHandler:
    def __init__(self):
        self.conn = sqlite3.connect("finance.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                transaction_type TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_transaction(self, date, amount, category, description, transaction_type):
        self.cursor.execute('''
            INSERT INTO transactions (date, amount, category, description, transaction_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, amount, category, description, transaction_type))
        self.conn.commit()

    def get_all_transactions(self):
        self.cursor.execute('SELECT * FROM transactions')
        rows = self.cursor.fetchall()
        columns = ['id', 'date', 'amount', 'category', 'description', 'transaction_type']
        return pd.DataFrame(rows, columns=columns)

    def get_all_categories(self):
        self.cursor.execute('SELECT * FROM categories')
        rows = self.cursor.fetchall()
        columns = ['id', 'name', 'type']
        return pd.DataFrame(rows, columns=columns)

    def get_summary_by_category(self, transaction_type, start_date=None, end_date=None):
        query = '''
            SELECT category, SUM(amount) as total
            FROM transactions
            WHERE transaction_type = ?
        '''
        params = [transaction_type]
        if start_date and end_date:
            query += ' AND date BETWEEN ? AND ?'
            params.extend([start_date, end_date])
        query += ' GROUP BY category'
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return pd.DataFrame(rows, columns=['category', 'total'])

    def get_monthly_summary(self, year):
        query = '''
            SELECT strftime('%m', date) as month, 
                   strftime('%Y', date) as year,
                   SUM(CASE WHEN transaction_type = 'income' THEN amount ELSE 0 END) as income,
                   SUM(CASE WHEN transaction_type = 'expense' THEN amount ELSE 0 END) as expense,
                   SUM(CASE WHEN transaction_type = 'saving' THEN amount ELSE 0 END) as saving
            FROM transactions
            WHERE strftime('%Y', date) = ?
            GROUP BY strftime('%m', date)
        '''
        self.cursor.execute(query, (year,))
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows, columns=['month', 'year', 'income', 'expense', 'saving'])
        df['month_name'] = pd.to_datetime(df['month'], format='%m').dt.strftime('%B')
        return df

    def export_to_csv(self, filename):
        transactions_df = self.get_all_transactions()
        transactions_df.to_csv(filename, index=False)
        return os.path.abspath(filename)

    def delete_transaction(self, transaction_id):
        self.cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
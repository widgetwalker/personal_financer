import sqlite3
import os

def create_database():
    # Create database if it doesn't exist
    if not os.path.exists('finance_tracker.db'):
        conn = sqlite3.connect('finance_tracker.db')
        cursor = conn.cursor()
        
        # Create transactions table
        cursor.execute('''
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            transaction_type TEXT NOT NULL
        )
        ''')
        
        # Create categories table
        cursor.execute('''
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL
        )
        ''')
        
        # Insert default categories
        default_categories = [
            ('Salary', 'income'),
            ('Freelance', 'income'),
            ('Groceries', 'expense'),
            ('Rent', 'expense'),
            ('Utilities', 'expense'),
            ('Entertainment', 'expense'),
            ('Transportation', 'expense'),
            ('Savings', 'saving'),
            ('Investment', 'saving')
        ]
        
        cursor.executemany('INSERT INTO categories (name, type) VALUES (?, ?)', default_categories)
        
        conn.commit()
        conn.close()
        print("Database created successfully!")
    else:
        print("Database already exists!")

if __name__ == "__main__":
    create_database()

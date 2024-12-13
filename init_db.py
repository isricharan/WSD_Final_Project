import sqlite3
import json


def initialize_database():
    # Connect to SQLite database
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    # Drop existing tables if they exist (to reset the database)
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS items')
    cursor.execute('DROP TABLE IF EXISTS customers')

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            UNIQUE (name, phone)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            name TEXT PRIMARY KEY NOT NULL,
            price REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            notes TEXT,
            timestamp INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (item_name) REFERENCES items(name)
        )
    ''')

    conn.commit()

    # Load data from JSON file
    with open('example_orders.json', 'r') as file:
        orders_data = json.load(file)

    for order in orders_data:
        # Insert customer
        cursor.execute('''
            INSERT OR IGNORE INTO customers (name, phone)
            VALUES (?, ?)
        ''', (order['name'], order['phone']))

        # Retrieve customer ID
        cursor.execute('''
            SELECT id FROM customers WHERE name = ? AND phone = ?
        ''', (order['name'], order['phone']))
        customer_id = cursor.fetchone()[0]

        # Insert items into the items table
        for item in order['items']:
            cursor.execute('''
                INSERT OR IGNORE INTO items (name, price)
                VALUES (?, ?)
            ''', (item['name'], item['price']))

            # Insert order with item
            cursor.execute('''
                INSERT INTO orders (customer_id, item_name, notes, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (customer_id, item['name'], order['notes'], order['timestamp']))

    conn.commit()
    conn.close()
    print("Database created and populated successfully.")


if __name__ == "__main__":
    initialize_database()

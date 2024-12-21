import sqlite3
import json


def initialize_database():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    # Drop tables if they exist
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS items')
    cursor.execute('DROP TABLE IF EXISTS customers')

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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            notes TEXT,
            timestamp INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    ''')


    conn.commit()

    with open('example_orders.json', 'r') as file:
        orders_data = json.load(file)


    for order in orders_data:

        cursor.execute('''
            INSERT OR IGNORE INTO customers (name, phone)
            VALUES (?, ?)
        ''', (order['name'], order['phone']))


        cursor.execute('''
            SELECT id FROM customers WHERE name = ? AND phone = ?
        ''', (order['name'], order['phone']))
        customer_id = cursor.fetchone()[0]


        for item in order['items']:

            cursor.execute('''
                INSERT OR IGNORE INTO items (name, price)
                VALUES (?, ?)
            ''', (item['name'], item['price']))

            cursor.execute('''
                SELECT id FROM items WHERE name = ? AND price = ?
            ''', (item['name'], item['price']))
            item_id = cursor.fetchone()[0]

            cursor.execute('''
                INSERT INTO orders (customer_id, item_id, notes, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (customer_id, item_id, order['notes'], order['timestamp']))


    conn.commit()

    conn.close()

    print("Database created and populated successfully.")


if __name__ == "__main__":
    initialize_database()

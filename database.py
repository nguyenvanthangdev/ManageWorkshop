import sqlite3

class Database:
    def __init__(self, db_name='Database/database.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        quantity INTEGER NOT NULL,
                        price REAL NOT NULL
                    )
                ''')
        self.connection.commit()

    def register_user(self, username, password):
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validate_user(self, username, password):
        self.cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        return self.cursor.fetchone() is not None

    def get_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def delete_user(self, username):
        self.cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        self.connection.commit()


    def update_password(self, username, new_password):
        self.cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
        self.connection.commit()

    def validate_register_check_user(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone() is not None
    # manage warehouse

    def get_products(self):
        self.cursor.execute('SELECT name, quantity, price FROM products')
        return self.cursor.fetchall()

    def add_product(self, name, quantity, price):
        try:
            self.cursor.execute('INSERT INTO products (name, quantity, price) VALUES (?, ?, ?)',
                                (name, quantity, price))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Product already exists.")

    def update_product(self, old_name, new_name, quantity, price):
        self.cursor.execute('''
             UPDATE products
             SET name = ?, quantity = ?, price = ?
             WHERE name = ?
         ''', (new_name, quantity, price, old_name))
        self.connection.commit()

    def delete_product(self, name):
        self.cursor.execute('DELETE FROM products WHERE name = ?', (name,))
        self.connection.commit()

    def close(self):
        self.connection.close()

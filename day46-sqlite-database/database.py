"""
Database module for SQLite operations
"""

import sqlite3
import os


class Database:
    """SQLite database handler for product management"""

    def __init__(self, db_path: str = "data/products.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print(f"[OK] Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            print(f"[ERROR] Database connection error: {e}")
            raise

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("[OK] Database connection closed")

    def create_tables(self):
        """Create all tables if they don't exist"""
        try:
            # Products table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock_quantity INTEGER NOT NULL,
                    supplier TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Customers table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    city TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Orders table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    total_amount REAL NOT NULL,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            """)

            # Order items table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """)

            self.connection.commit()
            print("[OK] All tables created successfully")

        except sqlite3.Error as e:
            print(f"[ERROR] Table creation error: {e}")
            self.connection.rollback()
            raise

    def execute_query(self, query: str, params: tuple = ()):
        """Execute SELECT query and return results as list of dictionaries"""
        try:
            self.cursor.execute(query, params)
            columns = [description[0] for description in self.cursor.description]
            results = []
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
        except sqlite3.Error as e:
            print(f"[ERROR] Query execution error: {e}")
            return []

    def execute_insert(self, query: str, params: tuple) -> int:
        """Execute INSERT query and return last row id"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"[ERROR] Insert error: {e}")
            self.connection.rollback()
            return -1

    def execute_update(self, query: str, params: tuple) -> int:
        """Execute UPDATE query and return number of rows affected"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"[ERROR] Update error: {e}")
            self.connection.rollback()
            return -1

    def execute_delete(self, query: str, params: tuple) -> int:
        """Execute DELETE query and return number of rows affected"""
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"[ERROR] Delete error: {e}")
            self.connection.rollback()
            return -1

    def get_table_data(self, table_name: str):
        """Get all data from a table"""
        query = f"SELECT * FROM {table_name}"
        return self.execute_query(query)

    def get_table_count(self, table_name: str) -> int:
        """Get row count from a table"""
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        result = self.execute_query(query)
        return result[0]['count'] if result else 0

    def close(self):
        """Alias for disconnect"""
        self.disconnect()
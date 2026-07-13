"""
Data models for the database application
"""

from database import Database


class Product:
    """Product model"""

    def __init__(self, db: Database):
        self.db = db

    def create(self, name: str, category: str, price: float,
               stock_quantity: int, supplier: str = None) -> int:
        """Insert a new product"""
        query = """
            INSERT INTO products (name, category, price, stock_quantity, supplier)
            VALUES (?, ?, ?, ?, ?)
        """
        return self.db.execute_insert(query, (name, category, price, stock_quantity, supplier))

    def get_all(self):
        """Get all products"""
        return self.db.get_table_data('products')

    def get_by_id(self, product_id: int):
        """Get product by ID"""
        query = "SELECT * FROM products WHERE id = ?"
        results = self.db.execute_query(query, (product_id,))
        return results[0] if results else None

    def update(self, product_id: int, **kwargs) -> int:
        """Update product fields"""
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            values.append(value)
        values.append(product_id)

        query = f"UPDATE products SET {', '.join(fields)} WHERE id = ?"
        return self.db.execute_update(query, tuple(values))

    def delete(self, product_id: int) -> int:
        """Delete product by ID"""
        query = "DELETE FROM products WHERE id = ?"
        return self.db.execute_delete(query, (product_id,))

    def get_by_category(self, category: str):
        """Get products by category"""
        query = "SELECT * FROM products WHERE category = ?"
        return self.db.execute_query(query, (category,))

    def get_low_stock(self, threshold: int = 10):
        """Get products with stock below threshold"""
        query = "SELECT * FROM products WHERE stock_quantity < ? ORDER BY stock_quantity"
        return self.db.execute_query(query, (threshold,))


class Customer:
    """Customer model"""

    def __init__(self, db: Database):
        self.db = db

    def create(self, first_name: str, last_name: str, email: str,
               phone: str = None, city: str = None) -> int:
        """Insert a new customer"""
        query = """
            INSERT INTO customers (first_name, last_name, email, phone, city)
            VALUES (?, ?, ?, ?, ?)
        """
        return self.db.execute_insert(query, (first_name, last_name, email, phone, city))

    def get_all(self):
        """Get all customers"""
        return self.db.get_table_data('customers')

    def get_by_id(self, customer_id: int):
        """Get customer by ID"""
        query = "SELECT * FROM customers WHERE id = ?"
        results = self.db.execute_query(query, (customer_id,))
        return results[0] if results else None

    def get_by_city(self, city: str):
        """Get customers by city"""
        query = "SELECT * FROM customers WHERE city = ?"
        return self.db.execute_query(query, (city,))


class Order:
    """Order model"""

    def __init__(self, db: Database):
        self.db = db

    def create(self, customer_id: int, total_amount: float, status: str = 'pending') -> int:
        """Insert a new order"""
        query = """
            INSERT INTO orders (customer_id, total_amount, status)
            VALUES (?, ?, ?)
        """
        return self.db.execute_insert(query, (customer_id, total_amount, status))

    def add_item(self, order_id: int, product_id: int, quantity: int, unit_price: float) -> int:
        """Add item to order"""
        query = """
            INSERT INTO order_items (order_id, product_id, quantity, unit_price)
            VALUES (?, ?, ?, ?)
        """
        return self.db.execute_insert(query, (order_id, product_id, quantity, unit_price))

    def get_all(self):
        """Get all orders"""
        return self.db.get_table_data('orders')

    def get_by_id(self, order_id: int):
        """Get order by ID"""
        query = "SELECT * FROM orders WHERE id = ?"
        results = self.db.execute_query(query, (order_id,))
        return results[0] if results else None

    def get_items(self, order_id: int):
        """Get all items for an order"""
        query = """
            SELECT oi.*, p.name as product_name
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        """
        return self.db.execute_query(query, (order_id,))

    def get_by_customer(self, customer_id: int):
        """Get orders by customer"""
        query = "SELECT * FROM orders WHERE customer_id = ? ORDER BY order_date DESC"
        return self.db.execute_query(query, (customer_id,))

    def update_status(self, order_id: int, status: str) -> int:
        """Update order status"""
        query = "UPDATE orders SET status = ? WHERE id = ?"
        return self.db.execute_update(query, (status, order_id))

    def get_total_by_customer(self):
        """Get total spent by each customer"""
        query = """
            SELECT
                c.id,
                c.first_name || ' ' || c.last_name as customer_name,
                COUNT(o.id) as order_count,
                SUM(o.total_amount) as total_spent
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            GROUP BY c.id
            ORDER BY total_spent DESC
        """
        return self.db.execute_query(query)
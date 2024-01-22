import logging

from db import CursorFromConnectionPool

logger = logging.getLogger(__name__)


class Product:
    def __init__(self, name, price, img_url):
        self.id = None
        self.name = name
        self.price = price
        self.img_url = img_url

    @staticmethod
    def create_products_table():
        """Create the products table."""

        # Create the products table with auto-incrementing id
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255),
                    price FLOAT(4),
                    img_url VARCHAR
                )"""
            )
        logger.info("Products table created")

    @staticmethod
    def save_product(product):
        """Save the product to the database."""

        # Check if the product is already in the database
        with CursorFromConnectionPool() as cursor:
            cursor.execute("SELECT * FROM products WHERE id = %s", (product.id,))
            product_data = cursor.fetchone()
            if product_data is not None:
                logger.info("Product already in database")
                return

        # Save the product to the database
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                """INSERT INTO products (name, price, img_url)
                VALUES (%s, %s, %s)""",
                (
                    product.name,
                    product.price,
                    product.img_url,
                ),
            )

    @staticmethod
    def delete_product(product):
        """Delete the product from the database."""

        # Delete the product from the database
        with CursorFromConnectionPool() as cursor:
            cursor.execute("DELETE FROM products WHERE id = %s", (product.id,))

    @classmethod
    def get_all_products(cls):
        """Get all products from the database and add them to the list."""

        products = []

        with CursorFromConnectionPool() as cursor:
            cursor.execute("SELECT * FROM products")
            products_data = cursor.fetchall()
            for product_data in products_data:
                product = cls(product_data[1], product_data[2], product_data[3])
                product.id = product_data[0]  # Assign the id after retrieving from the database
                products.append(product)
        return products

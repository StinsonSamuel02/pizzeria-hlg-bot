"""Database user handlers"""
import logging
from db import CursorFromConnectionPool

logger = logging.getLogger(__name__)


class User:
    def __init__(self, id, first_name, last_name, username, language_code):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code

    @staticmethod
    def create_users_table():
        """Create the users table."""

        # Create the users table
        with CursorFromConnectionPool() as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY, first_name VARCHAR(255),
                last_name VARCHAR(255), username VARCHAR(255), language_code VARCHAR(255))"""
            )
        logger.info("Users table created")

    @staticmethod
    def save_user(user):
        """Save the user to the database."""

        # Check if the user is already in the database
        with CursorFromConnectionPool() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user.id,))
            user_data = cursor.fetchone()
            if (
                    user_data
                    is not None
            ):
                logger.info("User already in database")
                return

                # Save the user to the database
            cursor.execute(
                """INSERT INTO users (id, first_name, last_name, username, language_code)
                VALUES (%s, %s, %s, %s, %s)""",
                (
                    user.id,
                    user.first_name,
                    user.last_name,
                    user.username,
                    user.language_code,
                ),
            )
            '''# Note the (email,) to make it a tuple!
                cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
                user_data = cursor.fetchone()
                return cls(email=user_data[1], first_name=user_data[2], last_name=user_data[3], id=user_data[0])'''

    @staticmethod
    def delete_user(user):
        """Delete the user from the database."""

        # Delete the user from the database
        with CursorFromConnectionPool() as cursor:
            cursor.execute("DELETE FROM users WHERE id = %s", (user.id,))

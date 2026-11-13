from mysql.connector import Error

from Database_Automation.config.settings import DB_NAME
from Database_Automation.database.connection import (
    get_server_connection,
    get_database_connection
)


def setup_database():

    connection = None
    cursor = None

    try:

        # Connect to MySQL server
        connection = get_server_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        # Create database
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"
        )

        print("Database created or already exists!")

    except Error as error:

        print("Database Setup Error:", error)

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

    # Test connection to the newly created database
    connection = get_database_connection()

    if connection is None:
        return

    cursor = None

    try:

        cursor = connection.cursor()

        cursor.execute(
            "SELECT DATABASE(), VERSION()"
        )

        result = cursor.fetchone()

        print("\nDatabase Connection Successful!")
        print("Database Name:", result[0])
        print("MySQL Version:", result[1])

    except Error as error:

        print("Database Verification Error:", error)

    finally:

        if cursor is not None:
            cursor.close()

        if connection.is_connected():
            connection.close()


if __name__ == "__main__":
    setup_database()
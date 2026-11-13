
from mysql.connector import Error

from Database_Automation.database.connection import (
    get_database_connection
)


def create_employee_table():

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS employees (

            id INT AUTO_INCREMENT PRIMARY KEY,

            name VARCHAR(100) NOT NULL,

            email VARCHAR(150) UNIQUE NOT NULL,

            department VARCHAR(100),

            salary DECIMAL(10, 2),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """

        cursor.execute(create_table_query)

        print("Employee table created successfully!")

        # Verify table structure
        cursor.execute("DESCRIBE employees")

        columns = cursor.fetchall()

        print("\nEmployee Table Structure:")

        for column in columns:
            print(column)

    except Error as error:

        print("Table Creation Error:", error)

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    create_employee_table()

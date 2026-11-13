
from mysql.connector import Error

from Database_Automation.database.connection import (
    get_database_connection
)


def insert_single_employee(cursor, connection):

    query = """
        INSERT INTO employees
        (name, email, department, salary)
        VALUES (%s, %s, %s, %s)
    """

    employee = (
        "John Smith",
        "john@example.com",
        "IT",
        55000.00
    )

    cursor.execute(query, employee)

    connection.commit()

    print("Single employee inserted!")
    print("Generated ID:", cursor.lastrowid)


def insert_multiple_employees(cursor, connection):

    query = """
        INSERT INTO employees
        (name, email, department, salary)
        VALUES (%s, %s, %s, %s)
    """

    employees = [

        ("Alice", "alice@example.com", "HR", 45000.00),

        ("Robert", "robert@example.com", "IT", 60000.00),

        ("David", "david@example.com", "Finance", 50000.00),

        ("Emma", "emma@example.com", "Marketing", 48000.00)

    ]

    cursor.executemany(query, employees)

    connection.commit()

    print("Multiple employees inserted!")
    print("Records inserted:", cursor.rowcount)


def fetch_one_employee(cursor):

    query = """
        SELECT * FROM employees
        WHERE id = %s
    """

    cursor.execute(query, (1,))

    employee = cursor.fetchone()

    print("\nSingle Employee:")

    print(employee)


def fetch_multiple_employees(cursor):

    query = """
        SELECT id, name, department, salary
        FROM employees
        WHERE salary >= %s
        ORDER BY salary DESC
        LIMIT %s
    """

    cursor.execute(query, (45000, 5))

    employees = cursor.fetchall()

    print("\nFiltered Employees:")

    for employee in employees:

        print(employee)


def fetch_all_employees(cursor):

    cursor.execute("""
        SELECT id, name, email, department, salary
        FROM employees
        ORDER BY id
    """)

    employees = cursor.fetchall()

    print("\nAll Employees:")

    for employee in employees:

        print(employee)


def update_employee(cursor, connection):

    query = """
        UPDATE employees
        SET salary = %s,
            department = %s
        WHERE email = %s
    """

    values = (
        70000.00,
        "Technology",
        "john@example.com"
    )

    cursor.execute(query, values)

    connection.commit()

    print("\nEmployee updated!")
    print("Rows affected:", cursor.rowcount)


def delete_employee(cursor, connection):

    query = """
        DELETE FROM employees
        WHERE email = %s
    """

    cursor.execute(
        query,
        ("emma@example.com",)
    )

    connection.commit()

    print("\nEmployee deleted!")
    print("Rows affected:", cursor.rowcount)


def search_employee(cursor):

    query = """
        SELECT id, name, email, department, salary
        FROM employees
        WHERE department = %s
    """

    cursor.execute(query, ("IT",))

    employees = cursor.fetchall()

    print("\nIT Department Employees:")

    for employee in employees:

        print(employee)


def run_crud_operations():

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        # CREATE
        insert_single_employee(cursor, connection)

        insert_multiple_employees(cursor, connection)

        # READ
        fetch_one_employee(cursor)

        fetch_multiple_employees(cursor)

        fetch_all_employees(cursor)

        search_employee(cursor)

        # UPDATE
        update_employee(cursor, connection)

        # DELETE
        delete_employee(cursor, connection)

        print("\nCRUD operations completed!")

    except Error as error:

        if connection is not None and connection.is_connected():
            connection.rollback()

        print("Database Error:", error)

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        print("Database connection closed.")


if __name__ == "__main__":
    run_crud_operations()

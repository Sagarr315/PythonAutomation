
from mysql.connector import Error

from Database_Automation.database.connection import (
    get_database_connection
)


# --------------------------------------------------
# 1. SETUP ADDITIONAL TABLES
# --------------------------------------------------

def setup_tables(cursor, connection):

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            department_name VARCHAR(100) UNIQUE NOT NULL
        )
    """)

    departments = [
        ("IT",),
        ("HR",),
        ("Finance",),
        ("Marketing",),
        ("Technology",)
    ]

    cursor.executemany("""
        INSERT IGNORE INTO departments (department_name)
        VALUES (%s)
    """, departments)

    connection.commit()

    print("\nDepartment table ready!")


# --------------------------------------------------
# 2. WHERE CONDITIONS AND FILTERING
# --------------------------------------------------

def where_filter(cursor):

    query = """
        SELECT id, name, department, salary
        FROM employees
        WHERE salary >= %s
    """

    cursor.execute(query, (45000,))

    print("\n--- WHERE FILTER ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 3. ORDER BY AND SORTING
# --------------------------------------------------

def order_by_sorting(cursor):

    query = """
        SELECT id, name, department, salary
        FROM employees
        ORDER BY salary DESC
    """

    cursor.execute(query)

    print("\n--- SALARY SORTING ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 4. GROUP BY AND HAVING
# --------------------------------------------------

def group_by_having(cursor):

    query = """
        SELECT
            department,
            COUNT(*) AS total_employees,
            AVG(salary) AS average_salary
        FROM employees
        GROUP BY department
        HAVING COUNT(*) >= %s
    """

    cursor.execute(query, (1,))

    print("\n--- GROUP BY AND HAVING ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 5. AGGREGATE FUNCTIONS
# --------------------------------------------------

def aggregate_functions(cursor):

    query = """
        SELECT
            COUNT(*) AS total_employees,
            SUM(salary) AS total_salary,
            AVG(salary) AS average_salary,
            MIN(salary) AS minimum_salary,
            MAX(salary) AS maximum_salary
        FROM employees
    """

    cursor.execute(query)

    result = cursor.fetchone()

    print("\n--- AGGREGATE RESULTS ---")
    print(result)


# --------------------------------------------------
# 6. INNER JOIN
# --------------------------------------------------

def inner_join(cursor):

    query = """
        SELECT
            e.id,
            e.name,
            d.department_name,
            e.salary
        FROM employees e
        INNER JOIN departments d
        ON e.department = d.department_name
    """

    cursor.execute(query)

    print("\n--- INNER JOIN ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 7. LEFT JOIN
# --------------------------------------------------

def left_join(cursor):

    query = """
        SELECT
            d.department_name,
            e.name,
            e.salary
        FROM departments d
        LEFT JOIN employees e
        ON d.department_name = e.department
    """

    cursor.execute(query)

    print("\n--- LEFT JOIN ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 8. RIGHT JOIN
# --------------------------------------------------

def right_join(cursor):

    query = """
        SELECT
            e.name,
            d.department_name
        FROM employees e
        RIGHT JOIN departments d
        ON e.department = d.department_name
    """

    cursor.execute(query)

    print("\n--- RIGHT JOIN ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 9. SUBQUERY
# --------------------------------------------------

def subquery_example(cursor):

    query = """
        SELECT id, name, salary
        FROM employees
        WHERE salary > (
            SELECT AVG(salary)
            FROM employees
        )
    """

    cursor.execute(query)

    print("\n--- ABOVE AVERAGE SALARY ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 10. PAGINATION
# --------------------------------------------------

def pagination(cursor):

    page_number = 1
    page_size = 2

    offset = (page_number - 1) * page_size

    query = """
        SELECT id, name, department, salary
        FROM employees
        ORDER BY id
        LIMIT %s OFFSET %s
    """

    cursor.execute(query, (page_size, offset))

    print("\n--- PAGINATION ---")
    print("Page:", page_number)
    print("Records per page:", page_size)

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 11. DYNAMIC QUERY BUILDING
# --------------------------------------------------

def dynamic_query(cursor):

    department = "IT"
    minimum_salary = 45000

    # Only allow predefined column names
    allowed_sort_columns = {
        "name": "name",
        "salary": "salary",
        "department": "department"
    }

    sort_by = "salary"
    sort_order = "DESC"

    if sort_by not in allowed_sort_columns:
        raise ValueError("Invalid sorting column")

    if sort_order not in ("ASC", "DESC"):
        raise ValueError("Invalid sorting order")

    query = """
        SELECT id, name, department, salary
        FROM employees
        WHERE department = %s
        AND salary >= %s
    """

    query += (
        f" ORDER BY {allowed_sort_columns[sort_by]} "
        f"{sort_order}"
    )

    cursor.execute(
        query,
        (department, minimum_salary)
    )

    print("\n--- DYNAMIC QUERY ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 12. CREATE AND USE VIEW
# --------------------------------------------------

def create_and_use_view(cursor, connection):

    cursor.execute("""
        CREATE OR REPLACE VIEW employee_salary_summary AS
        SELECT
            department,
            COUNT(*) AS total_employees,
            AVG(salary) AS average_salary
        FROM employees
        GROUP BY department
    """)

    connection.commit()

    cursor.execute("""
        SELECT * FROM employee_salary_summary
    """)

    print("\n--- DATABASE VIEW ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 13. STORED PROCEDURE
# --------------------------------------------------

def stored_procedure(cursor, connection):

    cursor.execute("""
        DROP PROCEDURE IF EXISTS GetEmployeesByDepartment
    """)

    procedure_query = """
        CREATE PROCEDURE GetEmployeesByDepartment(
            IN dept_name VARCHAR(100)
        )
        BEGIN
            SELECT id, name, department, salary
            FROM employees
            WHERE department = dept_name;
        END
    """

    cursor.execute(procedure_query)

    connection.commit()

    # Execute stored procedure
    cursor.callproc(
        "GetEmployeesByDepartment",
        ("IT",)
    )

    print("\n--- STORED PROCEDURE ---")

    for result in cursor.stored_results():

        for row in result.fetchall():
            print(row)


# --------------------------------------------------
# 14. MAIN EXECUTION
# --------------------------------------------------

def run_advanced_sql():

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        print("MySQL Connected Successfully!")

        setup_tables(cursor, connection)

        where_filter(cursor)

        order_by_sorting(cursor)

        group_by_having(cursor)

        aggregate_functions(cursor)

        inner_join(cursor)

        left_join(cursor)

        right_join(cursor)

        subquery_example(cursor)

        pagination(cursor)

        dynamic_query(cursor)

        create_and_use_view(cursor, connection)

        stored_procedure(cursor, connection)

        print("\nAdvanced SQL Automation Completed!")

    except Error as error:

        if connection is not None and connection.is_connected():
            connection.rollback()

        print("Database Error:", error)

    except Exception as error:

        print("Execution Error:", error)

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        print("Database Connection Closed!")


if __name__ == "__main__":
    run_advanced_sql()

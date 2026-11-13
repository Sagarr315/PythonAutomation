
from mysql.connector import Error

from Database_Automation.database.connection import (
    get_database_connection
)


# --------------------------------------------------
# 1. CREATE DEMONSTRATION TABLE
# --------------------------------------------------

def setup_table(cursor, connection):

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_performance_demo (

            id INT AUTO_INCREMENT PRIMARY KEY,

            name VARCHAR(100) NOT NULL,

            email VARCHAR(150) UNIQUE NOT NULL,

            department VARCHAR(100),

            salary DECIMAL(10, 2),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    connection.commit()

    print("Performance demonstration table ready!")


# --------------------------------------------------
# 2. BULK INSERT WITH PARAMETERIZED QUERIES
# --------------------------------------------------

def bulk_insert(cursor, connection):

    records = [
        ("User 1", "perf1@example.com", "IT", 55000),
        ("User 2", "perf2@example.com", "HR", 45000),
        ("User 3", "perf3@example.com", "Finance", 60000),
        ("User 4", "perf4@example.com", "IT", 65000),
        ("User 5", "perf5@example.com", "Marketing", 50000)
    ]

    try:

        cursor.executemany("""
            INSERT INTO security_performance_demo
            (name, email, department, salary)

            VALUES (%s, %s, %s, %s)

            ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            department = VALUES(department),
            salary = VALUES(salary)
        """, records)

        connection.commit()

        print("\nBulk insertion completed!")
        print("Affected rows:", cursor.rowcount)

    except Error as error:

        connection.rollback()

        print("Bulk insertion error:", error)


# --------------------------------------------------
# 3. SQL INJECTION PREVENTION
# --------------------------------------------------

def secure_search(cursor):

    user_input = "' OR 1=1 --"

    query = """
        SELECT id, name, email
        FROM security_performance_demo
        WHERE email = %s
    """

    cursor.execute(query, (user_input,))

    results = cursor.fetchall()

    print("\n--- SECURE SEARCH ---")

    print("Input:", user_input)

    print("Matching records:", len(results))

    print("The input was treated as data, not SQL code.")


# --------------------------------------------------
# 4. SAFE DYNAMIC QUERY
# --------------------------------------------------

def dynamic_sort(cursor):

    sort_column = "salary"

    sort_order = "DESC"

    allowed_columns = {
        "name": "name",
        "salary": "salary",
        "department": "department"
    }

    if sort_column not in allowed_columns:
        raise ValueError("Invalid sorting column")

    if sort_order not in ("ASC", "DESC"):
        raise ValueError("Invalid sorting order")

    query = f"""
        SELECT id, name, department, salary
        FROM security_performance_demo
        ORDER BY {allowed_columns[sort_column]} {sort_order}
    """

    cursor.execute(query)

    print("\n--- DYNAMIC SORT ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 5. CHECK DATABASE USER PERMISSIONS
# --------------------------------------------------

def inspect_permissions(cursor):

    cursor.execute("SELECT CURRENT_USER()")

    print("\nCurrent MySQL User:", cursor.fetchone()[0])

    cursor.execute("SHOW GRANTS")

    print("\n--- DATABASE PERMISSIONS ---")

    for grant in cursor.fetchall():
        print(grant[0])


# --------------------------------------------------
# 6. CREATE INDEX
# --------------------------------------------------

def create_index(cursor, connection):

    cursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.statistics
        WHERE table_schema = DATABASE()
        AND table_name = 'security_performance_demo'
        AND index_name = 'idx_perf_department_salary'
    """)

    exists = cursor.fetchone()[0]

    if not exists:

        cursor.execute("""
            CREATE INDEX idx_perf_department_salary
            ON security_performance_demo (department, salary)
        """)

        connection.commit()

        print("\nIndex created!")

    else:

        print("\nIndex already exists!")


# --------------------------------------------------
# 7. QUERY OPTIMIZATION USING EXPLAIN
# --------------------------------------------------

def explain_query(cursor):

    query = """
        EXPLAIN
        SELECT id, name, salary
        FROM security_performance_demo
        WHERE department = %s
        ORDER BY salary DESC
    """

    cursor.execute(query, ("IT",))

    print("\n--- QUERY EXECUTION PLAN ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 8. LARGE DATASET PROCESSING
# --------------------------------------------------

def fetch_in_batches(cursor):

    cursor.execute("""
        SELECT id, name, department, salary
        FROM security_performance_demo
        ORDER BY id
    """)

    batch_size = 2

    total_records = 0

    print("\n--- BATCH PROCESSING ---")

    while True:

        records = cursor.fetchmany(batch_size)

        if not records:
            break

        total_records += len(records)

        print("Processing batch:")

        for record in records:
            print(record)

    print("Total records processed:", total_records)


# --------------------------------------------------
# 9. DATABASE PERFORMANCE MONITORING
# --------------------------------------------------

def monitor_database(cursor):

    cursor.execute("""
        SELECT
            table_name,
            table_rows,
            data_length,
            index_length
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
    """)

    print("\n--- DATABASE TABLE STATISTICS ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 10. MAIN EXECUTION
# --------------------------------------------------

def run_module():

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        print("Database connected!")

        setup_table(cursor, connection)

        bulk_insert(cursor, connection)

        secure_search(cursor)

        dynamic_sort(cursor)

        inspect_permissions(cursor)

        create_index(cursor, connection)

        explain_query(cursor)

        fetch_in_batches(cursor)

        monitor_database(cursor)

        print("\nModule 7 completed!")

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

        print("Database connection closed!")


if __name__ == "__main__":
    run_module()


from mysql.connector import Error, IntegrityError

from Database_Automation.database.connection import (
    get_database_connection
)


# --------------------------------------------------
# 1. CREATE DEMONSTRATION TABLES
# --------------------------------------------------

def setup_tables(cursor, connection):

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_accounts (
            id INT PRIMARY KEY,
            account_name VARCHAR(100) NOT NULL,
            balance DECIMAL(12, 2) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_transfers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            from_account INT NOT NULL,
            to_account INT NOT NULL,
            amount DECIMAL(12, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bulk_demo_records (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            department VARCHAR(100),
            status VARCHAR(30) DEFAULT 'Pending'
        )
    """)

    # Reset only our demonstration accounts
    cursor.executemany("""
        INSERT INTO automation_accounts
        (id, account_name, balance)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        account_name = VALUES(account_name),
        balance = VALUES(balance)
    """, [
        (1, "Account A", 10000.00),
        (2, "Account B", 5000.00)
    ])

    connection.commit()

    print("Demonstration tables are ready!")


# --------------------------------------------------
# 2. TRANSACTION: COMMIT
# --------------------------------------------------

def transfer_money(cursor, connection):

    try:

        connection.start_transaction()

        amount = 1000.00

        cursor.execute("""
            UPDATE automation_accounts
            SET balance = balance - %s
            WHERE id = %s AND balance >= %s
        """, (amount, 1, amount))

        if cursor.rowcount != 1:
            raise ValueError("Insufficient balance or account not found")

        cursor.execute("""
            UPDATE automation_accounts
            SET balance = balance + %s
            WHERE id = %s
        """, (amount, 2))

        if cursor.rowcount != 1:
            raise ValueError("Destination account not found")

        cursor.execute("""
            INSERT INTO automation_transfers
            (from_account, to_account, amount)
            VALUES (%s, %s, %s)
        """, (1, 2, amount))

        connection.commit()

        print("\nMoney transfer completed!")
        print("Transferred amount:", amount)

    except Exception as error:

        connection.rollback()

        print("Transfer failed. Transaction rolled back:", error)


# --------------------------------------------------
# 3. TRANSACTION: ROLLBACK DEMONSTRATION
# --------------------------------------------------

def rollback_demo(cursor, connection):

    try:

        connection.start_transaction()

        cursor.execute("""
            UPDATE automation_accounts
            SET balance = balance - %s
            WHERE id = %s
        """, (500, 1))

        print("\nTemporary balance change performed.")

        # Deliberately rollback the change
        connection.rollback()

        print("Rollback completed. Change was not saved.")

    except Error as error:

        connection.rollback()

        print("Rollback demonstration error:", error)


# --------------------------------------------------
# 4. BULK INSERT
# --------------------------------------------------

def bulk_insert(cursor, connection):

    records = [
        ("Sample User 1", "bulk1@example.com", "IT"),
        ("Sample User 2", "bulk2@example.com", "HR"),
        ("Sample User 3", "bulk3@example.com", "Finance"),
        ("Sample User 4", "bulk4@example.com", "Marketing")
    ]

    try:

        cursor.executemany("""
            INSERT INTO bulk_demo_records
            (name, email, department)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            department = VALUES(department)
        """, records)

        connection.commit()

        print("\nBulk insert completed!")
        print("Affected rows:", cursor.rowcount)

    except Error as error:

        connection.rollback()

        print("Bulk insert error:", error)


# --------------------------------------------------
# 5. BULK UPDATE
# --------------------------------------------------

def bulk_update(cursor, connection):

    updates = [
        ("Completed", "bulk1@example.com"),
        ("Completed", "bulk2@example.com"),
        ("Processing", "bulk3@example.com"),
        ("Pending", "bulk4@example.com")
    ]

    try:

        cursor.executemany("""
            UPDATE bulk_demo_records
            SET status = %s
            WHERE email = %s
        """, updates)

        connection.commit()

        print("\nBulk update completed!")
        print("Affected rows:", cursor.rowcount)

    except Error as error:

        connection.rollback()

        print("Bulk update error:", error)


# --------------------------------------------------
# 6. DUPLICATE RECORD HANDLING
# --------------------------------------------------

def duplicate_handling(cursor, connection):

    try:

        cursor.execute("""
            INSERT IGNORE INTO bulk_demo_records
            (name, email, department)
            VALUES (%s, %s, %s)
        """, (
            "Duplicate Test",
            "bulk1@example.com",
            "IT"
        ))

        connection.commit()

        if cursor.rowcount == 0:
            print("\nDuplicate email detected. Record skipped.")
        else:
            print("\nNew record inserted.")

    except IntegrityError as error:

        connection.rollback()

        print("Integrity error:", error)


# --------------------------------------------------
# 7. ERROR HANDLING DEMONSTRATION
# --------------------------------------------------

def error_handling(cursor):

    try:

        cursor.execute("""
            SELECT * FROM unknown_demo_table
        """)

    except Error as error:

        print("\nDatabase error handled successfully:")
        print(error)


# --------------------------------------------------
# 8. DISPLAY DATABASE RECORDS
# --------------------------------------------------

def display_records(cursor):

    cursor.execute("""
        SELECT * FROM bulk_demo_records
        ORDER BY id
    """)

    print("\n--- BULK DEMO RECORDS ---")

    for record in cursor.fetchall():
        print(record)

    cursor.execute("""
        SELECT id, account_name, balance
        FROM automation_accounts
        ORDER BY id
    """)

    print("\n--- ACCOUNT BALANCES ---")

    for account in cursor.fetchall():
        print(account)


# --------------------------------------------------
# 9. MAIN EXECUTION
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

        setup_tables(cursor, connection)

        transfer_money(cursor, connection)

        rollback_demo(cursor, connection)

        bulk_insert(cursor, connection)

        bulk_update(cursor, connection)

        duplicate_handling(cursor, connection)

        error_handling(cursor)

        display_records(cursor)

        print("\nModule 4 completed!")

    except Error as error:

        if connection is not None and connection.is_connected():
            connection.rollback()

        print("Database execution error:", error)

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        print("Database connection closed!")


if __name__ == "__main__":
    run_module()

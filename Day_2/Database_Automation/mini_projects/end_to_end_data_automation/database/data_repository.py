
import logging

from decimal import Decimal, InvalidOperation
from mysql.connector import Error

from Database_Automation.database.connection import (
    get_database_connection
)


logger = logging.getLogger(__name__)


# --------------------------------------------------
# 1. CREATE ALL INTEGRATION TABLES
# --------------------------------------------------

def create_tables(cursor, connection):

    # API products
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS integration_products (

            id INT AUTO_INCREMENT PRIMARY KEY,

            external_id INT NOT NULL UNIQUE,

            title VARCHAR(255) NOT NULL,

            category VARCHAR(100),

            brand VARCHAR(150),

            price DECIMAL(12, 2),

            stock INT,

            rating DECIMAL(5, 2),

            source VARCHAR(50),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP

        )
    """)

    # Scraped books
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS integration_books (

            id INT AUTO_INCREMENT PRIMARY KEY,

            title VARCHAR(255) NOT NULL UNIQUE,

            price DECIMAL(10, 2),

            currency VARCHAR(10),

            rating VARCHAR(30),

            availability VARCHAR(100),

            product_url VARCHAR(500),

            source VARCHAR(50),

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP

        )
    """)

    # CSV and Excel employee records
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS integration_employees (

            id INT AUTO_INCREMENT PRIMARY KEY,

            name VARCHAR(150) NOT NULL,

            email VARCHAR(150) NOT NULL,

            department VARCHAR(100),

            salary DECIMAL(12, 2),

            source_file VARCHAR(30) NOT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ON UPDATE CURRENT_TIMESTAMP,

            UNIQUE KEY unique_employee_source (email, source_file)

        )
    """)

    connection.commit()

    print("All integration database tables created or verified!")

    logger.info("All integration tables created or verified")


# --------------------------------------------------
# 2. VALIDATE API PRODUCT DATA
# --------------------------------------------------

def validate_product(product):

    external_id = product.get("external_id")
    title = product.get("title")
    price = product.get("price")

    if not isinstance(external_id, int) or isinstance(external_id, bool):
        return None

    if external_id <= 0:
        return None

    if not isinstance(title, str) or not title.strip():
        return None

    try:

        price = Decimal(str(price))

        if not price.is_finite() or price < 0:
            return None

    except (InvalidOperation, TypeError, ValueError):
        return None

    stock = product.get("stock")

    if stock is not None:

        if not isinstance(stock, int) or isinstance(stock, bool):
            return None

        if stock < 0:
            return None

    rating = product.get("rating")

    if rating is not None:

        try:

            rating = Decimal(str(rating))

            if not rating.is_finite() or rating < 0:
                return None

        except (InvalidOperation, TypeError, ValueError):
            return None

    return (
        external_id,
        title.strip(),
        product.get("category"),
        product.get("brand"),
        price,
        stock,
        rating,
        product.get("source", "DummyJSON")
    )


# --------------------------------------------------
# 3. INSERT OR UPDATE API PRODUCTS
# --------------------------------------------------

def save_products(cursor, connection, products):

    if not products:

        print("No API products available.")

        return 0

    records = []

    for product in products:

        cleaned = validate_product(product)

        if cleaned is not None:

            records.append(cleaned)

        else:

            logger.warning("Invalid API product skipped.")

    if not records:

        print("No valid API products to save.")

        return 0

    query = """
        INSERT INTO integration_products
        (
            external_id,
            title,
            category,
            brand,
            price,
            stock,
            rating,
            source
        )

        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE

        title = VALUES(title),
        category = VALUES(category),
        brand = VALUES(brand),
        price = VALUES(price),
        stock = VALUES(stock),
        rating = VALUES(rating),
        source = VALUES(source)
    """

    try:

        cursor.executemany(query, records)

        connection.commit()

        print("\nAPI products saved successfully!")

        print("Records processed:", len(records))

        logger.info(
            "Processed %s API products",
            len(records)
        )

        return len(records)

    except Error:

        connection.rollback()

        logger.exception("Failed to save API products.")

        raise


# --------------------------------------------------
# 4. VALIDATE SCRAPED BOOK DATA
# --------------------------------------------------

def validate_book(book):

    title = book.get("title")

    if not isinstance(title, str) or not title.strip():
        return None

    try:

        price = Decimal(str(book.get("price")))

        if not price.is_finite() or price < 0:
            return None

    except (InvalidOperation, TypeError, ValueError):
        return None

    return (
        title.strip(),
        price,
        book.get("currency", "GBP"),
        book.get("rating", "Unknown"),
        book.get("availability", "Unknown"),
        book.get("product_url"),
        book.get("source", "BooksToScrape")
    )


# --------------------------------------------------
# 5. INSERT OR UPDATE SCRAPED BOOKS
# --------------------------------------------------

def save_books(cursor, connection, books):

    if not books:

        print("No scraped books available.")

        return 0

    records = []

    for book in books:

        cleaned = validate_book(book)

        if cleaned is not None:

            records.append(cleaned)

        else:

            logger.warning("Invalid scraped book skipped.")

    if not records:

        print("No valid books to save.")

        return 0

    query = """
        INSERT INTO integration_books
        (
            title,
            price,
            currency,
            rating,
            availability,
            product_url,
            source
        )

        VALUES (%s, %s, %s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE

        price = VALUES(price),
        currency = VALUES(currency),
        rating = VALUES(rating),
        availability = VALUES(availability),
        product_url = VALUES(product_url),
        source = VALUES(source)
    """

    try:

        cursor.executemany(query, records)

        connection.commit()

        print("\nScraped books saved successfully!")

        print("Records processed:", len(records))

        logger.info(
            "Processed %s scraped books",
            len(records)
        )

        return len(records)

    except Error:

        connection.rollback()

        logger.exception("Failed to save scraped books.")

        raise


# --------------------------------------------------
# 6. SAVE CSV AND EXCEL EMPLOYEES TO MYSQL
# --------------------------------------------------

def save_employee_records(cursor, connection, records, source):

    if source not in ("CSV", "Excel"):

        raise ValueError("Source must be CSV or Excel.")

    if not records:

        print(f"No employee records available from {source}.")

        return 0

    query = """
        INSERT INTO integration_employees
        (
            name,
            email,
            department,
            salary,
            source_file
        )

        VALUES (%s, %s, %s, %s, %s)

        ON DUPLICATE KEY UPDATE

        name = VALUES(name),
        department = VALUES(department),
        salary = VALUES(salary)
    """

    values = []

    for record in records:

        name = str(record.get("name") or "").strip()

        email = str(record.get("email") or "").strip().lower()

        department = str(
            record.get("department") or ""
        ).strip()

        try:

            salary = Decimal(str(record.get("salary")))

        except (InvalidOperation, TypeError, ValueError):

            logger.warning("Invalid employee salary skipped.")

            continue

        if not name or not email or "@" not in email:
            continue

        if not department or not salary.is_finite() or salary < 0:
            continue

        values.append((
            name,
            email,
            department,
            salary,
            source
        ))

    if not values:

        print(f"No valid employee records from {source}.")

        return 0

    try:

        cursor.executemany(query, values)

        connection.commit()

        print(f"\n{source} employee records saved to MySQL!")

        print("Records processed:", len(values))

        logger.info(
            "Processed %s employee records from %s",
            len(values),
            source
        )

        return len(values)

    except Error:

        connection.rollback()

        logger.exception(
            "Failed to save %s employee records",
            source
        )

        raise


# --------------------------------------------------
# 7. FETCH ALL API PRODUCTS
# --------------------------------------------------

def get_all_products(cursor):

    cursor.execute("""
        SELECT
            external_id,
            title,
            category,
            brand,
            price,
            stock,
            rating,
            source

        FROM integration_products

        ORDER BY external_id
    """)

    return cursor.fetchall()


# --------------------------------------------------
# 8. FETCH ALL SCRAPED BOOKS
# --------------------------------------------------

def get_all_books(cursor):

    cursor.execute("""
        SELECT
            title,
            price,
            currency,
            rating,
            availability,
            product_url,
            source

        FROM integration_books

        ORDER BY title
    """)

    return cursor.fetchall()


# --------------------------------------------------
# 9. FETCH ALL EMPLOYEE RECORDS
# --------------------------------------------------

def get_all_employees(cursor):

    cursor.execute("""
        SELECT
            name,
            email,
            department,
            salary,
            source_file

        FROM integration_employees

        ORDER BY source_file, email
    """)

    rows = cursor.fetchall()

    return [
        {
            "name": row[0],
            "email": row[1],
            "department": row[2],
            "salary": Decimal(str(row[3])),
            "source_file": row[4]
        }
        for row in rows
    ]


# --------------------------------------------------
# 10. DISPLAY DATABASE SUMMARY
# --------------------------------------------------

def display_database_summary(cursor):

    tables = [
        "integration_products",
        "integration_books",
        "integration_employees"
    ]

    print("\n--- DATABASE SUMMARY ---")

    for table in tables:

        cursor.execute(
            f"SELECT COUNT(*) FROM `{table}`"
        )

        count = cursor.fetchone()[0]

        print(f"{table}: {count} records")


# --------------------------------------------------
# 11. MAIN DATABASE TEST
# --------------------------------------------------

def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s"
    )

    connection = None
    cursor = None

    try:

        print("Connecting to MySQL...")

        connection = get_database_connection()

        if connection is None:

            print("Database connection failed.")

            return

        print("MySQL connected successfully!")

        cursor = connection.cursor()

        create_tables(cursor, connection)

        display_database_summary(cursor)

        print("\nExisting API products:", len(get_all_products(cursor)))

        print("Existing scraped books:", len(get_all_books(cursor)))

        print("Existing employee records:", len(get_all_employees(cursor)))

        print("\nDatabase repository test completed!")

    except Error as error:

        if connection is not None and connection.is_connected():
            connection.rollback()

        print("Database error:", error)

        logger.exception("Database repository test failed.")

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        print("Database connection closed!")


if __name__ == "__main__":
    main()

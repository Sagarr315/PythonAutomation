
import logging

from mysql.connector import Error

from Database_Automation.database.connection import (
    get_database_connection
)

from Database_Automation.mini_projects.end_to_end_data_automation.api.api_extractor import (
    fetch_all_products
)

from Database_Automation.mini_projects.end_to_end_data_automation.scraping.web_scraper import (
    scrape_books
)

from Database_Automation.mini_projects.end_to_end_data_automation.database.data_repository import (
    create_tables,
    save_products,
    save_books,
    save_employee_records,
    get_all_products,
    get_all_books,
    get_all_employees,
    display_database_summary
)

from Database_Automation.mini_projects.end_to_end_data_automation.files.csv_handler import (
    create_sample_csv,
    read_csv_records,
    export_csv_records
)

from Database_Automation.mini_projects.end_to_end_data_automation.files.excel_handler import (
    create_sample_excel,
    read_excel_records,
    export_excel_report
)

from Database_Automation.mini_projects.end_to_end_data_automation.config import (
    LOG_DIR
)


# --------------------------------------------------
# 1. LOGGING CONFIGURATION
# --------------------------------------------------

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 2. EXTRACT API DATA
# --------------------------------------------------

def extract_api_data():

    print("\n========== API EXTRACTION ==========")

    try:

        products = fetch_all_products(page_size=10)

        print("API products extracted:", len(products))

        return products

    except Exception as error:

        logger.exception("API extraction failed.")

        print("API extraction failed:", error)

        return []


# --------------------------------------------------
# 3. EXTRACT WEBSITE DATA
# --------------------------------------------------

def extract_website_data():

    print("\n========== WEB SCRAPING ==========")

    try:

        books = scrape_books(max_pages=3)

        print("Books extracted:", len(books))

        return books

    except Exception as error:

        logger.exception("Web scraping failed.")

        print("Web scraping failed:", error)

        return []


# --------------------------------------------------
# 4. EXTRACT CSV DATA
# --------------------------------------------------

def extract_csv_data():

    print("\n========== CSV EXTRACTION ==========")

    try:

        create_sample_csv()

        records = read_csv_records()

        print("CSV employee records:", len(records))

        return records

    except Exception as error:

        logger.exception("CSV extraction failed.")

        print("CSV extraction failed:", error)

        return []


# --------------------------------------------------
# 5. EXTRACT EXCEL DATA
# --------------------------------------------------

def extract_excel_data():

    print("\n========== EXCEL EXTRACTION ==========")

    try:

        create_sample_excel()

        records = read_excel_records()

        print("Excel employee records:", len(records))

        return records

    except Exception as error:

        logger.exception("Excel extraction failed.")

        print("Excel extraction failed:", error)

        return []


# --------------------------------------------------
# 6. LOAD ALL SOURCE DATA INTO MYSQL
# --------------------------------------------------

def load_data_into_mysql(
    connection,
    cursor,
    products,
    books,
    csv_records,
    excel_records
):

    print("\n========== MYSQL DATA LOADING ==========")

    create_tables(cursor, connection)

    save_products(
        cursor,
        connection,
        products
    )

    save_books(
        cursor,
        connection,
        books
    )

    save_employee_records(
        cursor,
        connection,
        csv_records,
        "CSV"
    )

    save_employee_records(
        cursor,
        connection,
        excel_records,
        "Excel"
    )

    print("\nAll available source records processed.")


# --------------------------------------------------
# 7. EXPORT MYSQL EMPLOYEE DATA TO CSV AND EXCEL
# --------------------------------------------------

def export_database_reports(cursor):

    print("\n========== DATABASE REPORT EXPORT ==========")

    employees = get_all_employees(cursor)

    print("Employee records retrieved from MySQL:", len(employees))

    # CSV report
    export_csv_records(employees)

    # Excel report with multiple worksheets
    export_excel_report(employees)

    print("\nDatabase reports generated successfully!")


# --------------------------------------------------
# 8. DISPLAY FINAL SUMMARY
# --------------------------------------------------

def display_final_summary(cursor):

    print("\n========== FINAL DATABASE SUMMARY ==========")

    products = get_all_products(cursor)

    books = get_all_books(cursor)

    employees = get_all_employees(cursor)

    print("API products in MySQL:", len(products))

    print("Scraped books in MySQL:", len(books))

    print("Employee records in MySQL:", len(employees))

    display_database_summary(cursor)


# --------------------------------------------------
# 9. RUN COMPLETE AUTOMATION PIPELINE
# --------------------------------------------------

def run_pipeline():

    connection = None
    cursor = None

    print("\n========================================")
    print("   END-TO-END DATA AUTOMATION PIPELINE")
    print("========================================")

    try:

        # STEP 1: Extract API data
        products = extract_api_data()

        # STEP 2: Scrape website data
        books = extract_website_data()

        # STEP 3: Read CSV data
        csv_records = extract_csv_data()

        # STEP 4: Read Excel data
        excel_records = extract_excel_data()

        # STEP 5: Connect to MySQL
        print("\n========== DATABASE CONNECTION ==========")

        connection = get_database_connection()

        if connection is None:

            raise RuntimeError(
                "Unable to connect to MySQL database."
            )

        cursor = connection.cursor()

        print("MySQL connected successfully!")

        # STEP 6: Store extracted data in MySQL
        load_data_into_mysql(
            connection,
            cursor,
            products,
            books,
            csv_records,
            excel_records
        )

        # STEP 7: Retrieve MySQL data and generate reports
        export_database_reports(cursor)

        # STEP 8: Display final database summary
        display_final_summary(cursor)

        print("\n========================================")
        print("   PIPELINE EXECUTION COMPLETED")
        print("========================================")

        logger.info("Integration pipeline completed successfully.")

    except (Error, RuntimeError) as error:

        if connection is not None and connection.is_connected():
            connection.rollback()

        print("\nPipeline database error:", error)

        logger.exception("Pipeline execution failed.")

    except Exception as error:

        if connection is not None and connection.is_connected():
            connection.rollback()

        print("\nPipeline execution error:", error)

        logger.exception("Unexpected pipeline failure.")

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        print("\nDatabase connection closed!")


# --------------------------------------------------
# 10. APPLICATION ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":

    run_pipeline()


import logging
import shutil
import subprocess
import tempfile

from datetime import datetime
from pathlib import Path

from mysql.connector import Error

from Database_Automation.config.settings import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)

from Database_Automation.database.connection import (
    get_database_connection
)


# --------------------------------------------------
# 1. PROJECT PATHS AND LOGGING
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

BACKUP_DIR = PROJECT_ROOT / "backups"

LOG_DIR = PROJECT_ROOT / "logs"

BACKUP_DIR.mkdir(parents=True, exist_ok=True)

LOG_DIR.mkdir(parents=True, exist_ok=True)

BACKUP_FILE = (
    BACKUP_DIR /
    f"{DB_NAME}_{datetime.now():%Y%m%d_%H%M%S}.sql"
)

logging.basicConfig(
    filename=LOG_DIR / "database_automation.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# 2. CREATE AUTOMATION TABLES
# --------------------------------------------------

def setup_automation_tables(cursor, connection):

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_audit_logs (

            id INT AUTO_INCREMENT PRIMARY KEY,

            action_name VARCHAR(100),

            description TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_sync_checkpoint (

            id INT PRIMARY KEY,

            last_sync DATETIME(6) NOT NULL

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_source_records (

            id INT AUTO_INCREMENT PRIMARY KEY,

            record_name VARCHAR(100),

            record_value VARCHAR(255),

            updated_at DATETIME(6)
                DEFAULT CURRENT_TIMESTAMP(6)
                ON UPDATE CURRENT_TIMESTAMP(6)

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_sync_records (

            id INT PRIMARY KEY,

            record_name VARCHAR(100),

            record_value VARCHAR(255),

            source_updated_at DATETIME(6)

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_cleanup_demo (

            id INT AUTO_INCREMENT PRIMARY KEY,

            record_name VARCHAR(100),

            created_at DATETIME

        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_schema_versions (

            id INT AUTO_INCREMENT PRIMARY KEY,

            version_number INT UNIQUE,

            description VARCHAR(255),

            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    # Initialize incremental synchronization checkpoint
    cursor.execute("""
        INSERT IGNORE INTO automation_sync_checkpoint
        (id, last_sync)
        VALUES (1, '2000-01-01 00:00:00.000000')
    """)

    # Insert sample source records only once
    cursor.executemany("""
        INSERT IGNORE INTO automation_source_records
        (id, record_name, record_value)
        VALUES (%s, %s, %s)
    """, [
        (1, "Source Record 1", "Value A"),
        (2, "Source Record 2", "Value B"),
        (3, "Source Record 3", "Value C")
    ])

    # Add demonstration cleanup records only once
    cursor.execute("""
        SELECT COUNT(*)
        FROM automation_cleanup_demo
    """)

    if cursor.fetchone()[0] == 0:

        cursor.execute("""
            INSERT INTO automation_cleanup_demo
            (record_name, created_at)
            VALUES
            ('Old Demo Record', DATE_SUB(NOW(), INTERVAL 120 DAY)),
            ('Recent Demo Record', NOW())
        """)

    connection.commit()

    print("Automation tables are ready!")


# --------------------------------------------------
# 3. AUDIT LOGGING
# --------------------------------------------------

def write_audit_log(cursor, connection, action, description):

    cursor.execute("""
        INSERT INTO automation_audit_logs
        (action_name, description)
        VALUES (%s, %s)
    """, (action, description))

    connection.commit()

    logger.info("%s: %s", action, description)


def display_audit_logs(cursor):

    cursor.execute("""
        SELECT id, action_name, description, created_at
        FROM automation_audit_logs
        ORDER BY id DESC
        LIMIT 10
    """)

    print("\n--- RECENT AUDIT LOGS ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 4. DATABASE HEALTH MONITORING
# --------------------------------------------------

def monitor_database(cursor):

    cursor.execute("SELECT VERSION(), DATABASE(), NOW()")

    version, database, current_time = cursor.fetchone()

    print("\n--- DATABASE HEALTH ---")

    print("MySQL Version:", version)

    print("Database:", database)

    print("Server Time:", current_time)

    cursor.execute("""
        SELECT
            COUNT(*),
            COALESCE(SUM(data_length + index_length), 0)
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
    """)

    table_count, database_size = cursor.fetchone()

    print("Number of Tables:", table_count)

    print("Database Size:", database_size, "bytes")

    cursor.execute("""
        SHOW GLOBAL STATUS LIKE 'Threads_connected'
    """)

    print("Connected Threads:", cursor.fetchone())


# --------------------------------------------------
# 5. TABLE STATISTICS
# --------------------------------------------------

def table_statistics(cursor):

    cursor.execute("""
        SELECT
            table_name,
            table_rows,
            data_length,
            index_length
        FROM information_schema.tables
        WHERE table_schema = DATABASE()
        ORDER BY table_name
    """)

    print("\n--- TABLE STATISTICS ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 6. INCREMENTAL DATA LOADING
# --------------------------------------------------

def incremental_data_loading(cursor, connection):

    cursor.execute("""
        SELECT last_sync
        FROM automation_sync_checkpoint
        WHERE id = 1
    """)

    last_sync = cursor.fetchone()[0]

    cursor.execute("""
        SELECT id, record_name, record_value, updated_at
        FROM automation_source_records
        WHERE updated_at > %s
        ORDER BY updated_at, id
    """, (last_sync,))

    records = cursor.fetchall()

    if not records:

        print("\nNo new or modified source records.")

        return

    latest_timestamp = max(
        record[3] for record in records
    )

    try:

        for record in records:

            cursor.execute("""
                INSERT INTO automation_sync_records
                (id, record_name, record_value, source_updated_at)

                VALUES (%s, %s, %s, %s)

                ON DUPLICATE KEY UPDATE

                record_name = VALUES(record_name),
                record_value = VALUES(record_value),
                source_updated_at = VALUES(source_updated_at)
            """, record)

        cursor.execute("""
            UPDATE automation_sync_checkpoint
            SET last_sync = %s
            WHERE id = 1
        """, (latest_timestamp,))

        connection.commit()

        print("\nIncremental synchronization completed!")

        print("Records processed:", len(records))

        write_audit_log(
            cursor,
            connection,
            "INCREMENTAL_SYNC",
            f"Processed {len(records)} source records"
        )

    except Error:

        connection.rollback()

        raise


# --------------------------------------------------
# 7. VERIFY SYNCHRONIZED DATA
# --------------------------------------------------

def display_synchronized_data(cursor):

    cursor.execute("""
        SELECT
            id,
            record_name,
            record_value,
            source_updated_at
        FROM automation_sync_records
        ORDER BY id
    """)

    print("\n--- SYNCHRONIZED RECORDS ---")

    for row in cursor.fetchall():
        print(row)


# --------------------------------------------------
# 8. AUTOMATED DATABASE CLEANUP
# --------------------------------------------------

def cleanup_old_records(cursor, connection):

    cursor.execute("""
        DELETE FROM automation_cleanup_demo
        WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY)
    """)

    deleted_records = cursor.rowcount

    connection.commit()

    print("\nDatabase cleanup completed!")

    print("Old demo records deleted:", deleted_records)

    write_audit_log(
        cursor,
        connection,
        "DATABASE_CLEANUP",
        f"Deleted {deleted_records} expired demo records"
    )


# --------------------------------------------------
# 9. DATABASE SCHEMA VERSION TRACKING
# --------------------------------------------------

def apply_schema_version(cursor, connection):

    cursor.execute("""
        SELECT version_number
        FROM automation_schema_versions
        WHERE version_number = 1
    """)

    existing = cursor.fetchone()

    if existing is None:

        cursor.execute("""
            INSERT INTO automation_schema_versions
            (version_number, description)
            VALUES (%s, %s)
        """, (
            1,
            "Initial database automation schema"
        ))

        connection.commit()

        print("\nSchema version 1 recorded!")

        write_audit_log(
            cursor,
            connection,
            "SCHEMA_VERSION",
            "Applied initial schema version 1"
        )

    else:

        print("\nSchema version 1 already exists!")


# --------------------------------------------------
# 10. MYSQL CLIENT CONFIGURATION
# --------------------------------------------------

def create_mysql_client_config():

    temporary_file = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".cnf",
        prefix="mysql_automation_",
        encoding="utf-8",
        delete=False
    )

    # Escape special characters in MySQL option values
    safe_password = (
        DB_PASSWORD
        .replace("\\", "\\\\")
        .replace('"', '\\"')
    )

    safe_user = DB_USER.replace("\\", "\\\\").replace('"', '\\"')

    safe_host = DB_HOST.replace("\\", "\\\\").replace('"', '\\"')

    temporary_file.write("[client]\n")
    temporary_file.write(f'user="{safe_user}"\n')
    temporary_file.write(f'password="{safe_password}"\n')
    temporary_file.write(f'host="{safe_host}"\n')
    temporary_file.write(f"port={DB_PORT}\n")

    temporary_file.close()

    return Path(temporary_file.name)


# --------------------------------------------------
# 11. AUTOMATED DATABASE BACKUP
# --------------------------------------------------

def backup_database():

    mysqldump = shutil.which("mysqldump")

    if mysqldump is None:

        print(
            "\nmysqldump not found in PATH. "
            "Configure the MySQL bin directory to enable backup."
        )

        return

    config_file = create_mysql_client_config()

    try:

        command = [
            mysqldump,
            f"--defaults-extra-file={config_file}",
            "--databases",
            DB_NAME,
            f"--result-file={BACKUP_FILE}"
        ]

        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=300
        )

        print("\nDatabase backup completed!")

        print("Backup file:", BACKUP_FILE)

        logger.info("Database backup created: %s", BACKUP_FILE)

    except subprocess.CalledProcessError as error:

        print("Backup failed:", error.stderr)

    except subprocess.TimeoutExpired:

        print("Database backup timed out.")

    finally:

        config_file.unlink(missing_ok=True)


# --------------------------------------------------
# 12. DATABASE RESTORE
# --------------------------------------------------

def restore_database(backup_file):

    mysql_client = shutil.which("mysql")

    backup_path = Path(backup_file)

    if mysql_client is None:

        print("MySQL command-line client not found.")

        return

    if not backup_path.is_file():

        print("Backup file does not exist:", backup_path)

        return

    # Restore can overwrite existing database objects.
    # Only call this function after confirming the backup
    # and target database are correct.

    config_file = create_mysql_client_config()

    try:

        command = [
            mysql_client,
            f"--defaults-extra-file={config_file}",
            DB_NAME
        ]

        with open(backup_path, "rb") as backup:

            subprocess.run(
                command,
                stdin=backup,
                check=True,
                capture_output=True,
                timeout=300
            )

        print("Database restore completed!")

        logger.info("Database restored from: %s", backup_path)

    except subprocess.CalledProcessError as error:

        print("Restore failed:", error.stderr)

    except subprocess.TimeoutExpired:

        print("Database restore timed out.")

    finally:

        config_file.unlink(missing_ok=True)


# --------------------------------------------------
# 13. MAIN EXECUTION
# --------------------------------------------------

def run_automation():

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            return

        cursor = connection.cursor()

        print("Database connected!")

        setup_automation_tables(cursor, connection)

        monitor_database(cursor)

        table_statistics(cursor)

        incremental_data_loading(cursor, connection)

        display_synchronized_data(cursor)

        cleanup_old_records(cursor, connection)

        apply_schema_version(cursor, connection)

        display_audit_logs(cursor)

        backup_database()

        print("\nAdvanced Database Automation completed!")

        logger.info("Database automation run completed.")

    except Error as error:

        if connection is not None and connection.is_connected():
            connection.rollback()

        print("MySQL Error:", error)

        logger.exception("MySQL execution error")

    except Exception as error:

        print("Automation Error:", error)

        logger.exception("Automation execution error")

    finally:

        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

        print("Database connection closed!")


if __name__ == "__main__":
    run_automation()

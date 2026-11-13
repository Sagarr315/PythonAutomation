import mysql.connector

from mysql.connector import Error

from Database_Automation.config.settings import (
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME
)


def get_server_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            connection_timeout=10
        )

        return connection

    except Error as error:

        print("MySQL Connection Error:", error)

        return None


def get_database_connection():

    try:

        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            connection_timeout=10
        )

        return connection

    except Error as error:

        print("Database Connection Error:", error)

        return None
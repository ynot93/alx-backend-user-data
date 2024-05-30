#!/usr/bin/env python3
"""
This module deals with personal data in backend development

"""
import os
import re
import logging
from typing import Sequence
import mysql.connector
from mysql.connector import connection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: Sequence,
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated

    """
    pattern = re.compile(f"({'|'.join(fields)})=.*?{separator}")
    return pattern.sub(
        lambda m: f"{m.group(1)}={redaction}{separator}", message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class

    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Sequence):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.msg = filter_datum(self.fields,
                                  self.REDACTION,
                                  record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    Creates and configures the logger

    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    s_handler = logging.StreamHandler()
    s_formatter = RedactingFormatter(PII_FIELDS)
    s_handler.setFormatter(s_formatter)

    logger.addHandler(s_handler)
    return logger


def get_db() -> connection.MySQLConnection:
    """
    Returns a connector to the database

    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME'),
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD'),
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db_connector = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return db_connector


def main() -> None:
    """
    Obtain db connection and display data

    """
    logger = get_logger()
    db_conn = get_db()
    cursor = db_conn.cursor
    cursor.execute('SELECT * from users;')
    rows = cursor.fetchall()

    columns = [col[0] for col in cursor.description]
    for row in rows:
        row_data = dict(zip(columns, row))
        log_message = "; ".join(
            [f"{key}={value}" for key, value in row_data.items()]) + ";"
        logger.info(log_message)

    cursor.close()
    db_conn.close()


if __name__ == '__main__':
    main()

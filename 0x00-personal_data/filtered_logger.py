#!/usr/bin/env python3
"""
This module deals with personal data in backend development

"""
import re
import logging
from typing import Sequence, Mapping, Dict


def filter_datum(fields: Sequence, redaction: str, message: str, separator: str) -> str:
    """
    Returns the log message obfuscated

    """
    pattern = re.compile(f"({'|'.join(fields)})=.*?{separator}")

    def substitute(match: str) -> str:
        """
        Substitute match with obfuscation text

        """
        return f"{match.group(1)}={redaction}{separator}"

    return pattern.sub(substitute, message)


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
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        
        return super(RedactingFormatter, self).format(record)

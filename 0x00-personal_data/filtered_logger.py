#!/usr/bin/env python3
"""
This module deals with personal data in backend development

"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated

    """
    pattern = re.compile(f"({'|'.join(fields)})=.*?{separator}")

    def substitute(match):
        """
        Substitute match with obfuscation text

        """
        return f"{match.group(1)}={redaction}{separator}"

    return pattern.sub(substitute, message)

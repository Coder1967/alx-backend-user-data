#!/usr/bin/env python3
"""
filterd logger module
"""
import re
from typing import Tuple, List
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields


    def format(self, record: logging.LogRecord) -> str:
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION,
                                message, self.SEPARATOR)
        return redacted
        

def assist_filter(fields: List[str], redaction: str,
                  separator: str) -> Tuple:
    """
    assists filter_datum function
    """
    patterns = [r"(?P<field>{})=[^{}]*".format(field,
                separator)for field in fields]
    replace = ["{}={}".format(field, redaction) for field in fields]
    return patterns, replace


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    patterns, repl = assist_filter(fields, redaction, separator)
    for i in range(len(fields)):
        message = re.sub(patterns[i], repl[i], message)
    return message

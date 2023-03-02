#!/usr/bin/env python3
"""
filterd logger module
"""
import re
from typing import Tuple

def assist_filter(fields, redaction, separator)->Tuple:
    """
    assists filter_datum function
    """
    patterns = [r"(?P<field>{})=[^{}]*".format(field, separator) for field in fields]
    replace = ["{}={}".format(field, redaction) for field in fields]
    return patterns, replace


def filter_datum(fields, redaction,
        message, separator)->str:
    """ returns the log message obfuscated"""
    patterns, repl = assist_filter(fields, redaction, separator)
    for i in range(len(fields)):
        message = re.sub(patterns[i], repl[i], message)
    return message

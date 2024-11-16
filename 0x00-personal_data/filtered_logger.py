#!/usr/bin/env python3
"""
    filtered_logger.py
    Module that filters a log file
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
        Returns the log message obfuscated
        Args:
            - fields: a list of strings representing all fields to obfuscate
            - redaction: a string representing by what the field will be obfuscated
            - message: a string representing the log line
            - separator: a string representing by which character is separating all fields in the log line
    """
    for field in fields:
        message = re.sub(
            r'(?<={}=)[^{}]*'.format(field, separator),
            redaction, message)
    return message

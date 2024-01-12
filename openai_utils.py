"""
Author: Imtiaz Rahi <imtiaz.rahi@gmail.com>
Created on: 2024-01-10

Copyright (c) 2024 UhuruTek Solutions
License: MIT
"""

import random
import re
import string
from datetime import datetime


def show_json(obj):
    """Show (print) JSON dump on screen (STDOUT)"""
    print(obj.model_dump_json(indent=2))


def datetime_str():
    """Return datetime as string; e.g. 20240111-015113"""
    now = datetime.now()
    dt = re.sub(r'[-:]', '', str(now)).replace(" ", "-").split('.')[0]
    return dt


def generate_random_string(length: int) -> str:
    """Generate random string of particular length"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def bytes_to_human_readable(size_in_bytes):
    """Convert bytes count into human-readable Byte, KB, MB etc"""
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    index = 0
    while size_in_bytes >= 1024 and index < len(units) - 1:
        size_in_bytes /= 1024
        index += 1
    return f"{size_in_bytes:.2f} {units[index]}"  # Format with 2 decimal places


def str_to_bool(s):
    """Convert a string representation of truth to true (1), otherwise false (0)"""
    return str(s).lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup']

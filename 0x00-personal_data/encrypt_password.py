#!/usr/bin/env python3
"""

"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Returns a hashed password
    """
    byt = password.encode()
    hashed = bcrypt.hashpw(byt, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checks if a password is valid
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

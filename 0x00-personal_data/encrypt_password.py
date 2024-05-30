#!/usr/bin/env python3
"""
This module encrypts passwords with bcrypt

"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Uses bcrypt to hash password

    """
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates matching passwords

    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

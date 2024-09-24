#!/usr/bin/env python3
"""
    module: to create auth
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
        Generate a password hash
    """
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10))

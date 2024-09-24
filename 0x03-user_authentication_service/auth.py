#!/usr/bin/env python3
"""
    module: to create auth
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


def _hash_password(password: str) -> bytes:
    """
        Generate a password hash
    """
    return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(10))


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a User
        """
        try:
            user = self._db.find_user_by(**{"email": email})
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        # create the user
        hashed_password = _hash_password(password)
        user = self._db.add_user(email, hashed_password)
        return user

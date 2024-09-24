#!/usr/bin/env python3
"""
    module: to create auth
"""
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid


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

    def valid_login(self, email: str, password: str) -> bool:
        """
            valid login
        """
        try:
            user = self._db.find_user_by(**{"email": email})

        except NoResultFound:
            return False
        else:
            if bcrypt.checkpw(
                    password.encode('utf8'), user.hashed_password):
                return True
            else:
                return False

    def _generate_uuid(self) -> str:
        """
            Generate uuids
        """
        return str(uuid.uuid4())

    def create_session(self, email: str):
        """
            create a session id
        """

        try:
            user = self._db.find_user_by(**{"email": email})

        except NoResultFound:
            pass

        else:
            session_id = self._generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return session_id

    def get_user_from_session_id(self, session_id):
        """
            Find user by session id
        """
        try:
            user = self._db.find_user_by(**{"session_id": session_id})

        except NoResultFound:
            return None

        else:
            return User

    def destroy_session(self, user_id):
        """
            destroy session
        """
        try:
            user = self._db.find_user_by(**{"session_id": session_id})

        except NoResultFound:
            pass

        user.session_id = None
        self._db._session.commit()

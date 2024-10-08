#!/usr/bin/env python3
""" session_auth.py: Implements Session Authentication """
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """ Represents a session authentication """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creates session_id for a user """
        if not user_id:
            return None
        if not isinstance(user_id, str):
            return None

        # generate session id
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns a User ID based on a Session ID """
        if not session_id:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Logout the user and deletes the user session """
        if not request:
            return False
        session_id = request.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        del SessionAuth.user_id_by_session_id[session_id]
        return True

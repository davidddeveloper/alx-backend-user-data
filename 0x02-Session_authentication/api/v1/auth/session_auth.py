#!/usr/bin/env python3
""" session_auth.py: Implements Session Authentication """
from api.v1.auth.auth import Auth
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
        session_id = uuid.uuid4()
        user_id_by_session_id[session_id] = user_id
        return session_id

#!/usr/bin/env python3
"""
    template for all authentication system
"""
from typing import List
from typing import TypeVar
import os


class Auth:
    """
        Represent authentication system
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ true if path not in excluded_paths """
        if not path:
            return True
        if not excluded_paths or excluded_paths == []:
            return True
        for excluded_path in excluded_paths:
            if path in excluded_path:
                return False
            if excluded_path.endswith('*'):
                if excluded_path[:-1] in path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ validates all request """
        if not request:
            return None

        auth_header = request.headers.get('Authorization')
        if auth_header:
            return auth_header
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return the current user """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie value from a request """
        if not request:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME'))

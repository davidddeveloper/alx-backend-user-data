#!/usr/bin/env python3
"""
    template for all authentication system
"""
from typing import List
from typing import TypeVar


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
        return True

    def authorization_header(self, request=None) -> str:
        """ validates all request """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """ return the current user """
        return None

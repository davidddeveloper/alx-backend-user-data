#!/usr/bin/env python3
""" basic_auth.py: creates basic authentication """
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ Representas a basic authentication """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns Base64 part of the Authorization header
        otherwise None
        """
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64 string """
        if not base64_authorization_header:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            data = base64.b64decode(
                    base64_authorization_header)
            return data.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """ returns the user email and password
        from the Base64 decoded value """
        if not decoded_base64_authorization_header:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        return tuple(decoded_base64_authorization_header.split(':'))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """ returns the User instance
        based on his email and password """
        if not user_email:
            return None
        if not user_pwd:
            return None

        try:
            query_users_result = User.search({"email": user_email})
        except Exception:
            return None

        if query_users_result == []:
            return None

        for user in query_users_result:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        if auth_header:
            base64_auth_header = self.extract_base64_authorization_header(
                    auth_header)
            if base64_auth_header:
                decoded_data = self.decode_base64_authorization_header(
                        base64_auth_header)
                if decoded_data:
                    user_credential = self.extract_user_credentials(
                            decoded_data)
                    email = user_credential[0]
                    pwd = user_credential[1]
                    if email and pwd:
                        return self.user_object_from_credentials(
                                email, pwd)
        return None

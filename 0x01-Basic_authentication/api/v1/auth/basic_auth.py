#!/usr/bin/env python3
""" basic_auth.py: creates basic authentication """
from api.v1.auth.auth import Auth
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

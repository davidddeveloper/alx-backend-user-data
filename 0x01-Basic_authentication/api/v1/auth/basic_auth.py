#!/usr/bin/env python3
""" basic_auth.py: creates basic authentication """
from api.v1.auth.auth import Auth


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

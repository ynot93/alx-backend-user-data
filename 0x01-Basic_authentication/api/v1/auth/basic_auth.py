#!/usr/bin/env python3
"""
This module deals with basic authentication

"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    Base class for authentication

    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header

        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 part of the Authorization header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode the Base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Convert bytes to a UTF-8 string
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

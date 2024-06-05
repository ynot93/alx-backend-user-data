#!/usr/bin/env python3
"""
This module deals with basic authentication.
"""

import base64
from typing import Optional, Tuple
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class for handling Basic Authentication.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        """
        Extracts the Base64 part of the Authorization header.

        Args:
            authorization_header (str): The authorization header.

        Returns:
            Optional[str]: The Base64 part of the authorization header, or None if invalid.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> Optional[str]:
        """
        Decodes the Base64 part of the Authorization header.

        Args:
            base64_authorization_header (str): The Base64 authorization header.

        Returns:
            Optional[str]: The decoded value of the Base64 string, or None if invalid.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Extracts the user email and password from the decoded authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded authorization header.

        Returns:
            Tuple[Optional[str], Optional[str]]: A tuple containing the user email and password, or (None, None) if invalid.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(':', 1)
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[User]:
        """
        Returns the User instance based on their credentials.

        Args:
            user_email (str): The user email.
            user_pwd (str): The user password.

        Returns:
            Optional[User]: The User instance, or None if invalid credentials.
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        user = User.search(user_email)
        if user is None:
            return None

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> Optional[User]:
        """
        Retrieves the User instance for a request.

        Args:
            request: The request object.

        Returns:
            Optional[User]: The User instance, or None if authentication fails.
        """
        if request is None:
            return None

        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        base64_authorization_header = self.extract_base64_authorization_header(authorization_header)
        if base64_authorization_header is None:
            return None

        decoded_base64_auth_header = self.decode_base64_authorization_header(base64_authorization_header)
        if decoded_base64_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_base64_auth_header)
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)

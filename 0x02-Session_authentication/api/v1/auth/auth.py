#!/usr/bin/env python3
"""
This module deals with user authentication

"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """
    Defines methods used during authentication

    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if path requires authentication

        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        if not path.endswith("/"):
            path += "/"
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif excluded_path == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Reurns the authorization content from header

        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user from request header

        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Retrieve the value of the session cookie from a request.

        """
        if request is None:
            return None

        session_cookie_name = os.getenv('SESSION_NAME')

        return request.cookies.get(session_cookie_name)

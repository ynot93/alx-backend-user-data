#!/usr/bin/env python3
"""
This module deals with user authentication

"""
from flask import request
from typing import List, TypeVar


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
        if excluded_paths is None or not excluded_paths:
            return True
        if not path.endswith("/"):
            path += "/"
        for  excluded_path in excluded_paths:
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

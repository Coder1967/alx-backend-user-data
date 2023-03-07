#!/usr/bin/env python3
from flask import request
from typing import List, TypeVar
"""
handles user authentication
"""


class Auth:
    """
    class to handle authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        returns: True if path not in excluded path
        returns: False other wise
        """
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path is None:
            return True
        if path not in excluded_paths and path + '/' not in excluded_paths:
            return True
        return False

    def authorization_header(self, request=None) -> str:
        """
        change later
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        change later
        """

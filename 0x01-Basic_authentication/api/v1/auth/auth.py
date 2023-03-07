#!/usr/bin/env python3
"""
handles user authentication
"""
from flask import request
from typing import List, TypeVar


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
        If request is None, returns None If request doesn’t 
        contain the header key Authorization, returns None Otherwise,
        return the value of the header request Authorization
        """
        if request is None:
            return None
        if "Authorization" in request.headers:
            return request.headers["Authorization"]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        change later
        """

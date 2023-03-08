#!/usr/bin/env python3
"""
implements basic auth
"""
import base64
from typing import TypeVar
import binascii
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    class to handle basic auth of api
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        extracts the base 64 string from the header
        """
        extract = []

        if authorization_header is None:
            return None
        if type(authorization_header).__name__ != "str":
            return None
        extract = authorization_header.split(" ")
        if len(extract) > 1:
            if extract[0] == "Basic":
                return extract[1]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        decodes the base64 encoded string
        """
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header).__name__ != 'str':
            return None
        try:
            return base64.b64decode(base64_authorization_header).decode("utf")
        except binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        extracts user credentials from a string with format;
        email:password
        """
        values = []

        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header).__name__ != 'str':
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        values = decoded_base64_authorization_header.split(":")
        if len(values) > 1:
            return values[0], values[1]
        return None, None

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """
        searches out a user
        return: user obj if found otherwise None is returned
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance based on a received request
        """
        Auth_header = self.authorization_header(request)
        if Auth_header is not None:
            token = self.extract_base64_authorization_header(Auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pword = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pword)
        return

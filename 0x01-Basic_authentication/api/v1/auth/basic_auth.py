#!/usr/bin/env python3
"""
implements basic auth
"""
import base64
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

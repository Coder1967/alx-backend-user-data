#!/usr/bin/env python3
"""
implements session auth
"""
from models.user import User
from uuid import uuid4
from typing import TypeVar
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    handles implementation of the session auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a new session id
        """
        if user_id is None or type(user_id).__name__ != "str":
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        that returns a User ID based on a Session ID
        """
        if session_id is None or type(session_id).__name__ != "str":
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        returns a user making the request
        """
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        destroys the session
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if (request is None or session_id is None) or user_id is None:
            return False
        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True

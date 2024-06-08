#!/usr/bin/env python3
"""
This module authenticates with session IDs stored in the db

"""

from datetime import datetime, timedelta
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Handles session authentication with db storage

    """

    def create_session(self, user_id=None):
        """
        Create a session ID and store it in the database.

        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve a user ID based on a session ID from the database.

        """
        if session_id is None:
            return None

        if not isinstance(session_id, UserSession):
            return None

        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return None

        user_session = user_sessions[0]

        if user_session.created_at + timedelta(seconds=self.session_duration) \
                < datetime.now():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """
        Destroy a session based on the session ID from the request cookie.

        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_sessions = UserSession.search({"session_id": session_id})
        if not user_sessions:
            return False

        user_session = user_sessions[0]
        user_session.remove()
        return True

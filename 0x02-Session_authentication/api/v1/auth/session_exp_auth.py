#!/usr/bin/env python3
"""
Module for Session Authentication with expiration

"""

from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for handling Session Authentication with expiration

    """

    def __init__(self):
        """
        Initialize the SessionExpAuth class

        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session ID with an expiration for a given user_id

        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve a user_id based on a session_id with expiration check

        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration) < \
                datetime.now():
            return None

        return session_dict.get('user_id')

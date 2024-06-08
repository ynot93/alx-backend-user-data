#!/usr/bin/env python3
"""
User Session module for handling user sessions stored in a file

"""

from models.base import Base


class UserSession(Base):
    """
    UserSession class to handle user sessions

    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize the UserSession class

        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')

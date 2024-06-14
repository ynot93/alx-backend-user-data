#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create and store a new user
        """
        user = User(email=email, hashed_password=hashed_password)
        self.session.add(user)
        self.session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Return a filtered user
        """
        session = self.session
        try:
            filtered_user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the provided criteria.")
        except InvalidRequestError:
            raise InvalidRequestError(
                "Invalid request with the provided criteria.")
        return filtered_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes
        """
        session = self.session
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        session.commit()

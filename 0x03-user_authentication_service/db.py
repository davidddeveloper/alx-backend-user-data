#!/usr/bin/env python3
"""module represent a sqlalchemy to mysql database
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from user import Base
from user import User
import bcrypt


class DB:
    """ Represent a database
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
            Add a user to db
        """
        # create a user model
        user = User(email=email, hashed_password=hashed_password)
        # add user model to session and save to db
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """
            Finds a user
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
            Update a user model
        """

        try:
            user = self.find_user_by(**{"id": user_id})
        except NoResultFound:
            return None

        except Exception:
            raise ValueError(
                "You passed values that does not equal to user attribute")

        else:
            for key, val in kwargs.items():
                if key not in user.__dict__:
                    raise ValueError(
                        'Existing attributes not found in user')
                setattr(user, key, val)

        self._session.commit()

        return None

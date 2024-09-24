#!/usr/bin/env python3
"""
    create a SQLAlchemy model named User
    for a database table named users
"""
from sqlalchemy.orm.declarative_base import Base
from sqlalchemy import Column, String, Integer


class User(Base):
    """ Represent a User model
        User -> users
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(



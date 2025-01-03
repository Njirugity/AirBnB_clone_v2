#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, String
from models.place import Place
from models.review import Review

class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    reviews = relationship(
            'Review',
            backref='user',
            cascade='all, delete,delete-orphan'
            )
#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import models
from models.city import City
import shlex
class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    name = Column(String(128), nullable=False)
    cities = relationship(
        'City', cascade='all, delete, delete-orphan', backref='state'
    )

    @property
    def cities(self):
        var = models.storage.all()
        my_list = []
        result = []
        for key in var:
            city = key.replace('.', ' ')
            city = shlex.split(city)
            if (city[0] == 'City'):
                my_list.append(var[key])
        for elem in my_list:
            if (elem.state_id == self.id):
                result.append(elem)
        return (result)

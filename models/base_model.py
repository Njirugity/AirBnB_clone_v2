#!/usr/bin/python3
from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
import uuid
import os

Base = declarative_base()


class BaseModel:
    """ Base model with common fields for all classes """

    id = Column(String(60), primary_key=True, default=str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    setattr(
                            self, key, datetime.fromisoformat(value)
                            if value else None
                            )
                else:
                    setattr(self, key, value)
        if not getattr(self, 'id', None):
            self.id = str(uuid.uuid4())

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance"""
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = self.__class__.__name__
        obj_dict['created_at'] = (
                self.created_at.isoformat() if self.created_at else None
                )
        obj_dict['updated_at'] = (
                self.updated_at.isoformat() if self.updated_at else None
                )
        obj_dict.pop('_sa_instance_state', None)
        return obj_dict

    def save(self):
        """Save to database"""
        storage_type = os.environ.get('HBNB_TYPE_STORAGE', 'db')
        if storage_type == "db":
            from models import storage
            self.updated_at = datetime.utcnow()
            storage.new(self)
            storage.save()
        else:
            pass

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
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key != 'created_at' and key != 'updated_at':
                    setattr(self, key, value)
        else:
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

        if not self.id:
            self.id = str(uuid.uuid4())
        else:
            self.updated_at = datetime.utcnow()

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

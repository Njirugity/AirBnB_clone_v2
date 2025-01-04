#!/usr/bin/python3
""" new class for sqlAlchemy """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ create tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        new_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            obj = self.__session.query(cls).all
            for i in obj:
                key = f"{cls.__name}.{i.id}"
                new_dict[key] = i

        else:
            classes = [User, State, City, Amenity, Place, Review]
            for j in classes:
                obj = self.__session.query(i).all()
                for i in obj:
                    key = f"{cls.__name}.{i.id}"
                    new_dict[key] = i

        return (new_dict)
    
    def new(self, obj):
        """add a new element in the table
        """

        self.__session.add(obj)

    def save(self):
        """save changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete an element"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """configuration"""
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session)

    def close(self):
        """ calls remove()
        """
        self.__session.close()
    
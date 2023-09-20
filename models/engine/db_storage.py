#!/usr/bin/python3
""" class dbstorage """

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage():
    """
    MySQL database
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        DBStorage object
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Returns dictionary with all objects
        """
        if cls:
            objs = self.__session.query(classes[cls])
        else:
            objs = self.__session.query(State).all()
            objs += self.__session.query(City).all()
            objs += self.__session.query(User).all()
            objs += self.__session.query(Place).all()
            objs += self.__session.query(Amenity).all()
            objs += self.__session.query(Review).all()

        a_dict = {}
        for obj in objs:
            k = '{}.{}'.format(type(obj).__name__, obj.id)
            a_dict[k] = obj
        return a_dict

    def new(self, obj):
        """
        adds the object
        """
        self.__session.add(obj)

    def save(self):
        """
        commits all changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        deletes from the current database
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        reloads data
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """
        call method
        """
        self.__session.remove()

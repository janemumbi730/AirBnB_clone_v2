#!/usr/bin/python3
'''change your storage engine and use SQLAlchemy'''


from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

import models
"""This module defines a class to manage sqlachemy for hbnb clone"""


class DBStorage():
    '''Database storage'''
    __engine = None
    __session = None

    def __init__(self):
        '''Getting attributes for the create engine Url'''
        user = getenv('HBNB_MYSQL_USER')
        pas = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                user, pas, host, db), pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)
            # engine specify database connection where operations are perfomed

    def all(self, cls=None):
        '''Retrieve all objects or individual class objects'''

        my_classes = [User, State, City, Amenity, Place, Review]
        dictionary = {}
        if cls is not None:
            for value in self.__session.query(cls).all():
                key = '{}.{}'.format(value.__class__.__name__, value.id)
                dictionary[key] = value
        else:
            for clas in my_classes:
                for value in self.__session.query(clas).all():
                    key = '{}.{}'.format(value.__class__.__name__, value.id)
                    dictionary[key] = value
        return dictionary

    def new(self, obj):
        '''Add a new object to the database'''
        self.__session.add(obj)

    def save(self):
        '''Implement data persistence'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Delete an entire database'''
        if obj is not None:
            Base.metadata.drop_all(self.__engine)
            # Deleting a database is basically dropping all the tables

    def reload(self):
        '''Retrieves all the data database'''
        Base.metadata.create_all(self.__engine)
        Var_Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Var_Session)
        self.__session = Session()

    def close(self):
        '''Calls remove() on private session attr'''
        self.__session.close()

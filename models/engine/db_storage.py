#!usr/bin/python3
"""Module for the database storage engine for AirBnB project"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """DataBase Storage class that handles create, update,
    read and delete functions
    attributes:
    __engine :binds class to mysql database
    __session : use to perform and track mysql operations
    """
    __engine = None
    __session = None
    __classes = ["City", "State", "User", "Amenity", "Place", "Review"]

    def __init__(self):
        """initialize attributes in the DBStorage class"""
        conn = "mysql+mysqldb://{}:{}@{}/{}".format(getenv("HBNB_MYSQL_USER"),
                                                    getenv("HBNB_MYSQL_PWD"),
                                                    getenv("HBNB_MYSQL_HOST"),
                                                    getenv("HBNB_MYSQL_DB"))
        self.engine = create_engine(conn, pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """return all data in a table about a class or all classes"""
        dic = {}
        if cls:
            query = self.__session.query(cls)
            for col in query.all():
                key = "{}.{}".format(cls.__name__, col.id)
                dic[key] = col
        else:
            for c in self.__classes:
                query = self.__session.query(c)
                for col in query.all():
                    key = "{}.{}".format(cls.__name__, col.id)
                    dic[key] = col
        return dic

    def new(self, obj):
        """add object to current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """save all changes made to the database"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete obj from current database if not none"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database using current session"""
        Base.metadata.create_all(self.__engine)
        session_thread = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        Session = scoped_session(session_thread)
        self.__session = Session()

    def close(self):
        """close current session"""
        self.__session.close()

#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """ The city class, contains state ID and name
     Attributes:
        __tablename__ (str): Name of table
        id (int): state_id which is the primary key
        name (str): Name of state
    """
    __tablename__ = "cities"
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    name = Column(String(128), nullable=False)
    state = relationship('State', back_populates='cities')
    places = relationship(
        'Place',
        back_populates='cities',
        cascade='all, delete-orphan'
        )

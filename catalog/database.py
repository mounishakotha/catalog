import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# creating User class.
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)


# creating cheese country base class.
class Cheese(Base):
    __tablename__ = 'cheese'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id
        }


# creating cheese items base class.
class CheeseItem(Base):
    __tablename__ = 'cheese_item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    cheese_id = Column(Integer, ForeignKey('cheese.id'))
    cheese = relationship(Cheese)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'price': self.price,
         }

engine = create_engine('sqlite:///cheesewithuser.db')

Base.metadata.create_all(engine)

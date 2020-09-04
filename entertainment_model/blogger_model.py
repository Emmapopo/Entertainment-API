from sqlalchemy import *
from sqlalchemy.orm import relationship
from .base import Base


# A User Class to model user details


class Blogger(Base):
    __tablename__ = 'blogger'
    id = Column('id', Integer, primary_key=True)
    user_name = Column('user_name', String(50), nullable=True)
    surname = Column('surname', String(50), nullable=True)
    first_name = Column('first_name', String(50), nullable=True)
    email = Column('email', String(50), nullable=True, unique=True)
    password = Column('password', String(300), nullable=True)

    def __init__(self, user_name=None, surname=None, first_name=None, email=None, password=None):
        self.user_name = user_name
        self.surname = surname
        self.first_name = first_name
        self.email = email
        self.password = password

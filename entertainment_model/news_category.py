from sqlalchemy import *
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.dialects import mysql


class NewsCategory(Base):
    __tablename__ = 'news_category'
    id = Column('id', Integer, primary_key=True)
    category = Column('category', String(70), nullable=False)

    def __init__(self, category=None):
        self.category = category
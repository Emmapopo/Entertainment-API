from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
import datetime
from .blogger_model import Blogger
from .base import Base
from .news_category import NewsCategory


class News(Base):
    __tablename__ = 'news'
    id = Column('id', Integer, primary_key=True)
    blogger_id = Column('blogger_id', Integer, ForeignKey('blogger.id'))
    title = Column ('title', String(500), nullable=False)
    content = Column('content', String(5000), nullable=False)
    category_id = Column('category_id', Integer, ForeignKey('news_category.id'))
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)

    

    def __init__(self, blogger_id=None, title = None, content=None, category_id=None, timestamp=None):
        self.blogger_id = blogger_id
        self.title = title
        self.content = content
        self.category_id = category_id
        self.timestamp = timestamp

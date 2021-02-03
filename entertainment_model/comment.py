from sqlalchemy import *
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.dialects import mysql
import datetime
from user_model.user_model import User
from .news_model import News


class Comment(Base):
    __tablename__ = 'comment'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    news_id = Column('news_id', Integer, ForeignKey('news.id'))
    post = Column('post', String(5000), nullable=False)
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)
  
    def __init__(self, user_id = None, news_id=None, post = None, timestamp=None):
        self.user_id = user_id
        self.news_id = news_id
        self.post = post
        self.timestamp = timestamp
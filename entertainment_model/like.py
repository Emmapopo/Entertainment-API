from sqlalchemy import *
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.dialects import mysql
import datetime
from user_model.user_model import User
from .news_model import News


class Like(Base):
    __tablename__ = 'like'
    id = Column('id', Integer, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    news_id = Column('news_id', Integer, ForeignKey('news.id'))
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id','news_id',),
                      )
  
    def __init__(self, user_id = None, news_id=None, timestamp=None):
        self.user_id = user_id
        self.news_id = news_id
        self.timestamp = timestamp
   
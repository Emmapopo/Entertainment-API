from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import mysql
import datetime
from .blogger_model import Blogger
from .base import Base


class News(Base):
    __tablename__ = 'news'
    id = Column('id', Integer, primary_key=True)
    blogger_id = Column('blogger_id', Integer, ForeignKey('blogger.id'))
    title = Column ('title', String(500), nullable=False)
    content = Column('content', String(5000), nullable=False)
    timestamp = Column(mysql.DATETIME(fsp=6), default=datetime.datetime.utcnow)

    def __init__(self, blogger_id=None, title = None, content=None, timestamp=None):
        self.blogger_id = blogger_id
        self.title = title
        self.content = content
        self.timestamp = timestamp

from sqlalchemy import *
from sqlalchemy.orm import relationship
from .news_model import News
from .base import Base


class FeaturedImage(Base):
    __tablename__ = 'featured_image'
    id = Column('id', Integer, primary_key=True)
    news_id = Column('news_id', Integer, ForeignKey('news.id'))
    image = Column('image', String(2000), nullable=False)
   
    def __init__(self, news_id=None, image=None):
        self.news_id = news_id
        self.image = image

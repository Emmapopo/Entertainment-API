from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from entertainment_model.news_model import News

class NewsController():
    def __init__(self, db):
        self.db = db

    def add_news(self, me):         # Function to add news to the database
        self.db.session.add(me)
        self.db.session.commit()


    def get_news_id (self, blogger_id, ts):
        news_id = self.db.session.query(News.id).filter(and_(News.timestamp==ts,News.blogger_id == blogger_id)).first()[0]
        return news_id

    def get_news (self, news_id):
        try:
            news = self.db.session.query(News).filter_by(id=news_id).one()
            return news
        except:
            return None





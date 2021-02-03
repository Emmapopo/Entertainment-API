from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from entertainment_model.news_model import News
from entertainment_model.featured_image_model import FeaturedImage
from entertainment_model.like import Like
from entertainment_model.comment import Comment
from sqlalchemy import and_
from entertainment_model.news_category import NewsCategory

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
            
    def get_featuredimage(self, news_id):
        try:
            featured_image = self.db.session.query(FeaturedImage).filter_by(news_id=news_id).one()
            return featured_image
        except:
            return None

    def like_news(self, like):         # Function to like a news
        self.db.session.add(like)
        self.db.session.commit()

    def unlike_news(self, user_id, news_id):   # function to unlike a news
        self.db.session.query(Like).filter(and_(Like.user_id == user_id, Like.news_id == news_id)).delete()
        self.db.session.commit()

    def comment_news(self, comment):
        self.db.session.add(comment)
        self.db.session.commit()

    def get_no_likes(self, news_id):

        try:
            no_of_likes = self.db.session.query(Like.id).filter_by(news_id=news_id).count()
            return no_of_likes
        
        except:
            return 0

    def get_no_comments(self, news_id):
        try:
            no_of_comments = self.db.session.query(Comment.id).filter_by(news_id=news_id).count()
            return no_of_comments

        except:
            return 0

    def user_like(self, user_id, news_id): #used to check is a specific user liked a specific news

        try:
            like_id = self.db.session.query(Like.id).filter(and_(Like.user_id == user_id, Like.news_id == news_id)).first()[0]
            return 'yes'

        except:
            return 'no'


    def get_comment(self, id):
        comment = self.db.session.query(Comment).filter_by(id=id).one()
        return comment


    def get_comments (self, news_id):
        comment_ids = self.db.session.query(Comment.id).filter_by(news_id = news_id).all()
        comment_ids = [item for t in comment_ids for item in t]

        comments = {}

        for i in comment_ids:
            comment = self.get_comment(i)
            print(comment)
            comments.update({i:{'comment': comment.post, 'commenter': comment.user_id, 'timestamp': comment.timestamp}})
            
        return comments
        
        
    def get_like(self, id):
        like = self.db.session.query(Like).filter_by(id=id).one()
        return like


    def get_likes (self, news_id):
        like_ids = self.db.session.query(Like.id).filter_by(news_id = news_id).all()
        like_ids = [item for t in like_ids for item in t]

        likes = {}

        for i in like_ids:
            like = self.get_like(i)
            likes.update({i:{'liker':like.user_id, 'timestamp': like.timestamp}})

        return likes


    def get_category(self, id):
        resp = self.db.session.query(NewsCategory).filter_by(id=id).one()
        category = resp.category

        return category


 


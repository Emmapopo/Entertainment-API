from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists

from entertainment_model.blogger_model import Blogger


class BloggerController():
    db = None
    def __init__(self, db):
        self.db = db


    def add_blogger(self, me):         # Function to new blogger to the database
        self.db.session.add(me)
        self.db.session.commit()

    def blogger_user(self, id):        # Function to retrieve a blogger from the database
        resp = self.db.session.query(Blogger).filter_by(id=id).one()
        return resp

    def blogger_name(self,id):
        resp = self.blogger_user(id)
        firstname = resp.first_name
        lastname = resp.surname
        name = firstname + ' ' + lastname
        return name

    def get_password(self, em):    # Function to retrieve the password of a blogger from the database
        password = self.db.session.query(Blogger).with_entities(Blogger.password).filter_by(email=em).first()
        return password

    def get_email(self, em):       # Function to retrieve the email of a blogger from the database
        email = self.db.session.query(Blogger).with_entities(Blogger.email).filter_by(email=em).first()
        return email

    def get_blogger_id(self, em):       # Function to retrieve the email of a blogger from the database
        email = self.db.session.query(Blogger).with_entities(Blogger.id).filter_by(email=em).first()
        return email
        
    def get_user_name(self, em):   # Function to retrieve the blogger name of a user from the database
        username = self.db.session.query(Blogger).with_entities(Blogger.user_name).filter_by(email=em).first()
        return username


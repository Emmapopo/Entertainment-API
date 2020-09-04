from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from entertainment_model.featured_image_model import FeaturedImage

class FeaturedImageController():
    def __init__(self, db):
        self.db = db

    def add_featured_image(self, me):         # Function to add news to the database
        self.db.session.add(me)
        self.db.session.commit()



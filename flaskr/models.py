"""
flaskr/models.py
"""
import os
from datetime import datetime
from flaskr import app, db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.String(30), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    pub_time = db.Column(db.DateTime, default=datetime.now())

    datas = db.relationship('Data', backref='user', lazy=True)

    def __init__(self,id,password,pub_time):
        self.id = id
        self.password = password
        self.pub_time = pub_time
    
    def get_json(self):
        return dict(
            id = self.id,
            password = self.password,
            pub_time = self.pub_time
        )
    
    def __repr__(self):
        return "id : %r, password: %r" %(self.id, self.password)

class Data(db.Model):
    __tablename__ = "data"
    news_id = db.Column(db.Integer, primary_key=True)
    news_title = db.Column(db.String(100), nullable=False)
    news_url = db.Column(db.String(100), nullable=False)
    stored_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    user_id = db.Column(db.String(30), db.ForeignKey('user.id', ondelete='CASCADE'))
    
    def get_json(self):
        return dict(
            news_id = self.news_id,
            news_title = self.news_title,
            news_url = self.news_url,
            stored_time = self.stored_time.strftime("%y/%m/%d %p %H:%M"),
            user_id = self.user_id
        )

    def __repr__(self):
        return "title: %r, url: %r" %(self.news_title, self.news_url)

class SearchedData(db.Model):
    __tablename__="searchedData"
    searched_news_id = db.Column(db.Integer, primary_key=True)
    searched_news_title = db.Column(db.String(100), nullable=False)
    searched_news_url = db.Column(db.String(100), nullable=False)
    searched_news_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def get_json(self):
        return dict(
            searched_news_id = self.searched_news_id,
            searched_news_title = self.searched_news_title,
            searched_news_url = self.searched_news_url,
            searched_news_time = self.searched_news_time
        )
"""
__init__.py
"""
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate       # DB

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@127.0.0.1:3306/testDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'baaa!111/'
app.secret_key = 'baaa!111/'    # session 사용하려면 필요
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flaskr.index import views
from flaskr.auth import views
from flaskr.crawling import views
from flaskr.mypage import views

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from flask_login import UserMixin
from main import db

#Stores user info for login

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))

#Job stores job data for each user

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(150))
    role = db.Column(db.String(150))
    status = db.Column(db.String(50))
    notes = db.Column(db.String(200))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    resume = db.Column(db.String(10000))


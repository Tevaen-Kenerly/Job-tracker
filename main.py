from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db' #Using SQLite
app.config['SECRET_KEY'] = 'your_secret_key' #required for login sessions
app.config['UPLOAD_FOLDER'] = os.path.join('static/uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' #Where to redirect if user is not logged in

from routes import *

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all() #Creates all database tables
    app.run(debug=True)

app=app

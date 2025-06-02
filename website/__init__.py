from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

# Database created
db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    # Initialize Flask and Database
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'UWATERLOO'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # Populates database
    from .models import User, Term, Course
    create_database(app)

    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Succesful")
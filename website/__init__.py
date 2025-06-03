from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import asyncio
from . import script

# Database created
db = SQLAlchemy()
DB_NAME = "database.db"
courses = []

def create_app():
    # Initialize Flask and Database
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'UWATERLOO'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    # Populates database
    from .models import User, Term, Course
    create_database(app)

    with app.app_context():
        c = Course.query.filter_by(id=1).first()
        print(c.title + c.description + c.body)

    return app

def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()

            from .models import Course
            courses = asyncio.run(script.scrape())
            for course in courses:
                new_course = Course(title=course[0], description=course[1], body=course[2])
                db.session.add(new_course)
            db.session.commit()
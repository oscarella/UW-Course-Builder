from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from os import path
import asyncio
from . import script
from flask_login import LoginManager
from website import filters

# Database created
db = SQLAlchemy()
whooshee = Whooshee()
DB_NAME = "database.db"
courses = []

def create_app():
    # Initialize Flask and Database
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'UWATERLOO'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['WHOOSHEE_DIR'] = 'whooshee' # Stores index on server
    app.jinja_env.filters['htmlfy'] = filters.htmlfy
    db.init_app(app)
    whooshee.init_app(app)
    # Register Blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    # Populates database
    from .models import User
    create_database(app)

    from flask_migrate import Migrate
    migrate= Migrate(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    # Tells Flask how we load User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

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
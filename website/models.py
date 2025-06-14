from . import db, whooshee
from flask_login import UserMixin # Module to assist user login

# Association table - User & Course
highlights = db.Table('highlights',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

# Association table - Term & Course
added = db.Table('added',
    db.Column('term_id', db.Integer, db.ForeignKey('term.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
)

class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

    terms = db.relationship('Term')
    courses = db.relationship('Course', secondary=highlights, backref='users')

class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, default="Term")

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    courses = db.relationship('Course', secondary=added, backref='terms')

    def to_dict(self):
        return {"id": self.id, "name": self.name}

@whooshee.register_model('title', 'description')
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, default="No description found.")
    body = db.Column(db.Text, default="No body found.")

    def to_dict(self):
        return {"id": self.id, "title": self.title, "desc": self.description, "body": self.body}
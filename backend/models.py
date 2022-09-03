import os
from dotenv import load_dotenv
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

#ici nous chargons le mot de passe de ma base de donnée dans notre fichier .env
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")
DATABASE_PASSWORD="123456789"
database_name = 'trivia'
database_path = "postgresql://{}:{}@{}/{}".format(
    "postgres", DATABASE_PASSWORD, "localhost:5432", database_name
)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    # print(database_path)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

"""
Question

"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    # category = Column(String)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }

"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    questions = db.relationship('Question', backref='categories', lazy=True)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }
    def format_id(self):
        return '{0}'.format(self.id)
    def format_type(self):
        return '{0}'.format(self.type)
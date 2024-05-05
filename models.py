from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

'''Model for User Registeration'''

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    collections = db.relationship('Collection', backref='user', lazy=True)


'''Model for Collection'''

class Collection(db.Model):
    __tablename__ = "collection"
     
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    username = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    uuid = db.Column(db.String(36), nullable=False, default=lambda: str(uuid.uuid4()))
    movies = db.relationship('Movie', backref='collection', lazy=True, cascade='all, delete-orphan')


'''Model for Movie'''

class Movie(db.Model):
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(455))
    genres = db.Column(db.String(100))
    uuid = db.Column(db.String(50))
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)


'''Model for Counter'''

class RequestCount(db.Model):
    __tablename__ = "counter"
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0) 

from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

'''Model for Collection'''

class Collection(db.Model):
    __tablename__ = "collection"
     
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    username = db.Column(db.Integer, db.ForeignKey('user.username'), nullable=False)
    uuid = db.Column(db.String(36), nullable=False, default=lambda: str(uuid.uuid4()))
    movies = db.relationship('Movie', backref='collection', lazy=True, cascade='all, delete-orphan')
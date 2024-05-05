from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''Model for Movie'''

class Movie(db.Model):
    __tablename__ = "movie"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(455))
    genres = db.Column(db.String(100))
    uuid = db.Column(db.String(50))
    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)
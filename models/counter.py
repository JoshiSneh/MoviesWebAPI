from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''Model for Counter'''

class RequestCount(db.Model):
    __tablename__ = "counter"
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0) 
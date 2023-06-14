"""Define data model."""

from datetime import datetime

from flaskr import db


class User(db.Model):
    """Define users table."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Post(db.Model):
    """Define posts table."""

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    author = db.relationship("User", backref=db.backref("author"))

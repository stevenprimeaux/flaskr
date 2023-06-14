"""Initialize application."""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
if SQLALCHEMY_DATABASE_URI is not None:
    SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)


def create_app(test_config=None):
    """Define application factory."""
    from . import auth, blog

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)

    with app.app_context():
        db.create_all()

    app.add_url_rule("/", endpoint="index")

    return app

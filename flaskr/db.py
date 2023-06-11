"""Manage database."""

import sqlite3
import click

from flask import current_app, g


def get_db():
    """Initialize connection."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """Close database connection."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Initialize database."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """CLI command to initialize database."""
    init_db()
    click.echo("Database has been initialized.")


def init_app(app):
    """Connect application to database."""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

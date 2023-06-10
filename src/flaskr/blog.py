"""Define blog blueprint."""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Fetch blog posts to display on home page."""
    db = get_db()
    posts = db.execute("""
        select p.id, title, body, created, author_id, username
        from post p join user u on p.author_id = u.id
        order by created desc
    """).fetchall()
    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create blog post."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."
        if not body:
            error = "Body is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                """
                insert into post (title, body, author_id)
                values (?, ?, ?)
                """,
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


def get_post(id, check_author=True):
    """Fetch blog post and associated information."""
    post = get_db().execute(
        """
        select p.id, title, body, created, author_id, username
        from post p join user u on p.author_id = u.id
        where p.id = ?
        """,
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exit.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update existing blog post."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."
        if not body:
            error = "Body is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                """
                update post set title = ?, body = ?
                where id = ?
                """,
                (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete blog post."""
    get_post(id)
    db = get_db()
    db.execute("delete from post where id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))

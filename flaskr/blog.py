"""Define blog blueprint."""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr import db
from flaskr.auth import login_required
from flaskr.models import Post

bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Fetch blog posts to display on home page."""
    posts = db.session.execute(
        db.select(Post).order_by(Post.created.desc())
    ).scalars()

    return render_template("blog/index.html", posts=posts)


@bp.route("/create", methods=["GET", "POST"])
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
            post = Post()
            post.title = title
            post.body = body
            post.author_id = g.user.id
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


def get_post(id, check_author=True):
    """Fetch blog post."""
    post = db.session.execute(
        db.select(Post).filter_by(id=id)
    ).scalar_one_or_none()

    if post is None:
        abort(404, f"Post id {id} doesn't exit.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post


@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):
    """Update blog post."""
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
            post.title = title
            post.body = body
            db.session.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    """Delete blog post."""
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("blog.index"))

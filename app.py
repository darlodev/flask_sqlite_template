##############################
# IMPORTS
##############################
from flask import Flask, render_template, url_for, redirect, flash, abort, request
import sqlite3
##############################
# APP STRUCTURE
##############################
app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

def get_db_connection():
    conn = sqlite3.connect("database/database.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id)).fetchone()

    conn.close()
    if post is None:
        abort(404)
    return post
##############################
# VIEWS
##############################
@app.route("/")
def home():
    conn = get_db_connection()
    posts = conn.execute("SELECT * FROM posts").fetchall()
    conn.close()
    return render_template("index.html", posts=posts)

@app.route("/create/", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title - Required")
        elif not content:
            flash("Content - Required")
        else:
            conn = get_db_connection()
            conn.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for("home"))

    return render_template("create.html")

@app.route("/<int:id>/edit/", methods=("GET", "POST"))
def edit(id):
    content = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title - Required")
        elif not content:
            flash("Content - Required")
        else:
            conn = get_db_connection()
            conn.execute("UPDATE contents SET title = ?, content = ?" "WHERE id = ?", (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for("home"))
    return render_template("edit.html", content=content)

@app.route("/<int:id>/delete/", methods=("POST",))
def delete(id):
    content = get_post(id)
    conn = get_db_connection()
    conn.execute("DELETE FROM posts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash(f"'{['title']}' was deleted.")
    return redirect(url_for('home'))
##############################
# ERROR-HANDLING
##############################
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template("page_not_found.html"), 404
##############################
# DUBUGGING
##############################
if __name__ == "__main__":
    app.run(debug=True, port=8000)
##############################
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
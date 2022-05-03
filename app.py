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
##############################
# VIEWS
##############################
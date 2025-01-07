from flask import Flask, request, render_template, redirect, url_for
import os
from data_models import db, Author, Book

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{base_dir}/data/library.sqlite"

db.init_app(app)

# Create the database tables. Run once
# with app.app_context():
#    db.create_all()
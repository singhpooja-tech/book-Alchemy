import os
import requests
from datetime import datetime
from data_models import db, Author, Book
from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{base_dir}/data/library.sqlite"

db.init_app(app)


@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    """
    Handles the creation of a new author. The function accepts both GET and POST requests.
    - GET: Renders the form for adding a new author.
    - POST: Processes the form submission, validates the input, and adds the author to the database.
    """
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        birth_date = request.form.get('birth_year', '').strip()
        date_of_death = request.form.get('death_year', '').strip()

        # Validate name: it must contain only alphabetic characters and spaces
        if not name or not name.replace(' ', '').isalpha():
            warning_message = "Author name is required and must contain only letters."
            return render_template("add_author.html", warning_message=warning_message)

        # Validate birth_date and date_of_death
        def validate_date(date_str, field_name):
            if date_str:
                try:
                    return datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    raise ValueError(f"Invalid {field_name}. Please use 'YYYY-MM-DD' format.")
            return None

        try:
            birth_date = validate_date(birth_date, "birth date")
            date_of_death = validate_date(date_of_death, "date of death")

            # Check if date_of_death is after birth_date
            if birth_date and date_of_death and date_of_death <= birth_date:
                warning_message = "Date of death must be after the birth date."
                return render_template("add_author.html", warning_message=warning_message)
        except ValueError as e:
            return render_template("add_author.html", warning_message=str(e))

        # Create the Author object
        author = Author(
            name=name,
            birth_date=birth_date,
            date_of_death=date_of_death
        )

        try:
            db.session.add(author)
            db.session.commit()
            success_message = "Author added successfully!"
            return render_template("add_author.html", success_message=success_message)
        except SQLAlchemyError as e:
            db.session.rollback()
            warning_message = f"Error adding author to the database: {e}"
            return render_template("add_author.html", warning_message=warning_message)

    if request.method == "GET":
        return render_template("add_author.html")

# Create the database tables. Run once
# with app.app_context():
#   db.create_all()
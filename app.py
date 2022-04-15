# https://stackoverflow.com/questions/22364551/creating-flask-form-with-selects-from-more-than-one-table
# https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Time
# last_updated = db.Column(db.DateTime, default=datetime.datetime.now())
import os
from flask import Flask, render_template
from dotenv import load_dotenv, find_dotenv
from models import (
    db,
    assigned_task_table,
    Department,
    Shift,
    Certification,
    Employee,
    Patient,
    Guest,
    Task,
)
import datetime


load_dotenv(find_dotenv())
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("NEW_DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    """Renders index page"""
    return render_template("index.html")


@app.route("/a_login")
def a_login():
    """Renders login page"""
    return render_template("a_login.html")


@app.route("/admin")
def admin():
    """Function builds/render web app"""
    return render_template("admin.html")


@app.route("/empl_form")
def empl_form():
    """Function builds/render web app"""
    return render_template("empl_form.html")


@app.route("/guest_form")
def guest_form():
    """Function builds/render web app"""
    return render_template("guest_form.html")


@app.route("/m_login")
def m_login():
    """Function builds/render web app"""
    return render_template("m_login.html")


@app.route("/management")
def management():
    """Function builds/render web app"""
    return render_template("management.html")


@app.route("/med_form")
def med_form():
    """Function builds/render web app"""
    return render_template("med_form.html")


@app.route("/p_login")
def p_login():
    """Function builds/render web app"""
    return render_template("p_login.html")


@app.route("/patient_form")
def patient_form():
    """Function builds/render web app"""
    return render_template("patient_form.html")


@app.route("/patient")
def patient():
    """Function builds/render web app"""
    return render_template("patient.html")


@app.route("/rate")
def rate():
    """Function builds/render web app"""
    return render_template("rate.html")


@app.route("/task")
def task():
    """Function builds/render web app"""
    return render_template("task.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

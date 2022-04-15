# https://stackoverflow.com/questions/22364551/creating-flask-form-with-selects-from-more-than-one-table
# https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Time
# last_updated = db.Column(db.DateTime, default=datetime.datetime.now())
import os
from flask import Flask, render_template, request
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


@app.route("/", methods=["GET", "POST"])
def index():
    """Function builds/render web app"""
    if request.method == "POST":
        if request.form.get("employee"):
            return render_template("empl_form.html")
        if request.form.get("patient"):
            return render_template("patient_form.html")
        if request.form.get("medication"):
            return render_template("med_form.html")
        if request.form.get("department"):
            return render_template("dept_form.html")
        if request.form.get("guest"):
            return render_template("guest_form.html")
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

# https://stackoverflow.com/questions/22364551/creating-flask-form-with-selects-from-more-than-one-table
# https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Time
# last_updated = db.Column(db.DateTime, default=datetime.datetime.now())
import os
from flask import Flask, flash, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    LoginManager,
    login_required,
    login_user,
    logout_user,
)
from dotenv import load_dotenv, find_dotenv
from models import (
    Users,
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
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("NEW_DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_manager = LoginManager()
login_manager.init_app(app)


db.init_app(app)
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """loads  current user"""
    return Users.query.get(int(user_id))


@app.route("/add")
def add():
    # new = Users()
    new = Employee(
        status="A",
        first_name="John",
        last_name="Doe",
        phone=1,
        dob=datetime.datetime(2020, 5, 17),
        gender="M",
        hire=datetime.datetime(2020, 5, 17),
        login_id=1,
        dept_no=1,
    )

    # new = Department(dep_name="ICU", building="Main", floor=1)
    db.session.add(new)
    db.session.commit()
    # print("USERID:", new.id)

    return redirect(url_for("index"))


@app.route("/", methods=["GET", "POST"])
def index():
    """Renders index page"""
    if request.method == "POST":
        if request.form.get("user") == "management":
            depts = Department.query.all()
            return render_template("m_login.html", depts=depts)

        if request.form.get("user") == "patient":
            return render_template("p_login.html")

        if request.form.get("user") == "administration":
            return render_template("a_login.html")

    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    """Renders login page"""
    if request.method == "POST":

        if request.form.get("admin"):

            id_no = int(request.form.get("admin"))
            emp = Employee.query.filter_by(empl_id=id_no).first()
            if emp and emp.status == "A":
                user = Users.query.filter_by(id=emp.login_id).first()
                login_user(user)
                return render_template("admin.html")

            flash("That employee id is not associated with an admin account.")
            return render_template("index.html")

        if request.form.get("patient"):

            id_no = int(request.form.get("patient"))
            patient = Patient.query.filter_by(patient_id=id_no).first()
            if patient:
                user = Users.query.filter_by(id=patient.login_id).first()
                login_user(user)
                return render_template("patient.html")

            flash("That patient id cannot be found.")
            return render_template("index.html")

        if request.form.get("management"):

            id_no = int(request.form.get("management"))
            emp = Employee.query.filter_by(empl_id=id_no).first()
            if emp and (emp.status == "A" or emp.status == "M"):
                user = Users.query.filter_by(id=emp.login_id).first()
                login_user(user)
                return render_template("management.html")

            flash("That employee id is not associated with an management account.")
            return render_template("index.html")

    return render_template("index.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    """Recieve input from admin to display appropriate form"""
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

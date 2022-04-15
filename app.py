# https://stackoverflow.com/questions/22364551/creating-flask-form-with-selects-from-more-than-one-table
# https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Time
# last_updated = db.Column(db.DateTime, default=datetime.datetime.now())
from hashlib import new
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
    Visitor,
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
    usr = Users()
    db.session.add(usr)
    db.session.commit()

    dept = Department(dept_name="ICU", building="Main", floor=1)
    db.session.add(dept)
    db.session.commit()

    shift = Shift(work_days="Su M", work_hours="First Shift")
    db.session.add(shift)
    db.session.commit()

    cert = Certification(cert_name="R.N.", pay=50.00)
    db.session.add(cert)
    db.session.commit()

    emp = Employee(
        status="A",
        first_name="John",
        last_name="Doe",
        phone=1,
        dob=datetime.date(2020, 5, 17),
        gender="M",
        hire=datetime.date(2020, 5, 17),
        login_id=1,
        dept_no=1,
        cert_no=1,
    )

    db.session.add(emp)
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/", methods=["GET", "POST"])
def index():
    """Renders index page"""
    if request.method == "POST":

        if request.form.get("user") == "administration":
            return render_template("a_login.html")

        if request.form.get("user") == "management":
            return render_template("m_login.html", depts=Department.query.all())

        if request.form.get("user") == "patient":
            return render_template("p_login.html")

    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Renders login page"""
    if request.method == "POST":

        if request.form.get("admin"):

            id_no = int(request.form.get("admin"))
            emp = Employee.query.filter_by(empl_no=id_no).first()
            if emp and emp.status == "A":
                user = Users.query.filter_by(id=emp.login_id).first()
                login_user(user)
                return render_template("admin.html")

            flash("That Employee Number is not associated with an admin account.")
            return render_template("index.html")

        if request.form.get("management"):

            id_no = int(request.form.get("management"))
            emp = Employee.query.filter_by(empl_no=id_no).first()
            if emp and (emp.status == "A" or emp.status == "M"):
                user = Users.query.filter_by(id=emp.login_id).first()
                login_user(user)
                return render_template("management.html")

            flash("That Employee Number is not associated with an management account.")
            return render_template("index.html")

        if request.form.get("patient"):

            id_no = int(request.form.get("patient"))
            patient = Patient.query.filter_by(patient_no=id_no).first()
            if patient:
                user = Users.query.filter_by(id=patient.login_id).first()
                login_user(user)
                return render_template("patient.html")

            flash("That Patient Number cannot be found.")
            return render_template("index.html")

    return render_template("index.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    """Recieve input from admin to display appropriate form"""
    if request.method == "POST":
        if request.form.get("department"):
            return render_template("dept_form.html")

        if request.form.get("shift"):
            return render_template("shift_form.html")

        if request.form.get("certification"):
            return render_template("cert_form.html")

        if request.form.get("employee"):
            depts = Department.query.all()
            shifts = Shift.query.all()
            certs = Certification.query.all()
            return render_template(
                "empl_form.html", depts=depts, shifts=shifts, certs=certs
            )

        if request.form.get("patient"):
            depts = Department.query.all()
            emps = Employee.query.all()
            certs = Certification.query.all()
            return render_template(
                "patient_form.html",
                depts=depts,
                emps=emps,
                certs=certs,
            )

        if request.form.get("visitor"):
            pts = Patient.query.all()
            return render_template("vistor_form.html", pts=pts)

        if request.form.get("task"):
            certs = Certification.query.all()
            return render_template("task_form.html", certs=certs)

        # if request.form.get("medication"):
        #     return render_template("med_form.html")

    return render_template("admin.html")


@app.route("/handle_form", methods=["POST"])
def handle_form():
    data = request.form
    keys = data.keys()

    if data["type"] == "department":
        new = Department(
            dept_name=data["dept_name"],
            building=data["building"],
            floor=int(data["floor"]),
        )

    if data["type"] == "shift":
        work_days = ""
        if "Sunday" in keys:
            work_days += "Su "
        if "Monday" in keys:
            work_days += "M "
        if "Tuesday" in keys:
            work_days += "Tu "
        if "Wednesday" in keys:
            work_days += "W "
        if "Thursday" in keys:
            work_days += "Th "
        if "Friday" in keys:
            work_days += "F "
        if "Saturday" in keys:
            work_days += "Sa"
        new = Shift(
            work_days=work_days,
            work_hours=data["work_hours"],
        )

    if data["type"] == "certification":
        new = Certification(cert_name=data["cert_name"], pay=data["pay"])

    if data["type"] == "employee":
        new_user = Users()
        db.session.add(new_user)
        db.session.commit()
        new = Employee(
            status=data["status"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=int(data["phone"]),
            dob=str(data["dob"]),
            gender=data["gender"],
            hire=str(data["hire"]),
            login_id=new_user.id,
            dept_no=int(data["dept_no"]),
            shift_no=int(data["shift_no"]),
            cert_no=int(data["cert_no"]),
        )

    if data["type"] == "patient":
        new_user = Users()
        db.session.add(new_user)
        db.session.commit()
        new = Patient(
            first_name=data["first_name"],
            last_name=data["last_name"],
            phone=data["phone"],
            dob=str(data["dob"]),
            gender=data["gender"],
            admission_date=str(data["adm"]),
            login_id=new_user.id,
            dept_no=int(data["dept_no"]),
            caretaker_no=int(data["caretaker_no"]),
        )

    if data["type"] == "vistor":
        new = Visitor(
            first_name=data["first_name"],
            last_name=data["last_name"],
            association=data["association"],
            visiting_pt=int(data["visiting_pt"]),
        )

    if data["type"] == "task":
        new = Task(
            required_cert=int(data["required_cert"]),
            task_time=data["task_time"],
            priority=int(data["priority"]),
            duration=int(data["duration"]),
            required=bool(data["required"]),
            isMedicine=bool(data["isMedicine"]),
            recurring=bool(data["recurring"]),
            frequency=int(data["frequency"]),
        )

    db.session.add(new)
    db.session.commit()
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

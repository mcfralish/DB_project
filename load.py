import os
from flask import Flask, flash, render_template, redirect, request, url_for
from dotenv import load_dotenv, find_dotenv
from models import (
    Users,
    db,
    Department,
    Shift,
    Certification,
    Employee,
    Patient,
    Visitor,
    Task,
    AssignedTask,
)
import datetime


load_dotenv(find_dotenv())
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("NEW_DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def index():

    dept = Department(dept_name="IPU", building="Health Pavilion", floor=4)
    shift = Shift(work_days="Su M Tu W Th", work_hours="First Shift")

    cert1 = Certification(cert_name="M.D.", pay=150.00, clearance=1)
    cert2 = Certification(cert_name="R.N.", pay=50.00, clearance=3)
    cert3 = Certification(cert_name="C.N.A.", pay=20.00, clearance=4)

    usr1 = Users()
    usr2 = Users()
    usr3 = Users()
    usr4 = Users()
    usr5 = Users()

    emp1 = Employee(
        status="A",
        first_name="Harry",
        last_name="Huggins",
        phone="1",
        dob=datetime.date(2020, 5, 17),
        gender="M",
        hire=datetime.date(2020, 5, 17),
        login_id=1,
        dept_no=1,
        shift_no=1,
        cert_no=1,
    )

    emp2 = Employee(
        status="M",
        first_name="Lilly",
        last_name="Lomein",
        phone="1",
        dob=datetime.date(2020, 5, 17),
        gender="M",
        hire=datetime.date(2020, 5, 17),
        login_id=2,
        dept_no=1,
        shift_no=1,
        cert_no=2,
    )

    emp3 = Employee(
        status="E",
        first_name="Polly",
        last_name="Pocket",
        phone="1",
        dob=datetime.date(2020, 5, 17),
        gender="M",
        hire=datetime.date(2020, 5, 17),
        login_id=3,
        dept_no=1,
        shift_no=1,
        cert_no=3,
    )

    pt1 = Patient(
        first_name="James",
        last_name="Jackson",
        phone="1",
        dob=datetime.date(2020, 5, 17),
        gender="M",
        admission_date=datetime.date(2020, 5, 17),
        login_id=4,
        dept_no=1,
    )

    pt2 = Patient(
        first_name="Regina",
        last_name="Rollins",
        phone="1",
        dob=datetime.date(2020, 5, 17),
        gender="F",
        admission_date=datetime.date(2020, 5, 17),
        login_id=5,
        dept_no=1,
    )

    task1 = Task(
        task_name="Initial Assessment",
        priority=1,
        duration=60,
        required=True,
        isMedicine=False,
        clearance=1,
        recurring=False,
    )

    task2 = Task(
        task_name="Give Bath",
        priority=3,
        duration=60,
        required=True,
        isMedicine=False,
        recurring=True,
        clearance=4,
        frequency=24,
    )

    task3 = Task(
        task_name="Give Pain Meds",
        priority=1,
        duration=15,
        required=True,
        isMedicine=True,
        recurring=True,
        clearance=3,
        frequency=6,
    )

    task4 = Task(
        task_name="Get Coffee",
        priority=5,
        duration=15,
        required=False,
        isMedicine=False,
        recurring=False,
        clearance=5,
    )

    db.session.add(dept)
    db.session.add(shift)
    db.session.add(cert1)
    db.session.add(cert2)
    db.session.add(cert3)
    db.session.add(usr1)
    db.session.add(usr2)
    db.session.add(usr3)
    db.session.add(usr4)
    db.session.add(usr5)
    db.session.add(emp1)
    db.session.add(emp2)
    db.session.add(emp3)
    db.session.add(pt1)
    db.session.add(pt2)
    db.session.add(task1)
    db.session.add(task2)
    db.session.add(task3)
    db.session.add(task4)
    db.session.commit()

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

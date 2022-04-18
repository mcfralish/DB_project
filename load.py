import os
import random as r
import numpy as np
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

    dept = Department(dept_name="ICU", building="Trauma Center", floor=3)
    db.session.add(dept)
    dept = Department(dept_name="Radiology", building="Main", floor=3)
    db.session.add(dept)
    dept = Department(dept_name="Oncology", building="Annex", floor=2)
    db.session.add(dept)
    dept = Department(dept_name="Pediatry", building="Health Pavilion", floor=2)
    db.session.add(dept)
    dept = Department(dept_name="Optomitry", building="Main", floor=7)
    db.session.add(dept)
    dept = Department(dept_name="Hospice", building="Health Pavilion", floor=4)
    db.session.add(dept)
    dept = Department(dept_name="Emergency", building="Trauma Center", floor=1)
    db.session.add(dept)
    dept = Department(dept_name="Telemetry", building="Main", floor=6)
    db.session.add(dept)
    dept = Department(dept_name="Dermatology", building="Main", floor=2)
    db.session.add(dept)
    dept = Department(dept_name="Pathology", building="Annex", floor=3)
    db.session.add(dept)

    shift = Shift(work_days="M Tu W Th", work_hours="First Shift")
    db.session.add(shift)
    shift = Shift(work_days="M Tu W Th", work_hours="Second Shift")
    db.session.add(shift)
    shift = Shift(work_days="M Tu W Th", work_hours="Thrid Shift")
    db.session.add(shift)
    shift = Shift(work_days="Su Sa", work_hours="First Shift")
    db.session.add(shift)
    shift = Shift(work_days="Su Sa", work_hours="Second Shift")
    db.session.add(shift)

    cert = Certification(cert_name="M.D.", pay=150.00, clearance=1)
    db.session.add(cert)
    cert = Certification(cert_name="R.N.", pay=50.00, clearance=2)
    db.session.add(cert)
    cert = Certification(cert_name="C.N.A.", pay=20.00, clearance=3)
    db.session.add(cert)
    cert = Certification(cert_name="Reception", pay=15.00, clearance=5)
    db.session.add(cert)
    cert = Certification(cert_name="Medical Records", pay=20.00, clearance=4)
    db.session.add(cert)
    cert = Certification(cert_name="Social Worker", pay=50.00, clearance=4)
    db.session.add(cert)

    # Emps
    genders = ["M", "F"]
    deps = list(range(1, 10 + 1))
    shifts = list(range(1, 5 + 1))
    dob_years = list(range(1955, 2002))
    hire_years = list(range(2010, 2022))
    days = list(range(1, 31))
    months = list(range(1, 13))
    certs = list(range(1, 6 + 1))
    first_names = [
        "Harry",
        "Ron",
        "Hermione",
        "Albus",
        "Ginny",
        "Severus",
        "Rubeus",
        "Draco",
        "Neville",
        "Minerva",
        "Sirius",
        "Luna",
        "Remus",
        "Bellatrix",
        "Molly",
        "Bill",
        "George",
        "Dudley",
        "Dolores",
        "Fred",
        "Dobby",
        "Alastor",
        "Lucius",
        "Gilderoy",
        "Cho",
        "Arthur",
        "Petunia",
        "Gellert",
        "Fluer",
        "Nymphadora",
        "Argus",
        "Narcissa",
        "Vernon",
        "Percy",
        "Peter",
        "Sybill",
        "Cornelius",
        "Rita",
        "Quirinus",
        "Horace",
        "Lily",
        "James",
        "viktor",
        "Vincent",
        "Gregory",
        "Newt",
        "Tom",
    ]
    last_names = [
        "Potter",
        "Weasley",
        "Granger",
        "Riddle",
        "Voldemort",
        "Dumbledore",
        "Snape",
        "Hagrid",
        "Malfoy",
        "Longbottom",
        "McGonagall",
        "Black",
        "Lovegood",
        "Lupin",
        "Lestrange",
        "Dursley",
        "Umbridge",
        "Moody",
        "Lockhart",
        "Chang",
        "Grindelwald",
        "Delacour",
        "Tonks",
        "Filch",
        "Pettigrew",
        "Trelawney",
        "Fudge",
        "Skeeter",
        "Quirrell",
        "Slughorn",
        "Krum",
        "Crabbe",
        "Goyle",
        "Scamander",
    ]
    login_id = 1

    # Admins
    for i in range(3):
        usr = Users()
        emp = Employee(
            status="A",
            first_name=r.choice(first_names),
            last_name=r.choice(last_names),
            phone="555-555-5555",
            dob=datetime.date(r.choice(dob_years), r.choice(months), r.choice(days)),
            gender=r.choice(genders),
            hire=datetime.date(r.choice(hire_years), r.choice(months), r.choice(days)),
            login_id=login_id,
            dept_no=r.choice(deps),
            shift_no=r.choice(shifts),
            cert_no=1,
        )
        db.session.add(usr)
        db.session.add(emp)
        login_id += 1

    # Managers
    for i in range(10):
        usr = Users()
        emp = Employee(
            status="M",
            first_name=r.choice(first_names),
            last_name=r.choice(last_names),
            phone="555-555-5555",
            dob=datetime.date(r.choice(dob_years), r.choice(months), r.choice(days)),
            gender=r.choice(genders),
            hire=datetime.date(r.choice(hire_years), r.choice(months), r.choice(days)),
            login_id=login_id,
            dept_no=i + 1,
            shift_no=r.choice(shifts),
            cert_no=1,
        )
        db.session.add(usr)
        db.session.add(emp)
        login_id += 1

    # Emps
    for i in range(100):
        usr = Users()
        emp = Employee(
            status="M",
            first_name=r.choice(first_names),
            last_name=r.choice(last_names),
            phone="555-555-5555",
            dob=datetime.date(r.choice(dob_years), r.choice(months), r.choice(days)),
            gender=r.choice(genders),
            hire=datetime.date(r.choice(hire_years), r.choice(months), r.choice(days)),
            login_id=login_id,
            dept_no=r.choice(deps),
            shift_no=r.choice(shifts),
            cert_no=r.choice(certs),
        )
        db.session.add(usr)
        db.session.add(emp)
        login_id += 1

    # Patients
    for i in range(500):
        usr = Users()
        pt = Patient(
            first_name=r.choice(first_names),
            last_name=r.choice(last_names),
            phone="555-555-5555",
            dob=datetime.date(r.choice(dob_years), r.choice(months), r.choice(days)),
            gender=r.choice(genders),
            admission_date=datetime.date(
                r.choice(hire_years), r.choice(months), r.choice(days)
            ),
            login_id=login_id,
            dept_no=r.choice(deps),
        )
        db.session.add(usr)
        db.session.add(pt)
        login_id += 1

    pts = list(range(1, 501))
    associations = [
        "Husband",
        "Wife",
        "Brother",
        "Sister",
        "Mother",
        "Father",
        "Cousin",
        "Friend",
        "Grandfather",
        "Grandmother",
        "Grandson",
        "Grandaughter",
        "Aunt",
        "Uncle",
        "Niece",
        "Nephew",
    ]

    # Visitors
    for i in range(500):
        vstr = Visitor(
            first_name=r.choice(first_names),
            last_name=r.choice(last_names),
            association=r.choice(associations),
            visiting_pt=r.choice(pts),
        )
        db.session.add(vstr)

    task = Task(
        task_name="Initial Assessment",
        priority=1,
        duration=60,
        required=True,
        isMedicine=False,
        clearance=1,
        recurring=False,
    )
    db.session.add(task)

    task = Task(
        task_name="Give Bath",
        priority=3,
        duration=60,
        required=True,
        isMedicine=False,
        recurring=True,
        clearance=3,
        frequency=24,
    )
    db.session.add(task)

    task = Task(
        task_name="Give Pain Meds",
        priority=1,
        duration=15,
        required=True,
        isMedicine=True,
        recurring=True,
        clearance=2,
        frequency=6,
    )
    db.session.add(task)

    task = Task(
        task_name="Get Coffee",
        priority=9,
        duration=15,
        required=False,
        isMedicine=False,
        recurring=False,
        clearance=5,
    )
    db.session.add(task)

    task = Task(
        task_name="Fluff Pillow",
        priority=8,
        duration=5,
        required=False,
        isMedicine=False,
        recurring=False,
        clearance=5,
    )
    db.session.add(task)

    task = Task(
        task_name="Chart on Patient",
        priority=5,
        duration=15,
        required=True,
        isMedicine=False,
        recurring=False,
        frequency=2,
        clearance=4,
    )
    db.session.add(task)

    task = Task(
        task_name="Provide Emotional Support",
        priority=7,
        duration=30,
        required=False,
        isMedicine=False,
        recurring=False,
        clearance=4,
    )
    db.session.add(task)

    db.session.commit()

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

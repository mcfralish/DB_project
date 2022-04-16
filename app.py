# https://stackoverflow.com/questions/22364551/creating-flask-form-with-selects-from-more-than-one-table
# https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Time
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
    # assigned_task_table,
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
login_manager = LoginManager()
login_manager.init_app(app)


db.init_app(app)
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    """loads  current user"""
    return Users.query.get(int(user_id))


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


@app.route("/login", methods=["POST"])
def login():
    """Renders login page"""
    if request.method == "POST":

        if request.form.get("admin"):

            id_no = int(request.form.get("admin"))
            emp = Employee.query.filter_by(empl_no=id_no).first()
            if emp and emp.status == "A":
                user = Users.query.filter_by(id=emp.login_id).first()
                login_user(user)
                return redirect(url_for("admin"))

            flash("That Employee Number is not associated with an admin account.")
            return render_template("index.html")

        if request.form.get("management"):

            id_no = int(request.form.get("management"))
            emp = Employee.query.filter_by(empl_no=id_no).first()
            emps = Employee.query.all()
            if emp and (emp.status == "A" or emp.status == "M"):
                user = Users.query.filter_by(id=emp.login_id).first()
                login_user(user)
                return redirect(url_for("manager"))

            flash("That Employee Number is not associated with an management account.")
            return render_template("index.html")

        if request.form.get("patient"):

            id_no = int(request.form.get("patient"))
            patient = Patient.query.filter_by(patient_no=id_no).first()
            if patient:
                user = Users.query.filter_by(id=patient.login_id).first()
                login_user(user)
                return redirect(url_for("patient"))

            flash("That Patient Number cannot be found.")
            return render_template("index.html")

    return redirect(url_for("index"))


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
            return render_template("visitor_form.html", pts=pts)

        if request.form.get("task"):
            certs = Certification.query.all()
            return render_template("task_form.html", certs=certs)

        # if request.form.get("medication"):
        #     return render_template("med_form.html")

    return render_template("admin.html")


@app.route("/handle_admin", methods=["POST"])
def handle_admin():
    data = request.form
    keys = data.keys()
    print(data)

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
        new = Certification(
            cert_name=data["cert_name"], pay=data["pay"], clearance=data["clearance"]
        )

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
        )

    if data["type"] == "visitor":
        new = Visitor(
            first_name=data["first_name"],
            last_name=data["last_name"],
            association=data["association"],
            visiting_pt=int(data["visiting_pt"]),
        )

    if data["type"] == "task":
        new = Task(
            task_name=data["task_name"],
            priority=int(data["priority"]),
            duration=int(data["duration"]),
            required=False,
            isMedicine=False,
            clearance=data["clearance"],
            recurring=False,
        )

        if data["required"] == "True":
            new.required = True

        if data["isMedicine"] == "True":
            new.isMedicine = True

        if data["recurring"] == "True":
            new.recurring = True

        if data["frequency"] != "":
            new.frequency = int(data["frequency"])

        if (new.recurring == False) and (new.frequency != None):
            new = None
            flash("May not include frequency on non-recurring tasks.")

    if new:
        db.session.add(new)
        db.session.commit()

    return redirect(url_for("admin"))


@app.route("/manager", methods=["GET", "POST"])
def manager():

    manager = Employee.query.filter_by(login_id=current_user.id).first()
    dep = Department.query.filter_by(dept_no=manager.dept_no).first()
    certs = Certification.query.all()
    tasks = Task.query.all()
    dep_pts = Patient.query.filter_by(dept_no=dep.dept_no).all()
    dep_emps = Employee.query.all()

    if request.method == "POST":
        data = request.form

        if data["action"] == "assign_task":
            assign = AssignedTask(
                requesting_pt=data["pt_no"],
                task_no=data["task_no"],
                assigned_caregiver=data["emp_no"],
            )

            caregiver_clearance = (
                Certification.query.filter_by(
                    cert_no=Employee.query.filter_by(empl_no=assign.assigned_caregiver)
                    .first()
                    .cert_no
                )
                .first()
                .clearance
            )

            required_clearance = (
                Task.query.filter_by(task_no=assign.task_no).first().clearance
            )

            if caregiver_clearance <= required_clearance:
                db.session.add(assign)
                db.session.commit()
            else:
                flash("Caregiver does not meet required clearance.")

    unassigned_tasks = AssignedTask.query.filter_by(assigned_caregiver=None).all()
    all_tasks = AssignedTask.query.all()
    assigned_tasks = []
    for task in all_tasks:
        if task.assigned_caregiver != None:
            assigned_tasks.append(task)

    unassigned_tasks.sort(
        key=lambda x: Task.query.filter_by(task_no=x.task_no).first().priority
    )
    assigned_tasks.sort(
        key=lambda x: Task.query.filter_by(task_no=x.task_no).first().priority
    )

    unassigned_list = []
    assigned_list = []

    for i in range(len(unassigned_tasks)):
        task_tuple = (
            Task.query.filter_by(task_no=unassigned_tasks[i].task_no).first(),
            Patient.query.filter_by(
                patient_no=unassigned_tasks[i].requesting_pt
            ).first(),
            unassigned_tasks[i].at_no,
        )

        if task_tuple[1].dept_no == dep.dept_no:
            unassigned_list.append(task_tuple)

    for i in range(len(assigned_tasks)):
        task_tuple = (
            Task.query.filter_by(task_no=assigned_tasks[i].task_no).first(),
            Patient.query.filter_by(patient_no=assigned_tasks[i].requesting_pt).first(),
            Employee.query.filter_by(
                empl_no=assigned_tasks[i].assigned_caregiver
            ).first(),
            assigned_tasks[i].at_no,
        )

        if task_tuple[1].dept_no == dep.dept_no:
            assigned_list.append(task_tuple)

    return render_template(
        "management.html",
        manager=manager,
        dep=dep,
        dep_pts=dep_pts,
        dep_emps=dep_emps,
        certs=certs,
        tasks=tasks,
        unassigned_list=unassigned_list,
        assigned_list=assigned_list,
    )


@app.route("/patient", methods=["GET", "POST"])
def patient():

    if request.method == "POST":
        data = request.form
        requested = AssignedTask(requesting_pt=data["pt_no"], task_no=data["task_no"])
        db.session.add(requested)
        db.session.commit()

    pt = Patient.query.filter_by(login_id=current_user.id).first()
    dep = Department.query.filter_by(dept_no=pt.dept_no).first()
    certs = Certification.query.all()
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        if task.required == False:
            task_list.append(task)

    my_tasks = AssignedTask.query.filter_by(requesting_pt=pt.patient_no).all()
    requested = []
    assigned = []

    for task in my_tasks:
        if task.assigned_caregiver == None:
            requested.append(Task.query.filter_by(task_no=task.task_no).first())
        else:
            task_tuple = (
                Task.query.filter_by(task_no=task.task_no),
                Employee.query.filter_by(empl_no=task.assigned_caregiver),
            )
            assigned.append(task_tuple)

    return render_template(
        "patient.html",
        certs=certs,
        pt=pt,
        dep=dep,
        task_list=task_list,
        requested=requested,
        assigned=assigned,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

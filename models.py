import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
meta = MetaData()
db = SQLAlchemy()


assigned_task_table = db.Table(
    "task",
    meta,
    db.Column("task_id", db.ForeignKey("Task.id"), primary_key=True),
    db.Column("patient_id", db.ForeignKey("Patient.id"), primary_key=True),
    db.Column("emp_id", db.ForeignKey("Employee.id"), primary_key=True),
)


class Department(db.Model, Base):
    __tablename__ = "Department"
    dept_no = db.Column(db.Integer, primary_key=True)
    dep_name = db.Column(db.String(20))
    building = db.Column(db.String(20))
    floor = db.Column(db.Integer)
    assigned_employees = relationship("Employee")
    assigned_patients = relationship("Patient")


class Shift(db.Model, Base):
    __tablename__ = "Shift"
    shift_id = db.Column(db.Integer, primary_key=True)
    shift_start = db.Column(db.DateTime)
    shift_end = db.Column(db.DateTime)
    work_days = db.Column(db.String(11))
    assigned_employees = relationship("Employee")


class Certification(db.Model, Base):
    __tablename__ = "Certifcation"
    cert_id = db.Column(db.Integer, primary_key=True)
    certification = db.Column(db.String(5))
    pay = db.Column(db.Float)
    emloyees = relationship("Employee")
    qualified_tasks = relationship("Tasks")


class Employee(db.Model, Base):
    __tablename__ = "Employee"
    empl_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    phone = db.Column(db.Integer)
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String(1))
    hire = db.Column(db.DateTime)
    dept_no = db.Column(db.Integer, db.ForeignKey(Department.dept_no))
    shift_no = db.Column(db.Integer, db.ForeignKey(Shift.shift_id))
    cert_id = db.Column(db.Integer, db.ForeignKey(Certification.cert_id))


class Patient(db.Model, Base):
    patient_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    phone = db.Column(db.Integer)
    dob = db.Column(db.DateTime)
    gender = db.Column(db.String(1))
    caretaker_id = db.Column(db.Integer, db.ForeignKey(Employee.empl_id))
    dept_no = db.Column(db.Integer, db.ForeignKey(Department.dept_no))


class Guest(db.Model, Base):
    __tablename__ = "Guest"
    guest_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    relationship = db.Column(db.String(200))
    patient_name = db.Column(db.String(200))
    visit_start = db.Column(db.DateTime)


class Task(db.Model, Base):
    __tablename__ = "Task"
    task_id = db.Column(db.Integer, primary_key=True)
    required_cert = db.Column(db.Integer, db.ForeignKey(Certification.cert_id))
    task_name = db.Column(db.String(30))
    priority = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    required = db.Column(db.Boolean)
    recurring = db.Column(db.Boolean)
    frequency = db.Column(db.Integer)
    isMedicine = db.Column(db.Boolean)

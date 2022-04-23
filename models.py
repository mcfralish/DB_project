from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
meta = MetaData()
db = SQLAlchemy()


class Users(db.Model, UserMixin, Base):
    id = db.Column(db.Integer, primary_key=True)
    employee = relationship("Employee")
    patient = relationship("Patient")


class Department(db.Model, Base):
    dept_no = db.Column(db.Integer, primary_key=True)
    dept_name = db.Column(db.String(200), nullable=False)
    building = db.Column(db.String(200), nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    assigned_employees = relationship("Employee")
    assigned_patients = relationship("Patient")


class Shift(db.Model, Base):
    shift_no = db.Column(db.Integer, primary_key=True)
    work_days = db.Column(db.String(200), nullable=False)
    work_hours = db.Column(db.String(200), nullable=False)


class Certification(db.Model, Base):
    cert_no = db.Column(db.Integer, primary_key=True)
    cert_name = db.Column(db.String(20), nullable=False)
    pay = db.Column(db.Float, nullable=False)
    clearance = db.Column(db.Integer, nullable=False)
    qualified_emloyees = relationship("Employee")


class Employee(db.Model, Base):
    empl_no = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(1), nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    hire = db.Column(db.String(200), nullable=False)
    login_id = db.Column(Integer, ForeignKey(Users.id), nullable=False)
    dept_no = db.Column(db.Integer, ForeignKey(Department.dept_no), nullable=False)
    shift_no = db.Column(db.Integer, ForeignKey(Shift.shift_no))
    cert_no = db.Column(db.Integer, ForeignKey(Certification.cert_no), nullable=False)
    taks_assigned = relationship("AssignedTask")


class Patient(db.Model, Base):
    patient_no = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    admission_date = db.Column(db.String(200), nullable=False)
    login_id = db.Column(Integer, ForeignKey(Users.id), nullable=False)
    dept_no = db.Column(db.Integer, ForeignKey(Department.dept_no), nullable=False)
    visitors = relationship("Visitor")
    requested_tasks = relationship("AssignedTask")


class Visitor(db.Model, Base):
    visitor_no = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    association = db.Column(db.String(200), nullable=False)
    visiting_pt = db.Column(db.Integer, ForeignKey(Patient.patient_no), nullable=False)


class Task(db.Model, Base):
    task_no = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    required = db.Column(db.Boolean, nullable=False)
    isMedicine = db.Column(db.Boolean, nullable=False)
    clearance = db.Column(db.Integer, nullable=False)
    recurring = db.Column(db.Boolean, nullable=False)
    frequency = db.Column(db.Integer)
    tasks_assigned = relationship("AssignedTask")


class AssignedTask(db.Model, Base):
    at_no = db.Column(db.Integer, primary_key=True)
    requesting_pt = db.Column(db.Integer, ForeignKey(Patient.patient_no))
    task_no = db.Column(db.Integer, ForeignKey(Task.task_no))
    assigned_caregiver = db.Column(db.Integer, ForeignKey(Employee.empl_no))

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# shift class
class Shift(db.Model):

    __tablename__ = "shift"
    shift_id = db.Column(db.Integer, primary_key=True)
    shift_start = db.Column(db.DateTime)
    shift_end = db.Column(db.DateTime)
    work_days = db.Column(db.String(200))


# empl class
class Empl(db.Model):

    __tablename__ = "empl"
    empl_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    phone = db.Column(db.Integer)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(1))
    hire = db.Column(db.Date)
    dept = db.Column(db.String(200))


class Guest(db.Model):

    __tablename__ = "guest"
    guest_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    relationship = db.Column(db.String(200))
    patient_name = db.Column(db.String(200))
    visit_start = db.Column(db.DateTime)


class Meds(db.Model):

    __tablename__ = "meds"
    med_id = db.Column(db.Integer, primary_key=True)
    med_name = db.Column(db.String(200))
    dosage = db.Column(db.String(200))
    recurring = db.Column(db.Boolean)
    recurring_time = db.Column(db.Integer)

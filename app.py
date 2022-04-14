# https://stackoverflow.com/questions/22364551/creating-flask-form-with-selects-from-more-than-one-table
# https://docs.sqlalchemy.org/en/14/core/type_basics.html#sqlalchemy.types.Time
# last_updated = db.Column(db.DateTime, default=datetime.datetime.now())

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import inspect
import datetime

# sets all parameters for the Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

ENV = "dev"

if ENV == "dev":
    app.debug = True
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://nbuysymo:KThBzw-jxq4s4Mzv7KjApmLNROSJ75R9@castor.db.elephantsql.com/nbuysymo"
else:
    app.debut = False
    app.config["SQLALCHEMY_DATABASE_URI"] = ""

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# shift class
class shift(db.Model):

    __tablename__ = "shift"
    shift_id = db.Column(db.Integer, primary_key=True)
    shift_start = db.Column(db.DateTime)
    shift_end = db.Column(db.DateTime)
    work_days = db.Column(db.String(200))

    def __init__(self, shift_id, shift_start, shift_end, work_days):
        self.shift_id = shift_id
        self.shift_start = shift_start
        self.shift_end = shift_end
        self.work_days = work_days


engine = create_engine(
    "postgresql://nbuysymo:KThBzw-jxq4s4Mzv7KjApmLNROSJ75R9@castor.db.elephantsql.com/nbuysymo"
)
inspector = inspect(engine)
for table_name in inspector.get_table_names():
    for column in inspector.get_columns(table_name):
        print("Column: %s" % column["name"])

# empl class
class empl(db.Model):

    __tablename__ = "empl"
    empl_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    phone = db.Column(db.Integer)
    dob = db.Column(db.Date)
    gender = db.Column(db.String(1))
    hire = db.Column(db.Date)
    dept = db.Column(db.String(200))

    def __init__(self, first_name, last_name, phone, dob, gender, hire, dept):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.dob = dob
        self.gender = gender
        self.hire = hire
        self.dept = dept


# guest class
class guest(db.Model):

    __tablename__ = "guest"
    guest_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    relationship = db.Column(db.String(200))
    patient_name = db.Column(db.String(200))
    visit_start = db.Column(db.DateTime)

    def __init__(self, first_name, last_name, phone, dob, gender, hire):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.dob = dob
        self.gender = gender
        self.hire = hire


# medication class
class meds(db.Model):

    __tablename__ = "meds"
    med_id = db.Column(db.Integer, primary_key=True)
    med_name = db.Column(db.String(200))
    dosage = db.Column(db.String(200))
    recurring = db.Column(db.Boolean)
    recurring_time = db.Column(db.Integer)

    def __init__(self, med_name, dosage, recurring, recurring_time):
        self.med_name = med_name
        self.dosage = dosage
        self.recurring = recurring
        self.recurring_time = recurring_time


engine = create_engine(
    "postgresql://nbuysymo:KThBzw-jxq4s4Mzv7KjApmLNROSJ75R9@castor.db.elephantsql.com/nbuysymo"
)
inspector = inspect(engine)
for table_name in inspector.get_table_names():
    for column in inspector.get_columns(table_name):
        print("Column: %s" % column["name"])


@app.route("/")
def index():
    """Function builds/render web app"""
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

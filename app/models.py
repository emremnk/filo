from datetime import date
from . import db


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(20), unique=True, nullable=False)
    inspection_date = db.Column(db.Date)
    insurance_date = db.Column(db.Date)
    exam_date = db.Column(db.Date)

    fines = db.relationship('TrafficFine', back_populates='vehicle', cascade='all, delete-orphan')


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    identity_no = db.Column(db.String(30))
    phone = db.Column(db.String(30))
    license_info = db.Column(db.String(120))
    license_expiry = db.Column(db.Date)

    absences = db.relationship('DriverAbsence', back_populates='driver', cascade='all, delete-orphan')


class DriverAbsence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    absence_date = db.Column(db.Date, nullable=False)

    driver = db.relationship('Driver', back_populates='absences')


class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    contract_start = db.Column(db.Date)
    contract_end = db.Column(db.Date)
    invoice_date = db.Column(db.Date)


class TrafficFine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    deducted_from_salary = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(200))

    vehicle = db.relationship('Vehicle', back_populates='fines')


class Check(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    company = db.Column(db.String(120), nullable=False)
    received_date = db.Column(db.Date)
    issued_date = db.Column(db.Date)
    payable_date = db.Column(db.Date)


def to_iso(d: date | None):
    return d.isoformat() if d else None

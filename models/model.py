from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Car(db.Model):
    __tablename__ = 'cars'
    car_id = db.Column(db.Integer, primary_key=True)
    rate_id = db.Column(db.Integer, db.ForeignKey('rates.rate_id'))
    status = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rate = db.relationship('Rate', backref='cars', lazy=True)


class Location(db.Model):
    __tablename__ = 'locations'
    location_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)


class Organization(db.Model):
    __tablename__ = 'organizations'
    organization_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    phone_number = db.Column(db.String(20))
    fio_director = db.Column(db.String(100))
    organization_name = db.Column(db.String(200))
    location = db.relationship('Location', backref='organizations', lazy=True)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20))
    fio = db.Column(db.String(100))


class Rate(db.Model):
    __tablename__ = 'rates'
    rate_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50))


class Deal(db.Model):
    __tablename__ = 'deals'
    deal_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('cars.car_id'), nullable=False)
    rate_id = db.Column(db.Integer, db.ForeignKey('rates.rate_id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.organization_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)

    car = db.relationship('Car', backref='deals')
    rate = db.relationship('Rate', backref='deals')
    organization = db.relationship('Organization', backref='deals')
    user = db.relationship('User', backref='deals')

    def __init__(self, car_id, rate_id, organization_id, user_id):
        self.car_id = car_id
        self.rate_id = rate_id
        self.organization_id = organization_id
        self.user_id = user_id
        self.start_time = datetime.utcnow()

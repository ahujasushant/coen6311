from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login


class Volunteer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    dob = db.Column(db.String(128))
    street_name = db.Column(db.String(128))
    street_number = db.Column(db.String(128))
    post_code = db.Column(db.String(128))
    country = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    days_of_availability = db.Column(db.String(128))
    areas_of_interest = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))


    def __repr__(self):
        return '<Volunteer {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return Volunteer.query.get(int(id))


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(64), index=True, unique=True)
    founded_in = db.Column(db.String(120), index=True, unique=True)
    official_email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<Organization {}>'.format(self.org_name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))
    location = db.Column(db.String(120))

    def __repr__(self):
        return '<Post {}>'.format(self.description)




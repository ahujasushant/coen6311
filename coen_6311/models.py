from datetime import datetime
from coen_6311 import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from coen_6311 import login


class Volunteer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    dob = db.Column(db.String(128), default='')
    street_name = db.Column(db.String(128), default='')
    street_number = db.Column(db.String(128), default='')
    post_code = db.Column(db.String(128), default='')
    state = db.Column(db.String(128), default='')
    country = db.Column(db.String(128), default='')
    phone = db.Column(db.String(128), default='')
    days_of_availability = db.Column(db.String(128), default='')
    areas_of_interest = db.Column(db.String(128), default='')
    password_hash = db.Column(db.String(128))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    history = db.relationship('History', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Volunteer {}>'.format(self.name)

    def location(self):
        if self.street_number and self.street_name and self.state and self.country and self.post_code:
            return self.street_number + ',' + self.street_name + ',' + self.state + ',' + self.country + ',' + self.post_code

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class History(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(64), index=True)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteer.id'))

    def __repr__(self):
        return '<History {}>'.format(self.location)


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(64), index=True, unique=True)
    founded_in = db.Column(db.String(120), index=True, unique=True)
    official_email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')


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
    organization_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    volunteers = db.relationship('Volunteer', backref='author', lazy='dynamic')


    def __repr__(self):
        return '<Post {}>'.format(self.description, self.location)




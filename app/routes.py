# Imports

import flask
from app import app
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user
from app.models import Volunteer, Organization
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from app import db



# Controllers.

@app.route('/')
def home():
    return flask.render_template('dashboard/home.html')


@app.route('/about')
def about():
    return flask.render_template('dashboard/about_us.html')


@app.route('/register_organization', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('about'))
    form = RegistrationForm()
    if form.validate_on_submit():
        organization = Organization(org_name=form.org_name.data, official_email=form.official_email.data)
        organization.set_password(form.password.data)
        db.session.add(organization)
        db.session.commit()
        flask.flash('Congratulations, you successfully registered as an Organization!')
        return flask.redirect(flask.url_for('posts'))
    return flask.render_template('/registration/register.html', title='Register', form=form)


@app.route('/login_organization', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('posts'))
    form = LoginForm()
    if form.validate_on_submit():
        organization = Organization.query.filter_by(official_email=form.official_email.data).first()
        if organization is None or not organization.check_password(form.password.data):
            flask.flash('Invalid name or password')
            return flask.redirect(flask.url_for('register'))

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = flask.url_for('posts')
        return flask.redirect(next_page)
    return flask.render_template('/login/login.html', title='Sign In', form=form)


@app.route('/logout_org')
def logout():
    logout_user()
    return flask.redirect(flask.url_for('home'))


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    return flask.render_template('post/index.html')
# Launch Application

# Default port:


if __name__ == '__main__':
    app.run()

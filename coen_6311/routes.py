# Imports

import flask
from coen_6311 import app
from coen_6311.forms import LoginForm, RegistrationForm, VolunteerLoginForm, VolunteerRegistrationForm, PostForm
from flask_login import current_user, login_user
from coen_6311.models import Volunteer, Organization, Post
from flask_login import logout_user
from flask import request
from werkzeug.urls import url_parse
from coen_6311 import db



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
        return flask.redirect(flask.url_for('posts'))
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
            return flask.redirect(flask.url_for('login'))

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = flask.url_for('posts')
        return flask.redirect(next_page)
    return flask.render_template('/login/login.html', title='Sign In', form=form)


@app.route('/register_volunteer', methods=['GET', 'POST'])
def register_vol():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('about'))
    form = VolunteerRegistrationForm()
    if form.validate_on_submit():
        volunteer = Volunteer(email=form.email.data)
        volunteer.set_password(form.password.data)
        db.session.add(volunteer)
        db.session.commit()
        flask.flash('Congratulations, you successfully registered as a Volunteer!')
        return flask.redirect(flask.url_for('about'))
    return flask.render_template('/registration/register_volunteer.html', title='Register', form=form)


@app.route('/login_volunteer', methods=['GET', 'POST'])
def login_vol():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('posts'))
    form = VolunteerLoginForm()
    if form.validate_on_submit():
        volunteer = Volunteer.query.filter_by(email=form.email.data).first()
        if volunteer is None or not volunteer.check_password(form.password.data):
            flask.flash('Invalid name or password')
            return flask.redirect(flask.url_for('login_vol'))

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = flask.url_for('about')
        return flask.redirect(next_page)
    return flask.render_template('/login/login_volunteer.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return flask.redirect(flask.url_for('home'))


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    posts = Post.query.all()
    return flask.render_template('post/index.html', posts=posts)


@app.route('/volunteers', methods=['GET', 'POST'])
def volunteers():
    volunteers = Volunteer.query.all()
    return flask.render_template('volunteer/index.html', volunteers=volunteers)

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('about'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(description=form.description.data, location=form.location.data)
        db.session.add(post)
        db.session.commit()
        flask.flash('Congratulations, your post has successfully been created')
        return flask.redirect(flask.url_for('posts'))
    return flask.render_template('/post/create_post.html', title='Create Post', form=form)

# Launch Application

# Default port:


if __name__ == '__main__':
    app.run()

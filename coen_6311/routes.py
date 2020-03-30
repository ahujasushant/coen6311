# Imports

import flask
from coen_6311 import app
from coen_6311.forms import LoginForm, RegistrationForm, VolunteerLoginForm, VolunteerRegistrationForm, PostForm, VolunteerEditForm, OrganizationEditForm
from flask_login import current_user, login_user
from coen_6311.models import Volunteer, Organization, Post, History
from flask_login import logout_user
from flask import request, current_app, session, g, Blueprint
from werkzeug.urls import url_parse
from coen_6311 import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('auth', __name__, url_prefix='/auth')


# Controllers.

@app.route('/')
def home():
    return flask.render_template('dashboard/home.html')


@app.route('/about')
def about():
    return flask.render_template('dashboard/about_us.html')


@app.route('/donate')
def donate():
    return flask.render_template('dashboard/donate.html')


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
        return flask.redirect(flask.url_for('login'))
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

        session.clear()
        session['organization_id'] = organization.id
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = flask.url_for('posts')
        return flask.redirect(next_page)
    return flask.render_template('/login/login.html', title='Sign In', form=form)


@app.route('/register_volunteer', methods=['GET', 'POST'])
def register_vol():
    form = VolunteerRegistrationForm()
    if form.validate_on_submit():
        volunteer = Volunteer(email=form.email.data, name=form.name.data)
        volunteer.set_password(form.password.data)
        db.session.add(volunteer)
        db.session.commit()
        flask.flash('Congratulations, you successfully registered as a Volunteer!')
        return flask.redirect(flask.url_for('login_vol'))
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

        session.clear()
        session['volunteer_id'] = volunteer.id
        volunteer_id = session.get('volunteer_id')

        if volunteer_id is None:
            g.volunteer = None
            return flask.redirect(flask.url_for('home'))
        else:
            g.volunteer = Volunteer.query.get(volunteer_id)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = flask.url_for('about')
        return flask.redirect(next_page)
    return flask.render_template('/login/login_volunteer.html', title='Sign In', form=form)


@app.route('/edit_vol_profile', methods=['GET', 'POST', 'PUT'])
def edit_vol_profile():
    form = VolunteerEditForm()
    volunteer_id = session.get('volunteer_id')

    if volunteer_id is None:
        g.volunteer = None
        return flask.redirect(flask.url_for('home'))
    else:
        g.volunteer = Volunteer.query.get(volunteer_id)

    volunteer = g.volunteer

    if request.method == 'GET':
        return flask.render_template('/volunteer/edit.html', form=form, volunteer=volunteer)

    if volunteer is None:
        errors = flask.flash('Please Enter the valid details')
        return flask.render_template('/volunteer/show.html', volunteer=volunteer, errors=errors)

    volunteer.name = form.name.data
    volunteer.post_code = form.post_code.data
    db.session.commit()
    return flask.render_template('/volunteer/show.html', volunteer=volunteer)


@app.route('/vol_profile', methods=['GET'])
def vol_profile():
    volunteer_id = session.get('volunteer_id')

    if volunteer_id is None:
        g.volunteer = None
        return flask.redirect(flask.url_for('home'))
    else:
        g.volunteer = Volunteer.query.get(volunteer_id)

    volunteer = g.volunteer
    return flask.render_template('volunteer/show.html', volunteer=volunteer)


@app.route('/edit_org_profile', methods=['GET', 'POST', 'PUT'])
def edit_org_profile():
    form = OrganizationEditForm()
    organization_id = session.get('organization_id')

    if organization_id is None:
        g.organization = None
        return flask.redirect(flask.url_for('home'))
    else:
        g.organization = Organization.query.get(organization_id)

    organization = g.organization
    if request.method == 'GET':
        return flask.render_template('/organization/edit.html', form=form, organization=organization)

    if organization is None:
        errors = flask.flash('Please Enter the valid details')
        return flask.url_for('org_profile', organization=organization)

    organization.org_name = form.org_name.data
    organization.official_email = form.official_email.data
    organization.founded_in = form.founded_in.raw_data[0]
    db.session.commit()

    return flask.redirect(flask.url_for('org_profile'))


@app.route('/org_profile', methods=['GET'])
def org_profile():
    organization_id = session.get('organization_id')

    if organization_id is None:
        g.organization = None
        return flask.redirect(flask.url_for('home'))
    else:
        g.organization = Organization.query.get(organization_id)

    organization = g.organization
    return flask.render_template('organization/show.html', organization=organization)


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    return flask.redirect(flask.url_for('home'))


@bp.before_app_request
def load_logged_in_organization():
    organization_id = session.get('organization_id')

    if organization_id is None:
        g.organization = None
    else:
        g.organization = Organization.get(organization_id)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    organization_id = session.get('organization_id')

    if organization_id is None:
        g.organization = None
        return flask.redirect(flask.url_for('home'))
    else:
        g.organization = Organization.query.get(organization_id)

    posts = g.organization.posts.all()

    return flask.render_template('post/index.html', posts=posts, volunteers=volunteers)


@app.route('/volunteers', methods=['GET', 'POST'])
def volunteers():
    organization_id = session.get('organization_id')

    if organization_id is None:
        g.organization = None
        return flask.redirect(flask.url_for('home'))
    else:
        g.organization = Organization.query.get(organization_id)
    posts = g.organization.posts.all()
    volunteers = Volunteer.query.all()
    return flask.render_template('volunteer/index.html', volunteers=volunteers, posts=posts)


@app.route('/connectVolunteer', methods=['POST'])
def connect_volunteer():
    volunteer_id = int(request.form['volunteer_id'])
    post_id = int(request.form['post_id'])
    volunteer = Volunteer.query.get(volunteer_id)
    post = Post.query.get(post_id)
    history = History(location=post.location, author=volunteer)
    volunteer.author = post
    try:
        db.session.add(history)
        db.session.commit()

        flask.flash("History successfully created!")
    except IntegrityError:
        flask.flash("We are sorry, something went wrong.")

    return flask.redirect(flask.url_for('volunteers'))


@app.route('/volunteer_history', methods=['GET'])
def volunteer_history():
    organization_id = session.get('organization_id')

    if organization_id is None:
        g.organization = None
        return flask.redirect(flask.url_for('home'))
    else:
        g.organization = Organization.query.get(organization_id)
    organization = g.organization

    posts = organization.posts.all()

    vol_history = {}
    for post in posts:
        for volunteer in post.volunteers:
            vol_his = []
            for history in volunteer.history:
                vol_his.append(history.location)
            vol_history[volunteer] = vol_his

    return flask.render_template('/organization/volunteer_history.html', vol_history=vol_history)


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    organization_id = session.get('organization_id')

    if organization_id is None:
        g.organization = None
        return flask.redirect(flask.url_for('home'))
    else:
        g.organization = Organization.query.get(organization_id)

    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('about'))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(description=form.description.data, location=form.location.data, author=g.organization)
        db.session.add(post)
        db.session.commit()
        flask.flash('Congratulations, your post has successfully been created')
        return flask.redirect(flask.url_for('posts'))
    return flask.render_template('/post/create_post.html', title='Create Post', form=form)

# Launch Application

# Default port:


if __name__ == '__main__':
    app.run()

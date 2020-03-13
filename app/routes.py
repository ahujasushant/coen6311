# Imports

import flask
from forms import LoginForm
import os

app = flask.Flask(__name__)
app.config.from_object('config')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


# Controllers.

@app.route('/')
def home():
    return flask.render_template('dashboard/home.html')


@app.route('/about')
def about():
    return flask.render_template('dashboard/about_us.html')

@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flask.flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return flask.redirect('/index')
    return flask.render_template('/login/login.html', title='Sign In', form=form)
# Launch Application

# Default port:
if __name__ == '__main__':
    app.run()

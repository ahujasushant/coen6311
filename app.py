# Imports
#----------------------------------------------------------------------------#

import flask
import os

app = flask.Flask(__name__)
app.config.from_object('config')

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return flask.render_template('dashboard/home.html')


@app.route('/about')
def about():
    return flask.render_template('dashboard/about_us.html')

# Launch Application

# Default port:
if __name__ == '__main__':
    app.run()

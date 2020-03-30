import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'


from coen_6311 import models
from coen_6311.models import *
from coen_6311.routes import *


if __name__ == '__main__':
    app.run()
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

login = LoginManager(app)

login.login_view = 'login' # tells the login manager which endpoint to redirect
# if someone is accessing a part of the site when not logged in
login.login_message = 'You must be logged in to do that.'
login.login_message_category = 'danger'

from . import routes, models
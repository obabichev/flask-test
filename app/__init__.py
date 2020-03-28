import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)

from app import routes, errors

from app.models import User, Environment, Resource


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Environment': Environment, 'Resource': Resource}

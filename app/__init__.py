import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes

from app.models import User, Environment, Resource


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Environment': Environment, 'Resource': Resource}

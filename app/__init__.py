import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from logging.handlers import SMTPHandler
from sqlalchemy_utils import Ltree

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)

from app import routes, errors

from app.models import User, Environment, Resource, Tag


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,

        'User': User,
        'Environment': Environment,
        'Resource': Resource,
        'Tag': Tag,

        'Ltree': Ltree
    }


if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

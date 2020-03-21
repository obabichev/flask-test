import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes

from app.models import User

# def create_app():
#     app = Flask(__name__, instance_relative_config=True)
#
#     app.config.from_object(os.environ['APP_SETTINGS'])
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#
#     print("os.environ['APP_SETTINGS']", os.environ['APP_SETTINGS'])
#     print('SQLALCHEMY_DATABASE_URI', app.config['SQLALCHEMY_DATABASE_URI'])
#
#     @app.route('/hello')
#     def hello():
#         return 'Hello, World!!!!'
#
#     return app

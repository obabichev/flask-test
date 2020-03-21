import os

from flask import Flask

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app import routes

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

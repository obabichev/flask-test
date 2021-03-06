from datetime import datetime

from app import db
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import func
from sqlalchemy.sql import expression
from sqlalchemy_utils.types.ltree import LQUERY
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy_utils import LtreeType


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_environment = db.Table(
    'user_environment',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('environment_id', db.Integer, db.ForeignKey('environment.id'), primary_key=True)
)


class Environment(db.Model):
    __tablename__ = 'environment'

    id = db.Column(db.Integer, primary_key=True)
    resources = db.relationship('Resource', backref='environment', lazy=True)
    users = db.relationship('User', secondary=user_environment, lazy='subquery',
                            backref=db.backref('environments', lazy=True))

    def __repr__(self):
        return '<Environment {}>'.format(self.id)


class Resource(db.Model):
    __tablename__ = 'resource'

    id = db.Column(db.Integer, primary_key=True)
    environment_id = db.Column(db.Integer, db.ForeignKey('environment.id'), nullable=False)

    documents = db.relationship('Document', backref='resource', lazy=True)

    def __repr__(self):
        return '<Resource {}>'.format(self.id)


class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=True)
    document_type = db.Column(
        "document_type",
        ENUM("article", "court", "book", "magazine", "link", "other", name="document_type", create_type=False)
    )

    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)

    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), nullable=True)
    file = db.relationship('File', backref='documents', lazy=True)

    def __repr__(self):
        return '<Document {}>'.format(self.id)


class File(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String)
    file_type = db.Column("file_type", ENUM("pdf", "doc", "xls", name="file_type"))
    mimetype = db.Column(db.String(256))

    def __repr__(self):
        return '<File {}>'.format(self.id)


class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    path = db.Column(LtreeType, nullable=False)

    def get_direct_descendants(self):
        lquery = str(self.path) + '.*{1,1}'
        return Tag.query.filter(
            Tag.path.lquery(expression.cast(lquery, LQUERY))
        ).all()

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

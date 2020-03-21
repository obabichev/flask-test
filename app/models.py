from app import db
from sqlalchemy.dialects.postgresql import ENUM


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


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

    def __repr__(self):
        return '<File {}>'.format(self.id)

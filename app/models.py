from app import db


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


class Resource(db.Model):
    __tablename__ = 'resource'

    id = db.Column(db.Integer, primary_key=True)
    environment_id = db.Column(db.Integer, db.ForeignKey('environment.id'), nullable=False)

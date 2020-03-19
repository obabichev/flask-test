import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# from models import Book


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    published = db.Column(db.String())
    neu = db.Column(db.String())
    also = db.Column(db.String())

    def __init__(self, name, author, published, neu, also):
        self.name = name
        self.author = author
        self.published = published
        self.neu = neu
        self.also = also

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'published': self.published,
            'neu': self.neu,
            'also': self.also
        }


user_environment = db.Table(
    'user_environment',
    # db.Column(db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('environment_id', db.Integer, db.ForeignKey('environment.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


class Environment(db.Model):
    __tablename__ = 'environment'

    id = db.Column(db.Integer, primary_key=True)
    resources = db.relationship('Resource', backref='environment', lazy=True)
    users = db.relationship('User', secondary=user_environment, lazy='subquery',
                            backref=db.backref('environments', lazy=True))


class Resource(db.Model):
    __tablename__ = 'resource'

    id = db.Column(db.Integer, primary_key=True)
    environment_id = db.Column(db.Integer, db.ForeignKey('environment.id'),
                               nullable=False)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/add")
def add_book():
    name = request.args.get('name')
    author = request.args.get('author')
    published = request.args.get('published')
    try:
        book = Book(
            name=name,
            author=author,
            published=published
        )
        db.session.add(book)
        db.session.commit()
        return "Book added. book id={}".format(book.id)
    except Exception as e:
        return (str(e))


@app.route("/getall")
def get_all():
    try:
        books = Book.query.all()
        return jsonify([e.serialize() for e in books])
    except Exception as e:
        return (str(e))


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book = Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return (str(e))


@app.route("/add/form", methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        name = request.form.get('name')
        author = request.form.get('author')
        published = request.form.get('published')
        try:
            book = Book(
                name=name,
                author=author,
                published=published
            )
            db.session.add(book)
            db.session.commit()
            return "Book added. book id={}".format(book.id)
        except Exception as e:
            return (str(e))
    return render_template("getdata.html")


if __name__ == '__main__':
    app.run()

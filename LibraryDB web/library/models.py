from flask_login import UserMixin

from library import db, manager


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(225), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    order = db.relationship("Orders", cascade="all, delete")

class Readers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(225), nullable=False, unique=True)
    phone = db.Column(db.String(50), nullable=False, unique=True)
    card = db.Column(db.String(4), nullable=False, unique=True)
    order = db.relationship("Orders", cascade="all, delete")

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_date = db.Column(db.Date, nullable=False)
    second_date = db.Column(db.Date, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    reader_id = db.Column(db.Integer, db.ForeignKey('readers.id'), nullable=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
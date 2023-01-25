from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    passport = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(256), nullable=False)

class Tarifs(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Services(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    tarif_id = db.Column(db.Integer, db.ForeignKey('tarifs.id'), nullable=False)
    start_reserv = db.Column(db.Date, nullable=False)
    ends_reserv = db.Column(db.Date, nullable=False)
    room_id = db.Column(db.Integer, nullable=False)
    relation_clients = db.relationship("Clients")
    relation_tarifs = db.relationship("Tarifs")

class Options(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    relation_services = db.relationship("Services")
    relation_clients = db.relationship("Clients")




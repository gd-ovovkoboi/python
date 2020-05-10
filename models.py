from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from settings import app

db = SQLAlchemy(app)


class Center(db.Model):
    __tablename__ = 'centers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    login = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    animals = relationship(lambda: Animal)


class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    animals = relationship(lambda: Animal)


class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, ForeignKey(Center.id), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80))
    age = db.Column(db.Integer, nullable=False)
    species_id = db.Column(db.Integer, ForeignKey(Species.id), nullable=False)
    price = db.Column(db.Float)


class AccessLog(db.Model):
    __tablename__ = 'access_log'
    center_id = db.Column(db.Integer, nullable=False)
    time_stamp = db.Column(db.TIMESTAMP(), primary_key=True)

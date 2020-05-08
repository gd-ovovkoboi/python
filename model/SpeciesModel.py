import json

from flask_sqlalchemy import SQLAlchemy

from settings import app

db = SQLAlchemy(app)


class Species(db.Model):
    __tablename__ = 'species'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def json(self):
        return {'id': self.id, 'name': self.name, 'description': self.description, 'price': self.price}

    def add_species(self):
        new_species = Species(name=self.name, description=self.description, price=self.price)
        db.session.add(new_species)
        db.session.commit()

    def get_all_species(self):
        return [Species.json(species) for species in Species.query.all()]

    def get_species(self):
        return Species.query.filter_by(id=self.id).first()

    def __repr__(self):
        species_object = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
        }
        return json.dumps(species_object)

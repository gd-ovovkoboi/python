import json

from flask_sqlalchemy import SQLAlchemy

from settings import app

db = SQLAlchemy(app)


class Animal(db.Model):
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    center_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80))
    age = db.Column(db.Integer, nullable=False)
    species_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float)

    def json(self):
        return {'id': self.id, 'center_id': self.center_id, 'name': self.name,
                'description': self.description, 'age': self.age,
                'species_id': self.species_id, 'price': self.price}

    def add_animal(self):
        new_animal = Animal(center_id=self.center_id, name=self.name, description=self.description,
                            age=self.age, species_id=self.species_id, price=self.price)
        db.session.add(new_animal)
        db.session.commit()

    def get_all_animals(self):
        return [Animal.json(animals) for animals in Animal.query.all()]

    def get_animal(self, _id):
        return Animal.query.filter_by(id=_id).first()

    def update_animal(self):
        updated_animal = Animal.query.filter_by(id=self.id).first()
        updated_animal.center_id = self.center_id
        updated_animal.name = self.name
        updated_animal.description = self.description
        updated_animal.age = self.age
        updated_animal.species_id = self.species_id
        updated_animal.price = self.price
        db.session.commit()

    def delete_animal(self):
        Animal.query.filter_by(id=self.id).delete()
        db.session.commit()

    def __repr__(self):
        animal_object = {
            'id': self.id,
            'center_id': self.center_id,
            'name': self.name,
            'description': self.description,
            'age': self.age,
            'species_id': self.species_id,
            'price': self.price,
        }
        return json.dumps(animal_object)

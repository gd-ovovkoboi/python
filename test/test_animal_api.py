import json
import os
import unittest

from api.animal_api import animal_api
from models import *


class AnimalTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath('test.db')
        self.app = app.test_client()
        app.register_blueprint(animal_api)
        db.drop_all()
        db.create_all()

    def test_get_animals(self):
        cat = Animal(center_id=1, name='cat', description='cat in the boots', age=33, species_id=1, price=100500)
        dog = Animal(center_id=2, name='dog', description='husky', age=3, species_id=2, price=300)
        db.session.add(cat)
        db.session.add(dog)
        db.session.commit()

        response = self.app.get('/animals')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, json.loads("{\"animals\": [{\"id\": 1, \"name\": \"cat\", "
                                                   "\"description\": \"cat in the boots\", \"age\": 33, "
                                                   "\"price\": 100500.0}, {\"id\": 2, \"name\": \"dog\", "
                                                   "\"description\": \"husky\", \"age\": 3, \"price\": 300.0}]}"))

    def test_get_animal(self):
        cat = Animal(center_id=1, name='cat', description='cat in the boots', age=33, species_id=1, price=100500)
        db.session.add(cat)
        db.session.commit()

        response = self.app.get('/animals/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, json.loads("{\"id\": 1, \"name\": \"cat\", \"description\": "
                                                   "\"cat in the boots\", \"age\": 33, \"price\": 100500.0, "
                                                   "\"species_id\": 1, \"center_id\": 1}"))

    def test_auth_for_write_endpoints(self):
        response = self.app.post('/animals',json=json.loads("{}"))
        self.assertEqual(response.status_code, 403)

        response = self.app.put('/animals/1',json=json.loads("{}"))
        self.assertEqual(response.status_code, 403)

        response = self.app.delete('/animals/1')
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main()

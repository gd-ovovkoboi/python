from flask import jsonify, request, make_response, Blueprint

from models import *
from decorators import *

species_api = Blueprint('species_api', __name__)


# GET /species
@species_api.route('/species')
@log_decorator
def get_species():
    result = []
    for species in Species.query.all():
        species_info = {
            'name': species.name,
            'animal_count': len(species.animals),
        }
        result.append(species_info)
    return jsonify({'species': result})


# POST /species
@species_api.route('/species', methods=['POST'])
@log_decorator
def add_species():
    request_data = request.get_json()
    if valid_species_object(request_data):
        new_species = Species(name=request_data['name'], description=request_data['description'],
                              price=request_data['price'])
        db.session.add(new_species)
        db.session.commit()
        return make_response(jsonify({}), 201)
    else:
        return make_response(jsonify({'error': 'Invalid species object passed in request',
                                      'helpString': "Data passed in similar to this {'name': 'name', "
                                                    "'description': 'description', 'price': 5.88}"}), 400)


# GET /species/<int:id>
@species_api.route('/species/<int:id>')
@log_decorator
def get_animals_by_species_id(id):
    species = Species.query.filter_by(id=id).first()
    if species is not None:
        animals = []
        for animal in species.animals:
            animal_info = {
                'name': animal.name,
                'description': animal.description,
                'age': animal.age,
                'price': animal.price
            }
            animals.append(animal_info)
        species_info = {
            'name': species.name,
            'description': species.description,
            'animals': animals
        }
        return jsonify(species_info)
    else:
        return make_response(jsonify({
            'error': 'Invalid species ID',
            'helpString': 'Make sure species with ID {} exists'.format(id)}), 400)


def valid_species_object(species):
    return 'name' in species and 'description' in species and 'price' in species and isinstance(species['price'], float)

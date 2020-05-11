from flask import make_response, Blueprint

from decorators import *
from models import *

species_api = Blueprint('species_api', __name__)


# GET /species
@species_api.route('/species')
@log_request
def get_species():
    """Returns the collection of all species"""
    result = []
    for species in Species.query.all():
        species_info = {
            'name': species.name,
            'animal_count': len(species.animals),
        }
        result.append(species_info)
    return jsonify({'species': result})


# POST /species?token=uEam0vbBtaK8slCuk-RDakZSvtxDuUIfuQs0
@species_api.route('/species', methods=['POST'])
@token_required
@log_request
def add_species():
    """Creates a new species or returns bad request in case of invalid object"""
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
@log_request
def get_animals_by_species_id(id):
    """Returns detailed information regarding the species with the specified ID"""
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
    """Validates passed species object, returns true in case it is valid and false otherwise"""
    return 'name' in species and 'description' in species and 'price' in species and isinstance(species['price'], float)

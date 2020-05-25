from flask import make_response, Blueprint
from cerberus import Validator

from decorators import log_request, token_required
from flask import request, jsonify
from models import Species, db

species_api = Blueprint('species_api', __name__)

required_request_input = {'name': {'type': 'string', 'required': True},
                          'description': {'type': 'string', 'required': True},
                          'price': {'type': 'float', 'required': True}}


@species_api.route('/species')
@log_request
def get_species():
    """ GET /species
    Returns the collection of all species
    """
    result = []
    for species in Species.query.all():
        species_info = {
            'name': species.name,
            'animal_count': len(species.animals),
        }
        result.append(species_info)
    return jsonify({'species': result})


@species_api.route('/species', methods=['POST'])
@token_required
@log_request
def add_species():
    """ POST /species?token=uEam0vbBtaK8slCuk-RDakZSvtxDuUIfuQs0
    Creates a new species or returns bad request in case of invalid object
    """
    request_data = request.get_json()
    if Validator(required_request_input).validate(request_data):
        new_species = Species(name=request_data['name'], description=request_data['description'],
                              price=request_data['price'])
        db.session.add(new_species)
        db.session.commit()
        return make_response(jsonify({}), 201)
    else:
        return make_response(jsonify({'error': 'Invalid species object passed in request',
                                      'helpString': "Data passed in similar to this {'name': 'name', "
                                                    "'description': 'description', 'price': 5.88}"}), 400)


@species_api.route('/species/<int:id>')
@log_request
def get_animals_by_species_id(id):
    """ GET /species/<int:id>
    Returns detailed information regarding the species with the specified ID
    """
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

from flask import jsonify, request, make_response, Blueprint

from model.SpeciesModel import *
from model.AnimalModel import *

species_api = Blueprint('species_api', __name__)


# GET /species
@species_api.route('/species')
def get_species():
    return jsonify({'species': Species.get_all_species(Species())})


# POST /species
@species_api.route('/species', methods=['POST'])
def add_species():
    request_data = request.get_json()
    if valid_species_object(request_data):
        new_species = Species(name=request_data['name'], description=request_data['description'],
                              price=request_data['price'])
        Species.add_species(new_species)
        return make_response(jsonify({}), 201)
    else:
        return make_response(jsonify({'error': 'Invalid species object passed in request',
                                      'helpString': "Data passed in similar to this {'name': 'name', "
                                                    "'description': 'description', 'price': 5.88}"}), 400)


# GET /species/<int:id>
@species_api.route('/species/<int:id>')
def get_animals_by_species_id(id):
    return_value = []
    species = Species.get_species(Species(id=id))
    if species is not None:
        for animal in Animal.get_all_animals(Animal()):
            if animal['species_id'] == id:
                animal_info = {
                    'name': animal['name'],
                    'id': animal['id'],
                    'species': species.name
                }
                return_value.append(animal_info)
        return jsonify(return_value)
    else:
        return make_response(jsonify({
            'error': 'Invalid species ID',
            'helpString': 'Make sure species with ID {} exists'.format(id)}), 400)


def valid_species_object(species):
    return 'name' in species and 'description' in species and 'price' in species

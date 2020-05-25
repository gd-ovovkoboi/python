from cerberus import Validator
from flask import make_response, Blueprint
from flask import request, jsonify

from decorators import log_request, token_required
from models import Animal, db

animal_api = Blueprint('animal_api', __name__)

required_request_input = {'name': {'type': 'string', 'required': True},
                          'description': {'type': 'string', 'required': True},
                          'center_id': {'type': 'integer', 'required': True},
                          'age': {'type': 'integer', 'required': True},
                          'species_id': {'type': 'integer', 'required': True},
                          'price': {'type': 'float', 'required': True}}

invalid_animal_object_error_msg = {
    'error': 'Invalid animal object passed in request',
    'helpString': "Data passed in similar to this {'center_id': 5, 'name': 'name', "
                  "'description': 'description', 'age': 2, 'species_id': 2, 'price': 5.88}"
}


@animal_api.route('/animals')
@log_request
def get_animals():
    """ GET /animals
    Returns the collection of all animals
    """
    result = []
    for animal in Animal.query.all():
        animal_info = {
            'id': animal.id,
            'name': animal.name,
            'description': animal.description,
            'age': animal.age,
            'price': animal.price,
        }
        result.append(animal_info)
    return jsonify({'animals': result})


@animal_api.route('/animals/<int:id>')
@log_request
def get_animal_by_id(id):
    """ GET /animals/<int:id>
    Returns detailed information regarding the animal with the specified ID
    """
    animal = Animal.query.filter_by(id=id).first()
    if animal is not None:
        animal_info = {
            'id': animal.id,
            'name': animal.name,
            'description': animal.description,
            'age': animal.age,
            'price': animal.price,
            'species_id': animal.species_id,
            'center_id': animal.center_id
        }
        return jsonify(animal_info)
    else:
        return make_response(jsonify({
            'error': 'Invalid animal ID',
            'helpString': 'Make sure animal with ID {} exists'.format(id)}), 400)


@animal_api.route('/animals', methods=['POST'])
@token_required
@log_request
def add_animal():
    """ POST /animals?token=uEam0vbBtaK8slCuk-RDakZSvtxDuUIfuQs0
    Creates a new animal or returns bad request in case of invalid object
    """
    request_data = request.get_json()
    if Validator(required_request_input).validate(request_data):
        new_animal = Animal(center_id=request_data['center_id'], name=request_data['name'],
                            description=request_data['description'], age=request_data['age'],
                            species_id=request_data['species_id'], price=request_data['price'])
        db.session.add(new_animal)
        db.session.commit()
        return make_response(jsonify({}), 201)
    else:
        return make_response(jsonify(invalid_animal_object_error_msg), 400)


@animal_api.route('/animals/<int:id>', methods=['PUT'])
@token_required
@log_request
def replace_animal(id):
    """ PUT /animals/<int:id>?token=uEam0vbBtaK8slCuk-RDakZSvtxDuUIfuQs0
    Rewrites existing animal or returns bad request in case of invalid object
    """
    request_data = request.get_json()
    if Validator(required_request_input).validate(request_data):
        updated_animal = Animal.query.filter_by(id=id).first()
        updated_animal.id = id
        updated_animal.center_id = request_data['center_id']
        updated_animal.name = request_data['name']
        updated_animal.description = request_data['description']
        updated_animal.age = request_data['age']
        updated_animal.species_id = request_data['species_id']
        updated_animal.price = request_data['price']
        db.session.commit()
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify(invalid_animal_object_error_msg), 400)


@animal_api.route('/animals/<int:id>', methods=['DELETE'])
@token_required
@log_request
def delete_book(id):
    """ DELETE /animals/<int:id>?token=uEam0vbBtaK8slCuk-RDakZSvtxDuUIfuQs0
    Deletes animal with the specified ID
    """
    Animal.query.filter_by(id=id).delete()
    db.session.commit()
    return make_response(jsonify({}), 204)

from flask import make_response, Blueprint

from decorators import *
from models import *

animal_api = Blueprint('animal_api', __name__)

invalid_animal_object_error_msg = {
    'error': 'Invalid animal object passed in request',
    'helpString': "Data passed in similar to this {'center_id': 5, 'name': 'name', "
                  "'description': 'description', 'age': 2, 'species_id': 2, 'price': 5.88}"
}


# GET /animals
@animal_api.route('/animals')
@log_request
def get_animals():
    """Returns the collection of all animals"""
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


# GET /animals/<int:id>
@animal_api.route('/animals/<int:id>')
@log_request
def get_animal_by_id(id):
    """Returns detailed information regarding the animal with the specified ID"""
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


# POST /animals?token=uEam0vbBtaK8slCuk-RDakZSvtxDuUIfuQs0
@animal_api.route('/animals', methods=['POST'])
@token_required
@log_request
def add_animal():
    """Creates a new animal or returns bad request in case of invalid object"""
    request_data = request.get_json()
    if valid_animal_object(request_data):
        new_animal = Animal(center_id=request_data['center_id'], name=request_data['name'],
                            description=request_data['description'], age=request_data['age'],
                            species_id=request_data['species_id'], price=request_data['price'])
        db.session.add(new_animal)
        db.session.commit()
        return make_response(jsonify({}), 201)
    else:
        return make_response(jsonify(invalid_animal_object_error_msg), 400)


# PUT /animals/<int:id>?token=uEam0vbBtaK8slCuk-RDakZSvtxDuUIfuQs0
@animal_api.route('/animals/<int:id>', methods=['PUT'])
@token_required
@log_request
def replace_animal(id):
    """Rewrites existing animal or returns bad request in case of invalid object"""
    request_data = request.get_json()
    if valid_animal_object(request_data):
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


# DELETE /animals/<int:id>?token=uEam0vbBtaK8slCuk-RDakZSvtxDuUIfuQs0
@animal_api.route('/animals/<int:id>', methods=['DELETE'])
@token_required
@log_request
def delete_book(id):
    """Deletes animal with the specified ID"""
    Animal.query.filter_by(id=id).delete()
    db.session.commit()
    return make_response(jsonify({}), 204)


def valid_animal_object(animal):
    """Validates passed animal object, returns true in case it is valid and false otherwise"""
    return 'center_id' in animal and 'name' in animal and 'description' in animal \
           and 'age' in animal and isinstance(animal['age'], int) \
           and 'species_id' in animal and 'price' in animal and isinstance(animal['price'], float)

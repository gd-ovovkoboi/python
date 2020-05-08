from flask import jsonify, request, make_response, Blueprint

from model.AnimalModel import *

animal_api = Blueprint('animal_api', __name__)

invalid_animal_object_error_msg = {
    'error': 'Invalid animal object passed in request',
    'helpString': "Data passed in similar to this {'center_id': 5, 'name': 'name', "
                  "'description': 'description', 'age': 2, 'species_id': 2, 'price': 5.88}"
}


# GET /animals
@animal_api.route('/animals')
def get_animals():
    return jsonify({'animals': Animal.get_all_animals(Animal())})


# GET /animals/<int:id>
@animal_api.route('/animals/<int:id>')
def get_animal_by_id(id):
    animal = Animal.get_animal(Animal(), id)
    if animal is not None:
        return_value = {
            'id': animal.id,
            'name': animal.name,
            'description': animal.description,
            'age': animal.age,
            'price': animal.price,
            'species_id': animal.species_id,
            'center_id': animal.center_id
        }
        return jsonify(return_value)
    else:
        return make_response(jsonify({
            'error': 'Invalid animal ID',
            'helpString': 'Make sure animal with ID {} exists'.format(id)}), 400)


# POST /animals
@animal_api.route('/animals', methods=['POST'])
def add_animal():
    request_data = request.get_json()
    if valid_animal_object(request_data):
        new_animal = Animal(center_id=request_data['center_id'], name=request_data['name'],
                            description=request_data['description'], age=request_data['age'],
                            species_id=request_data['species_id'], price=request_data['price'])
        Animal.add_animal(new_animal)
        return make_response(jsonify({}), 201)
    else:
        return make_response(jsonify(invalid_animal_object_error_msg), 400)


# PUT /animals/<int:id>
@animal_api.route('/animals/<int:id>', methods=['PUT'])
def replace_animal(id):
    request_data = request.get_json()
    if valid_animal_object(request_data):
        updated_animal = Animal(center_id=request_data['center_id'], name=request_data['name'],
                                description=request_data['description'], age=request_data['age'],
                                species_id=request_data['species_id'], price=request_data['price'])
        updated_animal.id = id
        Animal.update_animal(updated_animal)
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify(invalid_animal_object_error_msg), 400)


# DELETE /animals/<int:id>
@animal_api.route('/animals/<int:id>', methods=['DELETE'])
def delete_book(id):
    Animal.delete_animal(Animal(id=id))
    return make_response(jsonify({}), 204)


def valid_animal_object(animal):
    return 'center_id' in animal and 'name' in animal and 'description' in animal \
           and 'age' in animal and 'species_id' in animal and 'price' in animal

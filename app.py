from flask import Flask, jsonify, request, make_response

app = Flask(__name__)
centers = [
    {
        'login': 'center1',
        'password': 'password',
        'id': 1,
        'address': 'Krakow, al. 3 Maja 9'
    },
    {
        'login': 'center2',
        'password': 'password',
        'id': 2,
        'address': 'Wroclaw, ul. Kwitkowa 7'
    }
]
species = [
    {
        'id': 1,
        'name': 'Birds',
        'description': 'Birds',
        'price': 9.99
    },
    {
        'id': 2,
        'name': 'Mammals',
        'description': 'Cats and dogs',
        'price': 29.99
    }
]
animals = [
    {
        'id': 1,
        'center_id': 1,
        'name': 'Parrot',
        'description': 'Parrot',
        'age': 3,
        'species_id': 1,
        'price': 9.99
    },
    {
        'id': 2,
        'center_id': 1,
        'name': 'Cat',
        'description': 'Cat',
        'age': 1,
        'species_id': 2,
        'price': 25.99
    },
    {
        'id': 3,
        'center_id': 1,
        'name': 'Parrot',
        'description': 'Parrot',
        'age': 5,
        'species_id': 1,
        'price': 19.99
    },
    {
        'id': 4,
        'center_id': 1,
        'name': 'Dog',
        'description': 'Dog',
        'age': 2,
        'species_id': 2,
        'price': 45.99
    }
]
invalid_animal_object_error_msg = {
    'error': 'Invalid animal object passed in request',
    'helpString': "Data passed in similar to this {'center_id': 5, 'name': 'name', "
                  "'description': 'description', 'age': 2, 'species_id': 2, 'price': 5.88}"
}


# GET /species
@app.route('/species')
def get_books():
    return jsonify({'species': species})


# GET /species/<int:id>
@app.route('/species/<int:id>')
def get_animals_by_species_id(id):
    return_value = []
    species_name = get_species_name_by_id(id)
    for animal in animals:
        if animal['species_id'] == id:
            animal_info = {
                'name': animal['name'],
                'id': animal['id'],
                'species': species_name
            }
            return_value.append(animal_info)
    return jsonify(return_value)


# GET /centers
@app.route('/centers')
def get_centers():
    return jsonify({'centers': centers})


# GET /centers/<int:id>
@app.route('/centers/<int:id>')
def get_center_by_id(id):
    return_value = {}
    for center in centers:
        if center['id'] == id:
            return_value = {
                'address': center['address']
            }
    return jsonify(return_value)


# GET /animals
@app.route('/animals')
def get_animals():
    return jsonify({'animals': animals})


# GET /animals/<int:id>
@app.route('/animals/<int:id>')
def get_animal_by_id(id):
    return_value = {}
    for animal in animals:
        if animal['id'] == id:
            return_value = animal
    return jsonify(return_value)


# POST /animals
@app.route('/animals', methods=['POST'])
def add_animal():
    request_data = request.get_json()
    if valid_animal_object(request_data):
        new_animal = {
            'id': request_data['id'],
            'center_id': request_data['center_id'],
            'name': request_data['name'],
            'description': request_data['description'],
            'age': request_data['age'],
            'species_id': request_data['species_id'],
            'price': request_data['price']
        }
        animals.append(new_animal)
        return make_response(jsonify({}), 201)
    else:
        return make_response(jsonify(invalid_animal_object_error_msg), 400)


# PUT /animals/<int:id>
@app.route('/animals/<int:id>', methods=['PUT'])
def replace_animal(id):
    request_data = request.get_json()
    if not valid_animal_object(request_data):
        return make_response(jsonify(invalid_animal_object_error_msg), 400)

    new_animal = {
        'id': id,
        'center_id': request_data['center_id'],
        'name': request_data['name'],
        'description': request_data['description'],
        'age': request_data['age'],
        'species_id': request_data['species_id'],
        'price': request_data['price']
    }
    i = 0
    for animal in animals:
        if animal['id'] == id:
            animals[i] = new_animal
        i += 1
    return make_response(jsonify({}), 204)


# DELETE /animals/<int:id>
@app.route('/animals/<int:id>', methods=['DELETE'])
def delete_book(id):
    for animal in animals:
        if animal['id'] == id:
            animals.remove(animal)
            return make_response(jsonify({}), 204)

    return make_response(jsonify({"error": "ID not found"}), 404)


def valid_animal_object(animal):
    return 'center_id' in animal and 'name' in animal and 'description' in animal \
           and 'species_id' in animal and 'price' in animal


def get_species_name_by_id(id):
    for s in species:
        if (s['id'] == id):
            return s['name']


app.run(port=5000)

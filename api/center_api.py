from flask import jsonify, request, make_response, Blueprint

from models import *
from decorators import *

center_api = Blueprint('center_api', __name__)


# GET /centers
@center_api.route('/centers')
@log_decorator
def get_centers():
    result = []
    for center in Center.query.all():
        center_info = {
            'name': center.name,
            'address': center.address,
        }
        result.append(center_info)
    return jsonify({'centers': result})


# POST /centers
@center_api.route('/centers', methods=['POST'])
@log_decorator
def add_center():
    request_data = request.get_json()
    if valid_center_object(request_data):
        new_center = Center(name=request_data['name'], login=request_data['login'],
                            password=request_data['password'], address=request_data['address'])
        db.session.add(new_center)
        db.session.commit()
        return make_response(jsonify({}), 201)
    else:
        return make_response(jsonify({
            'error': 'Invalid center object passed in request',
            'helpString': "Data passed in similar to this {'name': 'name', 'login': 'login', "
                          "'password': 'password', 'address': 'Krakow, ul ..'}"}), 400)


# GET /centers/<int:id>
@center_api.route('/centers/<int:id>')
@log_decorator
def get_center_by_id(id):
    center = Center.query.filter_by(id=id).first()
    if center is not None:
        animals = []
        for animal in center.animals:
            animal_info = {
                'name': animal.name,
                'description': animal.description,
                'age': animal.age,
                'price': animal.price
            }
            animals.append(animal_info)
        center_info = {
            'name': center.name,
            'address': center.address,
            'animals': animals
        }
        return jsonify(center_info)
    else:
        return make_response(jsonify({
            'error': 'Invalid center ID',
            'helpString': 'Make sure center with ID {} exists'.format(id)}), 400)


def valid_center_object(center):
    return 'name' in center and 'login' in center and 'password' in center and 'address' in center

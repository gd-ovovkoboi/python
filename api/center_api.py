from cerberus import Validator
from flask import make_response, Blueprint
from flask import request, jsonify

from decorators import log_request
from models import Center, db

center_api = Blueprint('center_api', __name__)

required_request_input = {'name': {'type': 'string', 'required': True},
                          'login': {'type': 'string', 'required': True},
                          'password': {'type': 'string', 'required': True},
                          'address': {'type': 'string', 'required': True}}


@center_api.route('/centers')
@log_request
def get_centers():
    """ GET /centers
    Returns the collection of all centers
    """
    result = []
    for center in Center.query.all():
        center_info = {
            'name': center.name,
            'address': center.address,
        }
        result.append(center_info)
    return jsonify({'centers': result})


@center_api.route('/register', methods=['POST'])
@log_request
def add_center():
    """ POST /register
    Creates a new center or returns bad request in case of invalid object
    """
    request_data = request.get_json()
    if Validator(required_request_input).validate(request_data):
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


@center_api.route('/centers/<int:id>')
@log_request
def get_center_by_id(id):
    """ GET /centers/<int:id>
    Returns detailed information regarding the center with the specified ID
    """
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

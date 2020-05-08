from flask import jsonify, request, make_response, Blueprint

from model.CenterModel import *

center_api = Blueprint('center_api', __name__)


# GET /centers
@center_api.route('/centers')
def get_centers():
    return jsonify({'centers': Center.get_all_centers(Center())})


# POST /centers
@center_api.route('/centers', methods=['POST'])
def add_center():
    request_data = request.get_json()
    if valid_center_object(request_data):
        new_center = Center(login=request_data['login'], password=request_data['password'],
                            address=request_data['address'])
        Center.add_center(new_center)
        return make_response(jsonify({}), 201)
    else:
        return make_response(jsonify({
            'error': 'Invalid center object passed in request',
            'helpString': "Data passed in similar to this {'login': 'login', "
                          "'password': 'password', 'address': 'Krakow, ul ..'}"}), 400)


# GET /centers/<int:id>
@center_api.route('/centers/<int:id>')
def get_center_by_id(id):
    center = Center.get_center(Center(), id)
    if center is not None:
        return_value = {
            'address': center.address,
        }
        return jsonify(return_value)
    else:
        return make_response(jsonify({
            'error': 'Invalid center ID',
            'helpString': 'Make sure center with ID {} exists'.format(id)}), 400)


def valid_center_object(center):
    return 'login' in center and 'password' in center and 'address' in center

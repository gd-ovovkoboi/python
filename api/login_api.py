import datetime

from flask import Blueprint, make_response

from decorators import *
from models import Center

login_api = Blueprint('login_api', __name__)


# POST /login
@login_api.route('/login', methods=['POST'])
@log_request
def get_token():
    request_data = request.get_json()
    user = Center.query.filter_by(login=request_data['login']).filter_by(password=request_data['password']).first()
    if user is not None:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=app.config['SESSION_DURATION_MIN'])
        return jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'])
    else:
        return make_response(jsonify({'error': 'Incorrect login or password'}), 403)

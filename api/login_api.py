import datetime

from flask import Blueprint, make_response

from decorators import *
from models import *

login_api = Blueprint('login_api', __name__)


# POST /login
@login_api.route('/login', methods=['POST'])
@log_request
def get_token():
    request_data = request.get_json()
    center = Center.query.filter_by(login=request_data['login']).filter_by(password=request_data['password']).first()
    if center is not None:
        access_log_record = AccessLog(center_id=center.id, time_stamp=datetime.datetime.utcnow())
        db.session.add(access_log_record)
        db.session.commit()
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=app.config['SESSION_DURATION_MIN'])
        return jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'])
    else:
        return make_response(jsonify({'error': 'Incorrect login or password'}), 403)

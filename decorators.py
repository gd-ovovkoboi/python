from functools import wraps

import jwt
from flask import request, jsonify

from configuration import app


def log_request(fn):
    """Decorator function to log API request info"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            app.logger.debug('\n Method: {} \n URL: {}\n Body: {}'.format(request.method, request.url, request.json))
            return fn(*args, **kwargs)
        except Exception as ex:
            app.logger.debug("Exception {0}".format(ex))
            raise ex

    return wrapper


def token_required(fn):
    """Decorator function to check if valid JWT token was provided before performing an API call"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return fn(*args, **kwargs)
        except Exception as ex:
            return jsonify({'error': 'Need a valid token to access this endpoint'}), 403

    return wrapper

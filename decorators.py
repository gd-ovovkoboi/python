from functools import wraps

from flask import request

from configuration import app


def log_decorator(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        try:
            app.logger.debug('\n Method: {} \n URL: {}\n Body: {}'.format(request.method, request.url, request.json))
            return fn(*args, **kwargs)
        except Exception as ex:
            app.logger.debug("Exception {0}".format(ex))
            raise ex

    return decorated

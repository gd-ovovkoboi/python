import functools

from flask import request

from configuration import app


def log_decorator(fn):
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        try:
            app.logger.debug('\n Method: {} \n URL: {}\n Body: {}'.format(request.method, request.url, request.json))
            result = fn(*args, **kwargs)
            return result
        except Exception as ex:
            app.logger.debug("Exception {0}".format(ex))
            raise ex
    return decorated

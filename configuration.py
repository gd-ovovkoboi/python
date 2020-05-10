import os, logging
from logging.config import dictConfig

from flask import Flask

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': 'app.log',
            'mode': 'w',
            'encoding': 'utf-8'
        }
    },
    'root': {
        'handlers': ['file', 'wsgi'],
        'level': 'DEBUG'
    }
})

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

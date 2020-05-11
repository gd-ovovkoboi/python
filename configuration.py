import json
import logging
import os
from configparser import ConfigParser
from logging.config import dictConfig

from flask import Flask

with open('log_config.json') as f:
    config_dict = json.load(f)
    logging.config.dictConfig(config_dict)

parser = ConfigParser()
parser.read('config.ini')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(parser.get('db', 'db_file'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = parser.getboolean('db', 'track_modifications')
app.config['JSON_SORT_KEYS'] = parser.getboolean('settings', 'json_sort_keys')
app.config['SECRET_KEY'] = parser.get('settings', 'secret_key')
app.config['SESSION_DURATION_MIN'] = parser.getint('settings', 'session_duration_min')

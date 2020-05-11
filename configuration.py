import os, logging, json
from logging.config import dictConfig
from configparser import ConfigParser

from flask import Flask

with open('log_config.json') as f:
    config_dict = json.load(f)
    logging.config.dictConfig(config_dict)

parser = ConfigParser()
parser.read('config.ini')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(parser.get('db', 'db_file'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = parser.getboolean('db', 'track_modifications')
app.config['JSON_SORT_KEYS'] = parser.getboolean('rest', 'json_sort_keys')

import os

from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

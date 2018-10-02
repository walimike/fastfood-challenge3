import flask
from api.config import app_config

app = flask.Flask(__name__)

from api.views import admin,auth
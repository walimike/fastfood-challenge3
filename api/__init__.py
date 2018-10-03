import flask
from api.config import app_config
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)


app = flask.Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'walimike' 
jwt = JWTManager(app)

from api.views import admin,auth,user


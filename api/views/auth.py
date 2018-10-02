from flask import Flask, jsonify, request
from api import create_app
from api.models.dbcontroller import DbController
from api.models.models import User
import re
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from api.views import app

app.config['JWT_SECRET_KEY'] = 'walimike' 
jwt = JWTManager(app)

"""This route provides a welcome message for our api"""
@app.route('/')
def index():
    return "<h1> Welcome to Fast Food Fast </h1>"

"""This route is for user signup/in"""
@app.route('/v2/auth/signup', methods=['POST'])
@jwt_required
def signup():
    """{"name":"","password":"","role":""}"""
    if not request.json or not 'name' in request.json or not 'password' in request.json or not 'role' in request.json:
        error (400)

    if not isinstance(request.json.get('name'), str):
        return jsonify({"msg": "Name must be a string. Example: johndoe"}), 400

    name = request.get_json()['name'].strip()
    if not name:
        return jsonify({"msg": "Name field is empty"}), 400
    password = str(request.get_json()['password']).strip()

    role = request.get_json()['role']
    if not role:
        return jsonify({"msg":"Role field is empty"}), 400
    if role.lower() != "admin":
        if role.lower() != "user":
            return jsonify({"Error":"Only 'admin' or 'user' roles exist"})

    if name and password and role:
        if len(name) > 15:
            return jsonify({"msg": "Name is too long, max 15"}), 400

        if not re.match(r'^[a-z0-9_]+$', name):
            return jsonify({"msg": "Name can only contain lowercase a-z, 0-9 and _"}), 400

        if len(password) < 8:
            return jsonify({"msg": "Password too short, min 8 chars"}), 400

        if len(password) > 20:
            return jsonify({"msg": "Password too long, max 20"}), 400

        new_user = User(name, password, role)
        DbController().add_user(new_user)

    return jsonify({"msg": "empty field"}), 400

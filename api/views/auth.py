from flask import Flask
import jsonify
from api import create_app
from api.models.dbcontroller import DbController
from api.models.models import User
import re

from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from werkzeug.security import check_password_hash, generate_password_hash

app = create_app(config_name='development')

"""This route provides a welcome message for our api"""
@app.route('/')
def index():
    return "<h1> Welcome to Fast Food Fast </h1>"

"""This route is for user signup/in"""
@app.route('/v2/auth/signup', methods=['POST'])
def signup():
    if not request.json:
        error (400)

    if not isinstance(request.json.get('name'), str):
        return jsonify({"msg": "Name must be a string. Example: johndoe"}), 400

    name = request.json.get('name').strip()
    if not name:
        return jsonify({"msg": "Name field is empty"}), 400
    password = str(request.json.get('password')).strip()

    role = request.json.get('role')
    if not role:
        return jsonify({"msg":"Role field is empty"}), 400
    
    if email and name and password and role:
        if not re.match(r'^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            return jsonify({"msg": "Invalid email. Example: john@exam.com"}), 400

        if len(name) > 15:
            return jsonify({"msg": "Name is too long, max 15"}), 400

        if not re.match(r'^[a-z0-9_]+$', name):
            return jsonify({"msg": "Name can only contain lowercase a-z, 0-9 and _"}), 400

        if len(password) < 8:
            return jsonify({"msg": "Password too short, min 8 chars"}), 400

        if len(password) > 12:
            return jsonify({"msg": "Password too long, max 12"}), 400

        new_user = User(name, generate_password_hash(password), role)
        DbController().add_user(new_user)

        return new_user.insert_new_record()

    return jsonify({"msg": "empty field"}), 400    
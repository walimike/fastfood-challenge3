from flask import Flask, jsonify, request, abort
from api.models.models import User
import re
from api import app, db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity)


"""This route provides a welcome message for our api"""
@app.route('/')
def index():
    return "<h1> Welcome to Fast Food Fast </h1>"

"""This route is for user signup/in"""
@app.route('/auth/signup', methods=['POST'])
def signup():
    """{"name":"","password":"","role":""}"""
    if not request.json or not 'name' in request.json or not 'password' in request.json or not 'role' in request.json:
        abort (400)

    if not isinstance(request.json.get('name'), str):
        return jsonify({"msg": "Name must be a string."}), 400

    name = request.get_json()['name'].strip()
    if not name:
        return jsonify({"msg": "Name field is empty"}), 400
    password = str(request.get_json()['password']).strip()

    role = request.get_json()['role']
    if not role:
        return jsonify({"msg":"Role field is empty"}), 400
    if role.lower() != "user":
        return jsonify({"Error":"Only 'user' roles exist"})

    if name and password and role:
        if len(name) > 15:
            return jsonify({"msg": "Name is too long, max 15"}), 400

        if not re.match(r'^[a-z0-9_]+$', name):
            return jsonify({"msg": "Name can only contain lowercase a-z, 0-9 and _"}), 400

        if len(password) < 8:
            return jsonify({"msg": "Password too short, min 8 chars"}), 400

        if len(password) > 20:
            return jsonify({"msg": "Password too long, max 20"}), 400

        if db.get_user(name):
            return jsonify({"Error":"User already exists"})
        new_user = User(name, password, role)
        db.add_user(new_user)
        return jsonify({"Message":"You have successfully signed up."}),201

    return jsonify({"msg": "empty field"}), 400


@app.route('/auth/login', methods=['POST'])
def login():
    """{"name":"","password":"","role":""}"""
    
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('name', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    new_user = db.get_user(username)
    
    if not new_user:
        return jsonify({"Error":"User does not exist"}),404

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=new_user)
    return jsonify(access_token=access_token), 200
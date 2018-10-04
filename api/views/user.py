from flask import Flask,jsonify, request, abort, make_response
from api import app, db
from api.models.models import User
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)


@app.route('/users/orders',methods=['POST'])
@jwt_required
def make_order():
    """{"order":"","price":""}"""
    if not request.json or not 'order' in request.json or not 'price' in request.json:
        abort (400)

    if not isinstance(request.json.get('order'), str):
        return jsonify({"msg": "Food name must be a string."}), 400

    if not isinstance(request.json.get('price'), int):
        return jsonify({"msg": "Food price must be a integer."}), 400
    order = request.get_json()['order'].strip()
    if not order:
        return jsonify({"msg": "order field is empty"}), 400
    price = request.get_json()['price']
    if not price:
        return jsonify({"msg": "order field is empty"}), 400
    db.place_order(order,price,"Incomplete")    
    order = db.get_orders()
    return jsonify({"orders":order})  

@app.route('/user/menu',methods=['GET'])
@jwt_required
def get_menu():
    return jsonify({"Menu":db.get_menu()}) 


@app.route('/users/orders',methods=['GET'])
@jwt_required
def view_history(user_id):
    if not user_id:
        abort (404)
    return jsonify({"History":db.get_history_by_userid(user_id)})

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

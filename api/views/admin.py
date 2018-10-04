from flask import Flask,jsonify,json,request,abort,make_response
from api import app
from api.models.models import User
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from api import db

@app.route('/orders', methods=['GET'])
@jwt_required
def get_orders():
    identity = get_jwt_identity()[0]['username']
    if identity != 'superman':
        return jsonify({"Not authorized":"You do not have this access"}),401
    return jsonify({"orders":db.get_orders})

@app.route('/menu', methods=['POST'])
@jwt_required
def add_item_to_menu(): 
    """{"order":"","price":""}""" 
    identity = get_jwt_identity()[0]['username']
    if identity != 'superman':
        return jsonify({"Not authorized":"You do not have this access"}),401
    if not request.get_json() or not 'order' in request.get_json() or not 'price' in request.get_json():
        abort (404)
    order = request.get_json()['order'].strip()
    if not order:
        return jsonify({"msg": "Order field is empty"}), 400
    price = request.get_json()['price']
    if type(price) != int:
        return jsonify({"msg": "Price must be an integer"}), 400
    db.add_food_to_menu(order,price)
    menu = db.get_menu()
    return jsonify({"menu":menu})

@app.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required
def get_specific_order(order_id):
    if not order_id or type(order_id) != int:
        abort(400)
    specific_order = db.get_an_order(order_id,order_id)    
    return jsonify({"orders":specific_order})    

@app.route('/orders/<int:order_id>', methods=['PUT'])
@jwt_required
def update_order(order_id):
    if not type(order_id)==int:
        abort(400)

    """checks the the json data is in the right format and has the right key word"""    
    if not request.json or not 'completed_status' in request.json:
        abort(400)      
    new_status =  request.get_json()['completed_status']

    """checks that our completed status is either yes or no"""    
    if new_status.lower() != "complete":
        if new_status.lower() != "incomplete":
            return({"Error":"Status can only be complete or incomplete"})
    db.update_status(order_id,new_status)
    return jsonify({"orders":db.get_orders()})    


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 404)    

from flask import Flask,jsonify,json,request,abort,make_response
from api.models.dbcontroller import DbController
from api import app
from api.models.models import User


@app.route('/v2/admin/menu', methods=['GET'])
def get_orders():
    return jsonify({"orders":DbController().get_orders()})

@app.route('/v2/admin/menu', methods=['POST'])
def add_item_to_menu():   
    if not request.get_json() or not 'order' in request.get_json() or not 'price' in request.get_json():
        abort (404)
    order = request.get_json()['order'].strip()
    if not order:
        return jsonify({"msg": "Order field is empty"}), 400
    price = request.get_json()['price']
    if type(price) != int:
        return jsonify({"msg": "Price must be an integer"}), 400
    DbController().add_food_to_menu(order,price)
    menu = DbController().get_menu()
    return jsonify({"menu":menu})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 404)    

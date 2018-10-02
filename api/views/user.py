from flask import Flask,jsonify, request, abort, make_response
from api.models.dbcontroller import DbController
from api import app
from api.models.models import User

@app.route('/v2/user/orders',methods=['POST'])
def make_order():
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
    DbController().add_food_to_menu(order,price)    
    order = DbController().get_orders()
    return jsonify({"orders":order})    


@app.route('/v2/user/orders/<int:user_id>',methods=['GET'])
def view_history(user_id):
    if not user_id:
        abort (404)
    return jsonify({"History":DbController().get_history_by_userid(user_id)})

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

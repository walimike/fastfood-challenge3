from flask import Flask,jsonify
from api.models.dbcontroller import DbController
from api import app
from api.models.models import User


@app.route('/v2/admin/menu', methods=['GET'])
def get_orders():
    return jsonify({"orders":DbController().get_orders()})

    

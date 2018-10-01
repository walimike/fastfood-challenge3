from flask import Flask
import jsonify
from api import create_app

app = create_app(config_name='development')

"""This route provides a welcome message for our api"""
@app.route('/')
def index():
    return "<h1> Welcome to Fast Food Fast </h1>"
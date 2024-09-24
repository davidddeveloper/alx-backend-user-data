#!/usr/bin/env python3
"""
    module: basic flask app
"""
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Bienvenue"}), 200

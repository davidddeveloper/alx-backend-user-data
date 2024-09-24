#!/usr/bin/env python3
"""
    module: basic flask app
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=['POST'])
def users():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify(
            {"message": "email already registered"}
        ), 200

    return jsonify(
        {"email": user.email, "message": "user created"}
    ), 200


AUTH = Auth()
if __name__ == '__main__':
    app.run()
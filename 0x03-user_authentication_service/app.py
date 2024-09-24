#!/usr/bin/env python3
"""
    module: basic flask app
"""
from flask import Flask, jsonify, request, make_response
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


@app.route("/sessions")
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        abort(401)
    if not password:
        abort(401)

    session_id = AUTH.create_session(email)
    if session_id:
        response = make_response(
            jsonify(
                {"email": email, "message": "logged in"}
            ))
        response.set_cookie("session_id", session_id)
        return response


AUTH = Auth()
if __name__ == '__main__':
    app.run()

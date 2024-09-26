#!/usr/bin/env python3
"""
    module: basic flask app
"""
from flask import Flask, jsonify, request, make_response
from flask import abort, redirect
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


@app.route("/sessions", methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        abort(401)
    if not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if session_id:
        response = make_response(
            jsonify(
                {"email": email, "message": "logged in"}
            ))
        response.set_cookie("session_id", session_id)
        return response


@app.route("/sessions", methods=['DELETE'])
def logout():
    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user:
        AUTH.destroy_session(user.id)
        redirect("/")

    abort(403)


@app.route("/profile")
def profile():
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200

    abort(403)


@app.route("/reset_password", methods=['POST'])
def get_reset_password_token():
    """
        get reset password token
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)

    except ValueError:
        abort(403)

    else:
        return jsonify(
            {"email": email, "reset_token": token}
        )


@app.route("/reset_password", methods=['PUT'])
def update_password():
    """
        update password
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify(
            {"email": email, "message": "Password updated"}
        )
    except ValueError:
        abort(403)


AUTH = Auth()
if __name__ == '__main__':
    app.run()

#!/usr/bin/env python3
""" session_auth.py:  New view for Session Authentication"""

from api.v1.views import app_views
from flask import request, jsonify
from models.user import User
from api.v1.app import auth
import os

session_name = os.getenv('SESSION_NAME')


@app_views.route(
        "/auth_session/login",
        methods=['POST'],
        strict_slashes=False)
def auth_session_login():
    """
        GET: api/v1/auth_session/login
        Login a user
    """
    email = request.form.get('email')
    pwd = request.form.get('password')

    if not email or email == {}:
        return jsonify({"error": "email missing"}), 400

    if not pwd or pwd == {}:
        return jsonify({"error": "password missing"}), 400

    try:
        query_users_result = User.search({"email": email})
        if query_users_result == []:
            return jsonify(
                    {
                        "error": "no user found for this email"
                    }
            ), 404
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    for user in query_users_result:
        if user.is_valid_password(pwd):
            from api.v1.app import auth

            session_id = auth.create_session(user.id)
            res_obj = jsonify(user.to_json())
            res_obj.set_cookie(session_name, session_id)

            return res_obj, 200

    return jsonify({"error": "wrong password"}), 401


@app_views.route(
        "/auth_session/logout",
        methods=['DELETE'],
        strict_slashes=False)
def auth_session_logout():
    """ Get: api/v1/auth_session/logout """
    destroy = auth.destroy_session(request)
    if not destroy:
        abort(404)
    return jsonify({}), 200

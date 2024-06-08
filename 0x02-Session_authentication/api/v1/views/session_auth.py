#!/usr/bin/env python3
"""
Module for Session Authentication routes.

"""

from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
import os
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Route for user login using Session Authentication """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    response_data = user.to_json()

    response = jsonify(response_data)
    session_cookie_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_cookie_name, session_id)

    return response


@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Route for user logout / session destruction """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200

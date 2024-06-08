#!/usr/bin/env python3
"""
Module for Session Authentication routes.
"""

from flask import jsonify, request, make_response, abort
import os
from models.user import User
from api.v1.views import session_auth


@session_auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """ Route for user login using Session Authentication """
    from api.v1.app import auth

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve the User instance based on email
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID for the user
    session_id = auth.create_session(user.id)

    response_data = user.to_json()

    # Set session cookie in the response
    response = make_response(jsonify(response_data))
    session_cookie_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_cookie_name, session_id)

    return response


@session_auth.route('/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Route for user logout / session destruction """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200

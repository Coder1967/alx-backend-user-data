#!/usr/bin/env python3
"""
handles all routes for the Session authentication
"""
from flask import request, jsonify
from api.v1.views import app_views
from models.user import User
from os import getenv
from typing import Tuple


@app_views.route("/auth_session/login",
                 methods=["POST"], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    handles session authentication/login of users
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or len(email) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password) == 0:
        return jsonify({"error": "password missing"}), 400
    user = User.search({"email": email})
    if user is None or len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if user[0].is_valid_password(password) is False:
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    response = jsonify(user[0].to_json())
    response.set_cookie(getenv("SESSION_NAME"), sessiond_id)
    return response


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETES a session and return An empty JSON object.
    """
    from api.v1.app import auth
    destroyed = auth.destroy_session(request)
    if destroyed is False:
        abort(404)
    return jsonify({})

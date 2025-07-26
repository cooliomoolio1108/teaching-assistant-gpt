from flask import Blueprint, jsonify, request
from database.user_crud import get_user, create_user, get_users

user_routes = Blueprint("user", __name__)

@user_routes.route("/users/<user_id>", methods=["GET"])
def fetch_user(user_id):
    user = get_user(user_id)
    if user:
        return jsonify(user)
    return jsonify({"message": "User not found"}), 404

@user_routes.route("/users", methods=["POST"])
def add_user():
    data = request.json
    user_id = create_user(data)
    return jsonify({"message": "User created", "user_id": str(user_id)}), 201

@user_routes.route("/users", methods=["GET"])
def fetch_all_users():
    data = get_users()
    if data:
        return jsonify(data)
    return jsonify({"message": "No Users"})
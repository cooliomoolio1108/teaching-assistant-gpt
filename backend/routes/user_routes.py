from flask import Blueprint, jsonify, request
from database.user_crud import get_user, create_user, get_users
from models.user import User

user_routes = Blueprint("user", __name__)

@user_routes.route("/users/<oid>", methods=["GET"])
def fetch_user(oid):
    user = get_user(oid)
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
    users = []
    data = get_users()
    if data:
        for u in data:
            print("This is U: ", u)
            try:
                users.append(User(**u).dict())
                print("This is users:", users)
            except Exception as e:
                continue
        return jsonify(users)
    return jsonify({"message": "No Users"})
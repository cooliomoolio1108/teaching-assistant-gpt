from flask import Blueprint, jsonify, request
from database.message_crud import get_chat_message, submit_chat_message, get_chat_message_by_convoid

message_routes = Blueprint("message", __name__)

@message_routes.route("/message", methods=["GET"])
def fetch_message():
    message = get_chat_message()
    return jsonify(message)


@message_routes.route("/message/<convo_id>/", methods=["GET"])
def fetch_message_by_convoid(convo_id):
    messages = get_chat_message_by_convoid(convo_id)
    return jsonify([
        {
            "role": m["role"],
            "content": m["content"]
        }
        for m in messages
    ])

@message_routes.route("/message", methods=["POST"])
def receive_message():
    data = request.json
    message = submit_chat_message(data)
    return jsonify({"message": "message submitted", "message": str(message)}), 201
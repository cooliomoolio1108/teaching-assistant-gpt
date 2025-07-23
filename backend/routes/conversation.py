from flask import Blueprint, request, jsonify
from services.openai_service import get_openai_response, generate_title_for_chat  # your business logic
from database.conversation_crud import submit_chat_message, get_chat_message, get_convos, edit_title
from database.message_crud import get_chat_message, get_chat_message_by_convoid

conversation_routes = Blueprint("conversation", __name__)

# @conversation_routes.route("/conversation", methods=["POST"])
# def conversation():
#     data = request.get_json()
#     messages = data.get("messages", [])
#     response = get_openai_response(messages)
#     return jsonify({"response": response})

# @conversation_routes.route("/conversation", methods=["GET"])
# def get_conversation():
#     chat_message = get_chat_message()
#     return jsonify(chat_message)

@conversation_routes.route("/conversation", methods=["POST"])
def receive_conversation():
    data = request.get_json()
    convo_result = submit_chat_message(data)
    return jsonify({"message": "Convo submitted", "conversation_id": str(convo_result.inserted_id)}), 201

@conversation_routes.route("/conversation", methods=["GET"])
def get_conversation():
    chat_message = get_convos()
    return jsonify(chat_message)

@conversation_routes.route("/generate_title", methods=["POST"])
def generate_title():
    data = request.get_json()
    convo_id = data.get("conversation_id")

    if not convo_id:
        return jsonify({"error": "Missing conversation_id"}), 400

    messages = get_chat_message_by_convoid(convo_id)

    try:
        new_title = generate_title_for_chat(messages)
        success = edit_title(convo_id, new_title)
        if success:
            return jsonify({"title": new_title}), 200
        else:
            return jsonify({"error": "Failed to update title"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

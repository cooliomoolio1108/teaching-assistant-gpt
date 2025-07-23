# routes/chat_routes.py
from flask import Blueprint, request, jsonify, Response, stream_with_context
from services.openai_service import get_openai_response
from database.message_crud import get_chat_message_by_convoid, submit_chat_message

chat_routes = Blueprint("chat", __name__)

@chat_routes.route("/chat", methods=["POST"])
def get_chat_response():
    print("Getting GPT Response")
    data = request.get_json()
    convo_id = data.get("conversation_id")
    print("CONVO_ID: ", convo_id)

    if not convo_id:
        return jsonify({"error": "Missing conversation ID"}), 400

    messages = get_chat_message_by_convoid(convo_id)  # returns list of {role, content}
    print("Relevant Messages: ", messages)

    try:
        reply = get_openai_response(messages)
        # Save assistant message to DB
        assistant_msg = {
            "role": "assistant",
            "content": reply,
            "conversation_id": convo_id,
        }
        submit_chat_message(assistant_msg)

        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
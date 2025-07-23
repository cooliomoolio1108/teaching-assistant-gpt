from . import message_collection
from datetime import datetime

def submit_chat_message(message_data):
    result = message_collection.insert_one({
        "conversation_id": message_data["conversation_id"],
        "role": message_data["role"],
        "content": message_data["content"],
        "timestamp": datetime.utcnow()
    })
    return result

def get_chat_message():
    message_list = list(message_collection.find({}, {"_id": 0}))  # Exclude MongoDB _id
    return message_list

def get_chat_message_by_convoid(convo_id):
    messages = list(message_collection.find(
        {"conversation_id": convo_id}
    ).sort("timestamp", 1))
    return messages
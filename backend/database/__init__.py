from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["teaching_assistant"]

feedback_collection = db["feedback"]
user_collection = db["user"]
conversation_collection =  db["conversation"]
message_collection = db["message"]
chat_collection = db['chat']
course_collection = db['course']

def check_connection():
    try:
        client.server_info()  # Ping the server
        return {"status": "Success", "message": "Connected to MongoDB!"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
    
def serialize_user(user_doc):
    user_doc["_id"] = str(user_doc["_id"])
    return user_doc
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["teaching_assistant"]
collection1 = db["feedback"]
collection2 = db["feedback_details"]

def check_connection():
    try:
        client.server_info()  # Ping the server
        return {"status": "Success", "message": "Connected to MongoDB!"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

def get_feedback():
    feedback_list = list(collection1.find({}, {"_id": 0}))  # Exclude MongoDB _id
    return feedback_list

def get_feedback_details():
    feedback_details = list(collection2.find({}, {"_id": 0}))
    return feedback_details

def submit_feedback(data):
    result = collection2.insert_one(data)
    return result

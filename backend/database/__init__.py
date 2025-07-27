from pymongo import MongoClient
import os
from dotenv import load_dotenv
from typing import List, Type
from pydantic import BaseModel

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
file_collection = db['file']

def check_connection():
    try:
        client.server_info()  # Ping the server
        return {"status": "Success", "message": "Connected to MongoDB!"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}
    
def serialize_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc

def clean_data(data: List[dict], Model: Type[BaseModel]) -> List[dict]:
    datalist = []

    if len(data) == 1:
        u = data[0]
        try:
            datalist.append(Model(**u).dict())
        except Exception as e:
            print("Skipping due to error:", e)
    else:
        for u in data:
            try:
                datalist.append(Model(**u).dict())
            except Exception as e:
                print("Skipping due to error:", e)
    
    return datalist
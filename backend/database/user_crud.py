from . import user_collection

def get_user(user_id):
    return user_collection.find_one({"user_id": user_id}, {"_id": 0})

def create_user(user_data):
    result = user_collection.insert_one(user_data)
    return result.inserted_id

def serialize_user(user_doc):
    user_doc["_id"] = str(user_doc["_id"])
    return user_doc

def get_users():
    users_cursor = user_collection.find()
    return [serialize_user(user) for user in users_cursor]
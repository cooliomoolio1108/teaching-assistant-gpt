from . import user_collection

def get_user(user_id):
    return user_collection.find_one({"user_id": user_id}, {"_id": 0})

def create_user(user_data):
    result = user_collection.insert_one(user_data)
    return result.inserted_id
from . import file_collection
from datetime import datetime
from . import serialize_id, clean_data
from models.file import File
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "backend", "documents")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

def get_files():
    files = file_collection.find()
    return [serialize_id(file) for file in files]

def get_files_by_course(course_id: str):
    results = list(file_collection.find({"course_id": course_id}))
    cleaned = [serialize_id(file) for file in results]
    return cleaned

def save_files_to_db(data):
    def process(doc):
        return File(**doc).dict(by_alias=True, exclude_none=True)

    if isinstance(data, dict):
        # Single document
        cleaned = process(data)
        result = file_collection.insert_one(cleaned)
        return {"inserted_id": str(result.inserted_id)}

    elif isinstance(data, list):
        # Multiple documents
        cleaned_list = [process(doc) for doc in data if isinstance(doc, dict)]
        if not cleaned_list:
            raise ValueError("No valid documents to insert.")
        result = file_collection.insert_many(cleaned_list)
        return {"inserted_ids": [str(_id) for _id in result.inserted_ids]}

    else:
        raise ValueError("Expected a dictionary or a list of dictionaries.")
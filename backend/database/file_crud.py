from . import file_collection
from datetime import datetime
from . import serialize_id, clean_data

def get_files():
    files = file_collection.find()
    return [serialize_id(file) for file in files]

def get_files_by_course(course_id: str):
    results = list(file_collection.find({"course_id": course_id}))
    print("ALL FILES:", results)
    return list(file_collection.find({"course_id": course_id}))

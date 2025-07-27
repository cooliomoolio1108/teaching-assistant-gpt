from . import course_collection
from . import serialize_id
from bson import ObjectId
from typing import List, Type
from pydantic import BaseModel

def clean_data(data: List, Model: Type[BaseModel]) -> List[dict]:
    datalist = []
    if len(data) == 1:
        for u in data:
            print("This is U: ", u)
            try:
                datalist.append(Model(**u).dict())
            except Exception as e:
                print("Skipping due to error:", e)
                continue
    return datalist

def get_courses():
    courses_cursor = course_collection.find()
    return [serialize_id(course) for course in courses_cursor]

def get_course_details(id: str):
    print("THIS ID", id)
    doc = course_collection.find_one({"_id": id})
    return [doc]
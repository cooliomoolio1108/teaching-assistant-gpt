from . import course_collection
from . import serialize_user

def get_courses():
    courses_cursor = course_collection.find()
    return [serialize_user(course) for course in courses_cursor]
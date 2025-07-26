from flask import Blueprint, jsonify, request
from database.course_crud import get_courses
from models.course import Course

course_routes = Blueprint("course", __name__)

@course_routes.route("/courses", methods=["GET"])
def fetch_all_users():
    courses = []
    data = get_courses()
    if data:
        for u in data:
            print("This is U: ", u)
            try:
                courses.append(Course(**u).dict())
                print("This is courses:", courses)
            except Exception as e:
                continue
        return jsonify(courses)
    return jsonify({"message": "No courses"})
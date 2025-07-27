from flask import Blueprint, jsonify, request
from database.course_crud import get_courses, get_course_details, clean_data
from models.course import Course

course_routes = Blueprint("course", __name__)

@course_routes.route("/courses", methods=["GET"])
def fetch_all_courses():
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

@course_routes.route("/courses/<id>", methods=["GET"])
def fetch_one_course(id):
    data = get_course_details(id)
    if data:
        course = clean_data(data, Course)
        return jsonify(course)
    return jsonify({"message": "No courses"})
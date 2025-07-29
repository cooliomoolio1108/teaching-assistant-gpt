from flask import Blueprint, jsonify, request
from database.file_crud import get_files, get_files_by_course, save_files_to_db
from models.file import File
from database import clean_data

file_routes = Blueprint("file", __name__)

@file_routes.route("/files", methods=["GET"])
def fetch_files():
    course_id = request.args.get("course_id")

    if course_id:
        data = get_files_by_course(course_id)
    else:
        data = get_files()

    if data:
        files = clean_data(data, File)
        return jsonify(files)

    return jsonify({"message": "No Files"}), 404

@file_routes.route("/files", methods=["POST"])
def receive_file():
    data = request.json
    result = save_files_to_db(data)
    return jsonify({'result': result})
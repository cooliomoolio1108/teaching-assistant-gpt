from flask import Blueprint, jsonify, request
from database.file_crud import get_files, get_files_by_course
from models.file import File
from database import clean_data

file_routes = Blueprint("file", __name__)

@file_routes.route("/files", methods=["GET"])
def fetch_all_files():
    data = get_files()
    if data:
        files = clean_data(data, File)
        return jsonify(files)
    return jsonify({"message": "No Files"})
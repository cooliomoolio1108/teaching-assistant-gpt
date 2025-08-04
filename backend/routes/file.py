from flask import Blueprint, jsonify, request
from database.file_crud import get_files, get_files_by_course, save_files_to_db, get_file_by_id, embed_single_file
from models.file import File
from database import clean_data
from datetime import datetime
from werkzeug.utils import secure_filename
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "backend", "documents")

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
    uploaded = request.files.get("file")

    if not uploaded:
        return jsonify({"error": "No file part in request"}), 400
    print("Request Form:", request.form)
    metadata = {
        "course_id": request.form.get("course_id"),
        "uploaded_by": request.form.get("uploaded_by"),
        "title": request.form.get("title"),
        "uploaded_at": datetime.now(),
        "updated_at": datetime.now()
    }
    filename = secure_filename(uploaded.filename)

    folder_path = os.path.join(DOCUMENTS_DIR, request.form.get("course_id"))
    os.makedirs(folder_path, exist_ok=True)
    save_path = os.path.join(folder_path, filename)
    uploaded.save(save_path)

    metadata["file_name"] = filename
    metadata["path"] = save_path
    metadata["embedded"] = False

    result = save_files_to_db(metadata)
    return jsonify({'result': result})

@file_routes.route("/embed", methods=["POST"])
def embed_file():
    file_ids = request.json.get("file_ids", [])
    for file_id in file_ids:
        file_doc = get_file_by_id(file_id)
        if file_doc and not file_doc.get("embedded"):
            embed_single_file(file_doc)
    return jsonify({"status": "embedding complete"})
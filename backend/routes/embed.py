from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from utils.chunk_utils import extract_text_slide_by_slide, chunk_text
from utils.embedding_utils import generate_embeddings
from utils.file_utils import save_uploaded_file
from vector_store.chroma_manager import store_embeddings_in_chromadb
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

embed_routes = Blueprint("embed", __name__)

model_name = os.getenv("EMBED_DEPLOY_NAME")

@embed_routes.route("/embed", methods=["POST"])
def handle_multi_upload():
    files = request.files.getlist("files")

    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    total_chunks = 0

    for uploaded_file in files:
        filename = secure_filename(uploaded_file.filename)
        file_path = save_uploaded_file(uploaded_file, filename)

        slides = extract_text_slide_by_slide(file_path)
        for slide in slides:
            chunks = chunk_text(slide["text"])
            embeddings = generate_embeddings(chunks, model_name)
            store_embeddings_in_chromadb(chunks, embeddings, slide_number=slide["slide_number"])
            total_chunks += len(chunks)

    return jsonify({
        "message": "Files uploaded and processed",
        "total_files": len(files),
        "total_chunks": total_chunks
    }), 201
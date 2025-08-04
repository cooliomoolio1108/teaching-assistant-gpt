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

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "backend", "documents")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)
from . import file_collection
from datetime import datetime
from . import serialize_id, clean_data
from models.file import File
import os
from bson import ObjectId
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings  # or other
from langchain_chroma import Chroma
from services.chromadb_service import vector_store

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DOCUMENTS_DIR = os.path.join(BASE_DIR, "backend", "documents")
os.makedirs(DOCUMENTS_DIR, exist_ok=True)

def get_files():
    files = file_collection.find()
    return [serialize_id(file) for file in files]

def get_files_by_course(course_id: str):
    results = list(file_collection.find({"course_id": course_id}))
    cleaned = [serialize_id(file) for file in results]
    return cleaned

def get_file_by_id(id):
    file_doc = file_collection.find_one({"_id": ObjectId(id)})
    return file_doc

def save_files_to_db(data):
    def process(doc):
        return File(**doc).dict(by_alias=True, exclude_none=True)

    if isinstance(data, dict):
        # Single document
        cleaned = process(data)
        result = file_collection.insert_one(cleaned)
        return {"inserted_id": str(result.inserted_id)}

    elif isinstance(data, list):
        # Multiple documents
        cleaned_list = [process(doc) for doc in data if isinstance(doc, dict)]
        if not cleaned_list:
            raise ValueError("No valid documents to insert.")
        result = file_collection.insert_many(cleaned_list)
        return {"inserted_ids": [str(_id) for _id in result.inserted_ids]}

    else:
        raise ValueError("Expected a dictionary or a list of dictionaries.")
    
def embed_single_file(file_doc):
    if not file_doc:
        return {'Error': 'Error'}
    file_path = file_doc["path"]
    file_id = str(file_doc["_id"])

    loader = PyMuPDFLoader(file_path)
    raw_documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(raw_documents)
    if not chunks:
        raise ValueError("❌ No content to embed from document")
    for chunk in chunks:
        chunk.metadata["file_id"] = file_id
        chunk.metadata["file_name"] = file_doc["file_name"]
        chunk.metadata["course_id"] = file_doc["course_id"]
    
    doc_ids = vector_store.add_documents(chunks)
    file_collection.update_one(
        {"_id": ObjectId(file_doc["_id"])},
        {
            "$set": {
                "embedded": True,
                "embedding_at": datetime.utcnow(),
                "doc_ids": doc_ids
            }
        }
    )
    print("The collection is length:", vector_store._collection.count())
    return {"status": "embedded", "doc_count": len(doc_ids)}
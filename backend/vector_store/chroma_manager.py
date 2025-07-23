import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

persist_directory = "./chroma_db_data"  # Directory to store data
chroma_client = chromadb.PersistentClient(path="./chroma_db_data")

# Create or load a collection
collection = chroma_client.get_or_create_collection(name="course_doc")

def store_embeddings_in_chromadb(chunks, embeddings, slide_number):
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        collection.add(
            ids=[f"slide_{slide_number}_chunk_{i + 1}"],
            embeddings=[embedding],
            metadatas=[{
                "slide_number": slide_number,
                "chunk_number": i + 1,
                "text": chunk
            }]
        )

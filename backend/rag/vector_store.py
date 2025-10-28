import os
import chromadb
from chromadb.utils import embedding_functions 
from dotenv import load_dotenv                 
from typing import List, Dict, Any

load_dotenv()
DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vectordb")
COLLECTION_NAME = os.getenv("VECTOR_COLLECTION_NAME", "clinic_faqs")
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "models/text-embedding-004")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Please set it in your .env file.")

client = chromadb.PersistentClient(path=DB_PATH)

# --- Instantiate the Google Embedding Function ---
embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
    api_key=API_KEY,
    model_name=MODEL_NAME
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)


def add_documents_to_store(documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
    """
    Adds a batch of documents to the ChromaDB collection.
    """
    try:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully added {len(documents)} documents to collection '{COLLECTION_NAME}'.")
    except Exception as e:
        print(f"Error adding documents to Chroma: {e}")

def query_vector_store(query_text: str, n_results: int = 3) -> List[str]:
    """
    Queries the collection using raw text.
    """
    try:
        results = collection.query(
            query_texts=[query_text],  
            n_results=n_results,
            include=["documents"]     
        )
        
        # Results['documents'] is a list containing one list (for our one query)
        return results['documents'][0] if results['documents'] else []
    
    except Exception as e:
        print(f"Error querying ChromaDB: {e}")
        return []

def clear_vector_store():
    """Utility function to delete and re-create the collection."""
    try:
        print(f"Attempting to delete collection: {COLLECTION_NAME}...")
        client.delete_collection(name=COLLECTION_NAME)
        print("Collection deleted.")
    except Exception as e:
        print(f"Collection delete failed (may not exist): {e}")
    
    # Re-create it
    global collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )
    print(f"Collection '{COLLECTION_NAME}' ensured to be empty and ready.")
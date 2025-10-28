import json
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# ------------------------------------------------

from backend.rag.vector_store import add_documents_to_store, clear_vector_store

DATA_FILE = "data/clinic_info.json"

def process_and_load_data():
    """
    Reads the JSON data, formats it for ChromaDB, and ingests it.
    """
    print("--- Starting RAG Ingestion Process ---")
    
    # --- 1. Clear the vector store for a fresh upload ---
    # This makes the script idempotent (safe to run multiple times)
    clear_vector_store()

    # --- 2. Load data from JSON ---
    print(f"Loading data from {DATA_FILE}...")
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading data file: {e}")
        return

    documents = []
    metadatas = []
    ids = []
    doc_id_counter = 1

    # --- 3. Format data for ChromaDB ---
    for category, qa_list in data.items():
        for qa in qa_list:
            # The "document" is the combined Q&A
            doc_content = f"Question: {qa['q']}\nAnswer: {qa['a']}"
            
            documents.append(doc_content)
            
            # Metadata helps filter (though we don't use it in this simple query)
            metadatas.append({"category": category, "question": qa['q']})
            
            # IDs must be unique strings
            ids.append(f"faq_doc_{doc_id_counter}")
            doc_id_counter += 1

    if not documents:
        print("No documents found to ingest.")
        return

    # --- 4. Add to vector store ---
    print(f"Preparing to add {len(documents)} documents to vector store...")
    add_documents_to_store(documents=documents, metadatas=metadatas, ids=ids)
    
    print("--- RAG Ingestion Process Complete ---")

if __name__ == "__main__":
    process_and_load_data()
from .vector_store import query_vector_store
from typing import List

def get_faq_context(question: str) -> str:
    """
    Retrieves the most relevant FAQ context for a given question.
    
    """
    if not question:
        return "Please ask a question."
        
    # Query the vector store for the top 2 relevant documents
    context_items = query_vector_store(question, n_results=2)
    
    if not context_items:
        return "I'm sorry, I couldn't find any specific information about that."

    context_string = "\n\n---\n\n".join(context_items)
    
    return context_string
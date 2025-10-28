from fastapi import FastAPI
from pydantic import BaseModel
from .rag.faq_rag import get_faq_context

# Initialize FastAPI app
app = FastAPI(
    title="Medical Scheduling Agent - RAG Module",
    description="API endpoint for testing the FAQ RAG functionality.",
    version="1.0.0"
)

# --- Pydantic Models for API ---
class FAQRequest(BaseModel):
    question: str = "What insurance do you accept?"

class FAQResponse(BaseModel):
    question: str
    retrieved_context: str

@app.post("/api/ask-faq", 
          response_model=FAQResponse, 
          summary="Ask a question to the RAG")
def ask_faq_endpoint(request: FAQRequest):
    """
    Receives a patient's question, retrieves the most relevant context
    from the vector store, and returns it.
    
    This simulates the 'retrieval' part of RAG.
    """
    print(f"Received question: {request.question}")
    
    # Call our main RAG function
    context = get_faq_context(request.question)
    
    print(f"Retrieved context: {context}")
    return FAQResponse(
        question=request.question,
        retrieved_context=context
    )

if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server for RAG testing...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
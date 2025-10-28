##How to Run

###Set up Environment:

Create a virtual environment: python -m venv venv

Activate it: source venv/bin/activate (or .\venv\Scripts\activate on Windows)

Install dependencies: pip install -r requirements.txt

##Run the ingestion script from the project's root directory:

Bash
python scripts/ingest_data.py

You should see output confirming that documents were added. A new directory, data/vectordb, will be created.

##Run the Test Server:

Run the FastAPI application:

Bash
uvicorn backend.main:app --reload --port 8000


on your other terminal 
curl -X POST "http://127.0.0.1:8000/api/ask-faq" \
     -H "Content-Type: application/json" \
     -d '{"question": "Do I have to pay if I cancel?"}'

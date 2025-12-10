python -m venv venv
.\venv\Scripts\activate
pip install -r  requirements.txt

For start the app we need to run

.\venv\Scripts\activate
uvicorn app.main:app --reload

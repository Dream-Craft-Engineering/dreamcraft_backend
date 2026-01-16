python -m venv venv
.\venv\Scripts\activate
pip install -r  requirements.txt

For start the app we need to run

.\venv\Scripts\activate
uvicorn app.main:app --reload

if no "versions" folder under alembic then create it.
alembic revision --autogenerate -m "initial"

alembic current //Check current revision
alembic upgrade head //Run migrations


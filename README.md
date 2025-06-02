# auto_research_assis

* python -m venv venv
* source venv/Scripts/activate
* pip install -r requirements.txt
* export $(cat .env | xargs)
* uvicorn main:app --reload
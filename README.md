# Python with FastAPI
Python with FastAPI simple example

## VENV
For Mac 

`source .venv/bin/activate`

For Windows 

`.venv\Scripts\activate`

Deactive `deactivate`

## Run
`uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`

## Migration
`alembic revision --autogenerate -m "Messagehere"`

### Reset database
`alembic downgrade base`

`alembic upgrade head`
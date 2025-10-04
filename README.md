# Python with FastAPI
Python with FastAPI simple example

## Clone this project
Clone this project using your text editor

## Init project
`python -m venv .venv`

## VENV
For Mac 

`source .venv/bin/activate`

For Windows 

`.venv\Scripts\activate`

Deactive `deactivate`

## Install requirements
`pip install -r requirements.txt`

or

`pip3 install -r requirements.txt`

## Run migration
`alembic upgrade head`

## Run
`uvicorn src.main:app --reload --host 0.0.0.0 --port 8000`

## Check endpoint
`localhost:8000` and `localhost:8000/api/v1/student`


## Optional
### Crate Migration
`alembic revision --autogenerate -m "Messagehere"`

### Reset database
`alembic downgrade base`
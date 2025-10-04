# app/db/database.py
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.engine import Engine
from typing import Generator

# Import ALL your models here so SQLModel.metadata can find them
# Even if you don't use them directly in this file,
# their mere import registers them with SQLModel.metadata

from src.db.models.student import Student

from src.core.config import settings

engine: Engine | None = None # Initialize as None

def get_engine() -> Engine:
    global engine
    if engine is None:
        engine = create_engine(
            settings.DATABASE_URL,
            # echo=True if settings.ENVIRONMENT == 'development' else False,
            pool_pre_ping=True # Helps with stale connections
        )
    return engine

def create_db_and_tables():
    # SQLModel.metadata.create_all() uses the engine to connect
    # and create all tables defined with table=True in your imported models.
    SQLModel.metadata.create_all(get_engine())
    print("Database tables created (or already exist).")

def get_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session
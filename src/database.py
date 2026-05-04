"""
Database connection and session management.

Read DATABASE_URL from environment variable.
Create SQLAlchemy engine and session.
Provide a dependency for FastAPI to get a DB session.
"""

# TODO: Implement database connection here
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import getenv

DATABASE_URL = getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
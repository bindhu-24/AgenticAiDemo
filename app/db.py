import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
 
# Load .env file
load_dotenv()
 
# Read DATABASE_URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://books_user:StrongPassword%402026@localhost:5432/books_db"
)
 
# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,       # auto-reconnect if connection drops
    pool_size=10,            # number of connections in pool
    max_overflow=20,         # extra connections allowed
)
 
# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
 
# Base class for all models
Base = declarative_base()
 
# Dependency — use this in all routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

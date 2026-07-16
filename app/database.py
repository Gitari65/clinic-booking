from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Load DATABASE_URL from environment if present, else fall back to a local sqlite file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./clinic.db")

# If using sqlite, ensure the connect args include check_same_thread
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

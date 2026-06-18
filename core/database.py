# core/database.py
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# 1. Dynamically compute the absolute path to your root folder 
# This ensures Streamlit can safely write 'talent_suite.db' without permission issues.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DB_PATH = f"sqlite:///{os.path.join(BASE_DIR, 'talent_suite.db')}"

# 2. Grab from environment variables (like Streamlit Secrets) if provided, otherwise default to absolute path
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_PATH)

# 3. Quick fix for common production databases (e.g. Supabase/Render) using legacy "postgres://" URLs
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="Recruiter")  # Admin, Recruiter, Candidate
    created_at = Column(DateTime, default=datetime.utcnow)

class CandidateProfile(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)
    resume_text = Column(Text, nullable=True)
    ats_score = Column(Integer, nullable=True)
    status = Column(String, default="Applied")  # Applied, Interviewing, Offered, Rejected
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
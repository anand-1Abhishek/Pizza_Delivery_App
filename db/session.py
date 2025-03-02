# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

# Create engine with echo for debugging
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

# Create engine. In SQLite, we need connect_args={"check_same_thread": False}
# This can be safely removed if moving to PostgreSQL
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency for injecting DB sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

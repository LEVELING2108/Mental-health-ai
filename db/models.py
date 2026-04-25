import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from core.database import Base


def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    # Profile Fields
    full_name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    profile_image = Column(String, nullable=True) # Path to the image file
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to mood logs
    mood_logs = relationship("MoodLog", back_populates="owner", cascade="all, delete-orphan")

class MoodLog(Base):
    __tablename__ = "mood_logs"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)

    # Input
    user_text = Column(Text, nullable=False)

    # AI Analysis
    risk_level = Column(String, nullable=False)
    confidence_score = Column(Float, nullable=False)
    emotion = Column(String, nullable=False)
    keywords = Column(String, nullable=True) # Stored as comma-separated string

    # AI Output
    ai_response = Column(Text, nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    owner = relationship("User", back_populates="mood_logs")

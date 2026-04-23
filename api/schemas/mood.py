from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MoodLogOut(BaseModel):
    id: str
    user_text: str
    risk_level: str
    confidence_score: float
    emotion: str
    keywords: str | None
    ai_response: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

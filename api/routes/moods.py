
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_user
from api.schemas.mood import MoodLogOut
from core.database import get_db
from db.models import MoodLog, User

router = APIRouter()

@router.get("/", response_model=list[MoodLogOut])
def get_mood_history(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieve the mood history for the currently logged-in user."""
    logs = db.query(MoodLog).filter(MoodLog.user_id == current_user.id)\
             .order_by(MoodLog.created_at.desc())\
             .offset(skip).limit(limit).all()
    return logs

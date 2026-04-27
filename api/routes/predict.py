from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_current_user_optional
from api.schemas.predict import SupportRequest, SupportResponse
from core.database import get_db
from core.logger import setup_logger
from db.models import MoodLog
from model.predict import MentalHealthPredictor
from utils.response import generate_safe_response, get_resources

router = APIRouter()
logger = setup_logger(__name__)

@lru_cache
def get_predictor() -> MentalHealthPredictor:
    """Dependency for lazy loading the predictor."""
    return MentalHealthPredictor()

@router.post("/", response_model=SupportResponse)
def predict_mental_health(
    request: SupportRequest,
    predictor: MentalHealthPredictor = Depends(get_predictor),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_optional)
) -> SupportResponse:
    logger.info(f"Received prediction request. Text length: {len(request.text)}")
    try:
        # 1. Gather context: Prefer request history (current session) over DB history (past sessions)
        history_context = request.history
        
        if not history_context and current_user:
            history_context = []
            past_logs = db.query(MoodLog).filter(MoodLog.user_id == current_user.id)\
                          .order_by(MoodLog.created_at.desc()).limit(5).all()
            # Convert to history format (oldest first for the AI)
            for log in reversed(past_logs):
                history_context.append({"role": "user", "content": log.user_text})
                history_context.append({"role": "assistant", "content": log.ai_response})

        # 2. Perform AI Analysis with History and Gender
        logger.info(f"Starting AI prediction (History depth: {len(history_context) if history_context else 0})...")
        gender = current_user.gender if current_user else None
        result = predictor.predict(request.text, history=history_context, gender=gender)
        logger.info("AI prediction completed successfully.")

        # 2. Prepare responses
        safe_response = generate_safe_response(result)
        resources = get_resources(result["risk"])

        # 3. Optional Persistence (Log to Database)
        if current_user:
            try:
                mood_log = MoodLog(
                    user_id=current_user.id,
                    user_text=request.text,
                    risk_level=result["risk"],
                    confidence_score=result["score"],
                    emotion=result["emotion"],
                    keywords=result["keywords"][0] if result["keywords"] else None,
                    ai_response=result["ai_generated_response"]
                )
                db.add(mood_log)
                db.commit()
                logger.info(f"Mood logged successfully for user {current_user.email}")
            except Exception as db_err:
                logger.error(f"Database logging failed (non-critical): {db_err}")
                db.rollback()

        return SupportResponse(
            risk=result["risk"],
            score=result["score"],
            emotion=result["emotion"],
            keywords=result["keywords"],
            response=safe_response,
            ai_generated_response=result["ai_generated_response"],
            resources=resources
        )
    except Exception as e:
        logger.error(f"CRITICAL: Error during predict_mental_health: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed on server: {str(e)}"
        )

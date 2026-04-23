from fastapi import APIRouter, HTTPException
from api.schemas.predict import SupportRequest, SupportResponse
from model.predict import MentalHealthPredictor
from utils.response import generate_safe_response, get_resources
from core.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

# Initialize predictor
# Loading will be slower the first time as it downloads the model (Zephyr or Flan-T5)
predictor = MentalHealthPredictor()

@router.post("/", response_model=SupportResponse)
def predict_mental_health(request: SupportRequest) -> SupportResponse:
    logger.info(f"Received prediction request. Text length: {len(request.text)}")
    try:
        result = predictor.predict(request.text)
        
        # Standard safety response
        safe_response = generate_safe_response(result)
        resources = get_resources(result["risk"])
        
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
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")

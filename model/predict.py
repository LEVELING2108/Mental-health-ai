import os
import sys
from typing import Any

import joblib
from transformers import pipeline

# Add the parent directory to sys.path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.config import settings
from core.logger import setup_logger
from utils.explain import get_top_keywords
from utils.generator import ai_generator  # New: Generative AI
from utils.preprocess import clean_text

logger = setup_logger(__name__)

class MentalHealthPredictor:
    def __init__(self, model_path: str | None = None, vectorizer_path: str | None = None):
        mp = model_path or settings.MODEL_PATH
        vp = vectorizer_path or settings.VECTORIZER_PATH

        try:
            # 1. Specialized Classifier
            self.model = joblib.load(mp)
            self.vectorizer = joblib.load(vp)
            logger.info(f"Loaded classifier from {mp}")

            # 2. Advanced Emotion Transformer
            logger.info("Loading Advanced Transformer Model (distilbert-base-uncased-emotion)...")
            self.ai_analyzer = pipeline(
                "sentiment-analysis",
                model="bhadresh-savani/distilbert-base-uncased-emotion",
                device=-1  # Use CPU
            )
            logger.info("Advanced Emotion Model loaded successfully.")

        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise

    def predict(self, text: str) -> dict[str, Any]:
        cleaned = clean_text(text)

        # 1. Classify Risk (Specialized Model)
        features = self.vectorizer.transform([cleaned])
        custom_prediction = self.model.predict(features)[0]
        custom_probs = self.model.predict_proba(features)[0]
        custom_score = float(max(custom_probs))

        # 2. Analyze Emotion (Transformer)
        ai_result = self.ai_analyzer(text)[0]
        ai_label = ai_result['label']
        ai_score = ai_result['score']

        # 3. Hybrid Risk Refinement
        final_risk = custom_prediction
        critical_emotions = ['sadness', 'fear', 'anger']
        if ai_label in critical_emotions and ai_score > 0.8:
            if custom_prediction == "low":
                final_risk = "medium"
            elif custom_prediction == "medium":
                final_risk = "high"

        # 4. Keyword Explainability
        keywords = get_top_keywords(features, self.vectorizer)

        # 5. GENERATIVE AI RESPONSE
        # Generate a unique, empathetic response based on all detected data
        ai_generated_response = ai_generator.generate(
            risk=final_risk,
            emotion=ai_label,
            user_text=text,
            keywords=keywords
        )

        logger.info(f"Analysis Complete - Risk: {final_risk}, Emotion: {ai_label}")

        return {
            "risk": str(final_risk),
            "score": round(float((custom_score + ai_score) / 2), 2),
            "emotion": ai_label,
            "keywords": keywords,
            "ai_generated_response": ai_generated_response
        }

if __name__ == "__main__":
    predictor = MentalHealthPredictor()
    print(predictor.predict("I feel very lonely and sad"))

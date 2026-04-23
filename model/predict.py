import os
import sys
from typing import Any

from transformers import pipeline

# Add the parent directory to sys.path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.logger import setup_logger
from utils.generator import ai_generator

logger = setup_logger(__name__)

class MentalHealthPredictor:
    def __init__(self):
        try:
            # TIER 1 UPGRADE: Zero-Shot Classification (Industry Standard for Robustness)
            # This uses BART-Large-MNLI to classify text into dynamic labels without needing a niche model.
            logger.info("Loading Tier 1 Zero-Shot Classifier (facebook/bart-large-mnli)...")
            self.classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1  # Use CPU
            )

            # 2. Advanced Emotion Transformer
            logger.info("Loading Advanced Emotion Model (distilbert-base-uncased-emotion)...")
            self.emotion_analyzer = pipeline(
                "sentiment-analysis",
                model="bhadresh-savani/distilbert-base-uncased-emotion",
                device=-1  # Use CPU
            )

            logger.info("All Advanced AI Models loaded successfully.")

        except Exception as e:
            logger.error(f"Failed to load models: {e}")
            raise

    def predict(self, text: str) -> dict[str, Any]:
        # 1. Zero-Shot Risk Classification
        # We provide the labels we want the model to look for.
        candidate_labels = ["normal", "anxiety", "depression", "suicidal", "stress", "bipolar"]

        logger.info(f"Analyzing risk with Zero-Shot for labels: {candidate_labels}")
        raw_prediction = self.classifier(text, candidate_labels=candidate_labels)

        # The first label in 'labels' is the most likely one
        label = raw_prediction['labels'][0]
        score = raw_prediction['scores'][0]

        # Map labels to Risk Levels
        risk_mapping = {
            'normal': 'low',
            'stress': 'medium',
            'anxiety': 'medium',
            'bipolar': 'medium',
            'depression': 'high',
            'suicidal': 'high'
        }
        final_risk = risk_mapping.get(label, 'medium')

        # 2. Analyze Emotion
        emotion_result = self.emotion_analyzer(text)[0]
        emotion_label = emotion_result['label']
        emotion_score = emotion_result['score']

        # 3. GENERATIVE AI RESPONSE
        ai_generated_response = ai_generator.generate(
            risk=final_risk,
            emotion=emotion_label,
            user_text=text,
            keywords=[label]
        )

        logger.info(f"Analysis Complete - Risk: {final_risk} (Detected: {label}), Emotion: {emotion_label}")

        return {
            "risk": str(final_risk),
            "score": round(float((score + emotion_score) / 2), 2),
            "emotion": emotion_label,
            "keywords": [label],
            "ai_generated_response": ai_generated_response
        }

if __name__ == "__main__":
    predictor = MentalHealthPredictor()
    print(predictor.predict("I feel very lonely and sad"))

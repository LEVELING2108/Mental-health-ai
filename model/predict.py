import os
import sys
from typing import Any, Dict

import torch
from transformers import pipeline

# Add the parent directory to sys.path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.config import settings
from core.logger import setup_logger
from utils.preprocess import clean_text
from utils.generator import ai_generator

logger = setup_logger(__name__)

class MentalHealthPredictor:
    def __init__(self):
        try:
            # TIER 1 UPGRADE: Advanced Specialized Mental Health Transformer
            # This model is specifically pre-trained on mental health texts.
            logger.info("Loading Tier 1 Transformer Classifier (mental-health-classification)...")
            self.classifier = pipeline(
                "text-classification",
                model="rabiaqayyum/bert-base-uncased-mental-health-classification",
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
        cleaned = clean_text(text)

        # 1. Classify Risk using the Advanced Mental Health Transformer
        # This model outputs labels like 'Normal', 'Depression', 'Suicidal', etc.
        # We map these to our 'low', 'medium', 'high' risk levels.
        raw_prediction = self.classifier(text)[0]
        label = raw_prediction['label'].lower()
        score = raw_prediction['score']

        # Map Transformer labels to Risk Levels
        risk_mapping = {
            'normal': 'low',
            'anxiety': 'medium',
            'bipolar': 'medium',
            'depression': 'high',
            'personality disorder': 'high',
            'suicidal': 'high'
        }
        final_risk = risk_mapping.get(label, 'medium')

        # 2. Analyze Emotion
        emotion_result = self.emotion_analyzer(text)[0]
        emotion_label = emotion_result['label']
        emotion_score = emotion_result['score']

        # 3. GENERATIVE AI RESPONSE
        # Keywords are now handled more naturally by the LLM prompt
        ai_generated_response = ai_generator.generate(
            risk=final_risk,
            emotion=emotion_label,
            user_text=text,
            keywords=[] # LLM handles extraction now
        )

        logger.info(f"Analysis Complete - Risk: {final_risk} (Label: {label}), Emotion: {emotion_label}")

        return {
            "risk": str(final_risk),
            "score": round(float((score + emotion_score) / 2), 2),
            "emotion": emotion_label,
            "keywords": [label], # Use the detected clinical label as a primary keyword
            "ai_generated_response": ai_generated_response
        }

if __name__ == "__main__":
    predictor = MentalHealthPredictor()
    print(predictor.predict("I feel very lonely and sad"))

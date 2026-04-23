import os
import sys

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Add the parent directory to sys.path to import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.config import settings
from core.logger import setup_logger
from utils.preprocess import clean_text

logger = setup_logger(__name__)

def train_model() -> None:
    data_path = settings.DATA_PATH
    if not os.path.exists(data_path):
        logger.error(f"Dataset not found at {data_path}")
        return

    logger.info(f"Loading dataset from {data_path}")
    df = pd.read_csv(data_path)

    logger.info("Preprocessing text...")
    df['clean_text'] = df['text'].apply(clean_text)

    logger.info("Vectorizing text...")
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['risk']

    logger.info("Training Logistic Regression model...")
    model = LogisticRegression()
    model.fit(X, y)

    # Ensure model directory exists
    os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(settings.VECTORIZER_PATH), exist_ok=True)

    logger.info(f"Saving model to {settings.MODEL_PATH}")
    joblib.dump(model, settings.MODEL_PATH)

    logger.info(f"Saving vectorizer to {settings.VECTORIZER_PATH}")
    joblib.dump(vectorizer, settings.VECTORIZER_PATH)
    logger.info("Model and vectorizer saved successfully!")

if __name__ == "__main__":
    train_model()

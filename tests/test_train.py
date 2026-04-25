import os
import pandas as pd
import pytest
from model.train import train_model
from core.config import settings

def test_train_model_logic(tmp_path):
    # Create a small dummy dataset in the temp directory
    dummy_data = {
        "text": ["I am happy", "I am sad", "I am stressed"],
        "risk": ["low", "high", "medium"]
    }
    df = pd.DataFrame(dummy_data)
    
    # Path to temp dataset
    temp_csv = tmp_path / "test_dataset.csv"
    df.to_csv(temp_csv, index=False)
    
    # Temporarily override settings for this test
    original_data_path = settings.DATA_PATH
    original_model_path = settings.MODEL_PATH
    original_vec_path = settings.VECTORIZER_PATH
    
    settings.DATA_PATH = str(temp_csv)
    settings.MODEL_PATH = str(tmp_path / "test_model.pkl")
    settings.VECTORIZER_PATH = str(tmp_path / "test_vec.pkl")
    
    try:
        # Run the training function
        train_model()
        
        # Verify files were created
        assert os.path.exists(settings.MODEL_PATH)
        assert os.path.exists(settings.VECTORIZER_PATH)
    finally:
        # Restore original settings
        settings.DATA_PATH = original_data_path
        settings.MODEL_PATH = original_model_path
        settings.VECTORIZER_PATH = original_vec_path

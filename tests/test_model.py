import pytest

from model.predict import MentalHealthPredictor


@pytest.fixture
def predictor():
    return MentalHealthPredictor()

def test_predictor_initialization(predictor):
    assert predictor.classifier is not None
    assert predictor.emotion_analyzer is not None

def test_predictor_predict(predictor):
    result = predictor.predict("I feel very lonely and sad")
    assert "risk" in result
    assert "score" in result
    assert "keywords" in result
    assert isinstance(result["risk"], str)
    assert isinstance(result["score"], float)
    assert isinstance(result["keywords"], list)

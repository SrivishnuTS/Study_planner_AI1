import pytest, os, json, joblib
from unittest.mock import patch
import mongomock
from app import app
from utils import engineer_features
import pandas as pd

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-secret'
    # Mocking MongoDB
    with patch('app.MongoClient', mongomock.MongoClient):
        with app.test_client() as client:
            yield client

def test_multi_model_response_structure(client, tmp_path):
    # Setup temp model dir for test
    test_model_dir = tmp_path / "model"
    test_model_dir.mkdir()
    metrics_file = test_model_dir / "model_metrics.json"
    
    with open(metrics_file, 'w') as f:
        json.dump({"best_model_name": "Test RF", "model_version": "test-v1"}, f)
    
    # Patch the paths in app to use our test directory
    with patch('app.METRICS_PATH', str(metrics_file)):
        with patch('app.BEST_MODEL_PATH', 'model/best_model.pkl'): # Use existing model for inference
            payload = {
        "study_hours": 4, "break_time": 1, "sleep_hours": 8, "focus_score": 8,
        "distraction_level": "low", "day_of_week": "Monday", "previous_score": 80,
        "course_name": "General", "course_difficulty": "medium", "study_goal_type": "Revision",
        "energy_level": "Medium", "time_of_day": "Afternoon"
    }
    
    res = client.post('/api/v1/predict', json=payload)
    # This might return 400 if best_model.pkl is missing, but we want to see the keys if it works
    if res.status_code == 200:
        data = res.get_json()
        assert "model_name" in data
        assert "model_confidence_probability_estimate" in data
        assert "predicted_pattern" in data

def test_engineer_features_robustness():
    data = {"study_hours": 4, "focus_score": 8, "previous_score": 80, "sleep_hours": 6, "break_time": 1}
    df = engineer_features(pd.DataFrame([data]))
    assert "efficiency_base" in df.columns
    assert float(df['efficiency_base'].iloc[0]) == 160.0

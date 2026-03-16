from fastapi import APIRouter, HTTPException
from src.app.models.trip import TripInput
import joblib
import pandas as pd
import os

router = APIRouter(tags=['ML Prediction'])

# Global variable to hold the model
model = None

# Load model on startup
MODEL_PATH = 'src/ml/trip_predictor.joblib'

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

@router.post('/predict')
def predict_duration(data: TripInput):
    if not model:
        raise HTTPException(status_code=500, detail='Model not loaded')
    
    # Sklearn expects a DataFrame or 2d array
    features = pd.DataFrame({
        'distance': [data.distance_km],
        'battery': [data.battery_level]
    })

    prediction = model.predict(features)[0]

    return {
        'distance_km': data.distance_km,
        'estimated_minutes': round(prediction, 1)
    }
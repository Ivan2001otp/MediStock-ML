from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os

from ml_logic import load_model, preprocess_data

app = FastAPI(
    title="MediStock ML service",
    description="Provides vendor recommendation based on historical performance.",
    version="0.1.0"
)

ML_MODEL = None
ML_FEATURES = None
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'vendor_recommender_model.joblib')



class PredictionRequest(BaseModel) :
    unit_price:float
    quality_rating:int
    avg_delivery_days:int



# fast api life cycle events 
@app.on_event("startup")
async def startup_event():
    global ML_MODEL, ML_FEATURES
    try:
        ML_MODEL, ML_FEATURES = load_model()
        print("ML model loaded successfully")
        print(f"Model expects features: {ML_FEATURES}")
    except FileNotFoundError:
        print(f"Error: Model file not found at {MODEL_PATH}. Please run ml_logic.py to train and save the model.")
        raise HTTPException(status_code=500, detail="ML Model not found. Please train the model first.")
    except Exception as e:
        print(f"Error loading ML model: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load ML model: {e}")
 

# API Endpoints starts from here onwards
@app.get("/")
async def health_check():
    return {"status":"ok","message":"Medistock AI Ml-service is running !"}


@app.post("/predict")
async def predict_vendor_score(request: PredictionRequest) :
    if ML_MODEL is None or ML_FEATURES is None :
        raise HTTPException(status_code=500, detail="ML model not loaded .")
    
    try :
        input_data_dict : dict = {
            "unit_price":request.unit_price,
            "quality_rating":request.quality_rating,
            "avg_delivery_days":request.avg_delivery_days
        }

        input_df = pd.DataFrame([input_data_dict], columns = ML_FEATURES)


        #make prediction
        predicted_score = ML_MODEL.predict(input_df)[0]
        return {"predicted_outcome_score":round(float(predicted_score), 4)}

    except Exception as e:
        print(f"Prediction error : {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed : {e}")
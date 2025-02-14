import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# ✅ Ensure correct file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "intrusion_lgbm.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "model", "scaler.pkl")

# ✅ Load AI Model & Scaler
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
model = joblib.load(MODEL_PATH)

if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"Scaler file not found: {SCALER_PATH}")
scaler = joblib.load(SCALER_PATH)

app = FastAPI()

# ✅ Define API Schema
class NetworkData(BaseModel):
    features: List[List[float]]  # Accepts multiple packets

# ✅ Prediction Endpoint
@app.post("/predict/")
def predict_intrusion(data: NetworkData):
    X = np.array(data.features)  # Convert list to NumPy array

    # 🚨 Validate input
    if X.shape[1] == 0:
        raise HTTPException(status_code=400, detail="Invalid input: No features provided.")

    X_scaled = scaler.transform(X)
    preds = model.predict(X_scaled)  # Predict for all packets

    # Return 1 if any packet is an intrusion
    intrusion_detected = int(any(preds))
    return {"intrusion": intrusion_detected}

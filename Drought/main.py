from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import joblib
import numpy as np
import sqlite3
from typing import Optional
import os

MODEL_DIR = "models"
DB = "alerts.db"
ALERT_DROUGHT_PROB_THRESHOLD = 0.6
ALERT_DEMAND_SUPPLY_RATIO = 1.1

app = FastAPI(title="Drought Prediction & Alert API")

# Allow CORS from all origins (so your browser can call the API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_models():
    files = {
        "drought": "drought_clf.joblib",
        "demand": "demand_reg.joblib",
        "supply": "supply_reg.joblib"
    }
    models = {}
    for key, fname in files.items():
        path = os.path.join(MODEL_DIR, fname)
        if not os.path.exists(path):
            raise RuntimeError(f"Model file missing: {path}. Run training first.")
        models[key] = joblib.load(path)
    return models["drought"], models["demand"], models["supply"]

try:
    drought_m, demand_m, supply_m = load_models()
except RuntimeError as e:
    print(f"❌ {e}")
    drought_m = demand_m = supply_m = None

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""
      CREATE TABLE IF NOT EXISTS subscribers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        email TEXT,
        phone TEXT
      )
    """)
    conn.commit()
    conn.close()

init_db()

class Sample(BaseModel):
    city: str
    rainfall_mm: float
    avg_temp_c: float
    soil_moisture: float
    reservoir_level: float
    population: int
    past_month_consumption: float

class Subscribe(BaseModel):
    city: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

def fe_transform(sample: Sample):
    rainfall_3m = sample.rainfall_mm
    avg_temp_3m = sample.avg_temp_c
    resv_pop_ratio = sample.reservoir_level / (sample.population + 1e-6)
    consumption_lag1 = sample.past_month_consumption
    features = np.array([
        sample.rainfall_mm, sample.avg_temp_c, sample.soil_moisture,
        sample.reservoir_level, rainfall_3m, avg_temp_3m, resv_pop_ratio,
        consumption_lag1, sample.population
    ]).reshape(1, -1)
    return features

@app.post("/predict")
def predict(sample: Sample):
    if drought_m is None:
        raise HTTPException(status_code=500, detail="Models not loaded. Train them first.")
    X = fe_transform(sample)
    drought_model = drought_m["model"]
    demand_model = demand_m["model"]
    supply_model = supply_m["model"]

    prob = drought_model.predict_proba(X)[0,1]
    demand = float(demand_model.predict(X)[0])
    supply = float(supply_model.predict(X)[0])
    return {
        "city": sample.city,
        "drought_probability": prob,
        "predicted_demand_m3": demand,
        "predicted_supply_m3": supply
    }

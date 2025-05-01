from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
import pandas as pd # type: ignore
import joblib # type: ignore
import os

app = FastAPI(title="AgroChill Price Forecast API")

# Load trained models (assumes a dictionary of models saved as models.pkl)
MODEL_PATH = "models.pkl"
if os.path.exists(MODEL_PATH):
    models = joblib.load(MODEL_PATH)
else:
    models = {}  # fallback for development

# === Request schemas ===
class ForecastRequest(BaseModel):
    region: str
    commodity: str
    features: list  # List of 4 dictionaries with feature names

class NewDataRequest(BaseModel):
    data: list  # List of rows (dicts)

# === API Endpoints ===

@app.get("/")
def read_root():
    return {"message": "AgroChill forecasting API is running."}

@app.post("/forecast")
def forecast(req: ForecastRequest):
    key = (req.region, req.commodity)
    if key not in models:
        raise HTTPException(status_code=404, detail=f"No model found for {req.region}-{req.commodity}")
    
    model = models[key]
    df = pd.DataFrame(req.features)

    if df.empty or len(df.columns) == 0:
        raise HTTPException(status_code=400, detail="Invalid or missing feature data")

    predictions = model.predict(df).tolist()
    return {
        "region": req.region,
        "commodity": req.commodity,
        "predictions": predictions
    }

@app.post("/new-weather-data")
def add_weather_data(payload: NewDataRequest):
    new_df = pd.DataFrame(payload.data)
    new_df.to_csv("new_weather_data.csv", index=False)
    return {"message": f"Received {len(new_df)} new weather rows."}

@app.post("/new-price-data")
def add_price_data(payload: NewDataRequest):
    new_df = pd.DataFrame(payload.data)
    new_df.to_csv("new_price_data.csv", index=False)
    return {"message": f"Received {len(new_df)} new price rows."}

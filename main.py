from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import xgboost as xgb
import os
import csv

app = FastAPI(
    title="AgroChill Forecasting API",
    description="Predict crop prices and accept weather/price updates",
    version="2.0"
)

# Load the trained XGBoost model
MODEL_PATH = "model/xgboost_model.json"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("Trained model not found. Please train it before running the API.")

model = xgb.XGBRegressor()
model.load_model(MODEL_PATH)

# Root checkS
@app.get("/")
def root():
    return {"message": "AgroChill API is running ✅"}

# ------------------------
# Forecast Endpoint
# ------------------------

class ForecastFeatureSet(BaseModel):
    Temperature_K: float
    Rainfall_mm: float
    Humidity_percent: float
    Crop_Yield_Impact_Score: float
    Year: int
    Month: int
    Week_Num: int
    lag_1: float
    lag_2: float
    lag_3: float
    lag_4: float

class ForecastRequest(BaseModel):
    region: str
    commodity: str
    features: list[ForecastFeatureSet]

@app.post("/forecast")
def forecast_price(request: ForecastRequest):
    try:
        predictions = []

        for feature in request.features:
            input_dict = {
                "temperature": feature.Temperature_K,
                "rainfall": feature.Rainfall_mm,
                "humidity": feature.Humidity_percent,
                "yield_impact_score": feature.Crop_Yield_Impact_Score,
                "lag_1": feature.lag_1,
                "lag_2": feature.lag_2,
                "lag_3": feature.lag_3,
                "lag_4": feature.lag_4,
                "weekofyear": feature.Week_Num,
                "month": feature.Month,
                "season": (feature.Month % 12) // 3 + 1  # Auto-calculated
            }

            input_df = pd.DataFrame([input_dict])
            pred = model.predict(input_df)[0]
            predictions.append(round(pred, 2))

        return {
            "region": request.region,
            "commodity": request.commodity,
            "predicted_prices": predictions
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------
# Add New Weather Data
# ------------------------

class WeatherData(BaseModel):
    Date: str
    Region: str
    temperature: float
    rainfall: float
    humidity: float
    yield_impact_score: float

@app.post("/weather")
def add_weather_data(weather: WeatherData):
    filename = "data/weather_live.csv"
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=weather.dict().keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(weather.dict())
    return {"message": "✅ Weather data received and saved."}

# ------------------------
# Add New Price Data
# ------------------------

class PriceData(BaseModel):
    Date: str
    Region: str
    Commodity: str
    price: float
    type: str

@app.post("/price")
def add_price_data(price: PriceData):
    filename = "data/price_live.csv"
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=price.dict().keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(price.dict())
    return {"message": "✅ Price data received and saved."}

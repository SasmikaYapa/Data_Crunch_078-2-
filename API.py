# Save this as main.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from prophet import Prophet

app = FastAPI()

class ForecastRequest(BaseModel):
    region: str
    commodity: str

@app.post("/predict")
def predict_price(data: ForecastRequest):
    # Load your preprocessed dataset
    df = pd.read_csv("merged_data.csv", parse_dates=["Date"])

    df = df[(df['Region'] == data.region) & (df['Commodity'] == data.commodity)]
    prophet_df = df[['Date', 'price']].rename(columns={"Date": "ds", "price": "y"})

    model = Prophet()
    model.fit(prophet_df)
    future = model.make_future_dataframe(periods=4, freq='W')
    forecast = model.predict(future)

    return forecast[['ds', 'yhat']].tail(4).to_dict(orient="records")

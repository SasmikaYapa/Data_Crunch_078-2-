
  

# 🌾 AgroChill Forecasting API — "The Freezer Gambit"

  

This project is a time-series forecasting API built for the DataCrunch 2025 competition, enabling agricultural market predictions to support cold-storage logistics.

  

---

  

## 🚀 Project Overview

  

AgroChill helps decide whether to **sell fresh produce immediately** or **freeze it for later**, based on predicted price trends. It supports:

  

- Rolling **4-week-ahead price forecasts** by region and commodity

- Data ingestion via API (weather and price updates)

- Dockerized deployment

  

---

  

## 📦 Project Structure

  

```

datacrunch_submission/

├── deployment/

│ ├── main.py # FastAPI app

│ ├── Dockerfile # Container config

│ ├── requirements.txt # Python dependencies

├── models.pkl # Trained XGBoost models (dict of models)

├── Documentation.pdf # Final report

├── Presentation.pptx # Slide deck

├── README.md # This file

└── image_name.txt # DockerHub image link

```

  

---

  

## 🔧 Setup Instructions (Local)

  

### 1. Clone or unzip this repository

  

```bash

git  clone <repo-link>

cd  datacrunch_submission/deployment

```

  

### 2. Install dependencies

  

```bash

pip  install  -r  requirements.txt

```

  

### 3. Run the FastAPI app

  

```bash

uvicorn  main:app  --host  0.0.0.0  --port  8000

```

  

---

  

## 🐳 Docker Deployment

  

### 1. Build the image

  

```bash

docker  build  -t  forecast-api  .

```

  

### 2. Run the container

  

```bash

docker  run  -d  -p  8000:8000  forecast-api

```

  

### 3. Access the API

  

Navigate to: [http://localhost:8000/docs](http://localhost:8000/docs)

  

---

  

## 📡 API Endpoints

  

### ➕ `/forecast` — POST

  

**Description**: Get 4-week price forecast.

  

```json

{

"region": "Starling City",

"commodity": "Snow Peas",

"features": [

{"Temperature (K)": 294, "Rainfall (mm)": 10, "Humidity (%)": 75, "Crop Yield Impact Score": 0.88, "Year": 2044, "Month": 4, "Week_Num": 18, "lag_1": 42.1, "lag_2": 39.8, "lag_3": 38.7, "lag_4": 37.5}

]

}

```

  

---

  

### ➕ `/new-weather-data` — POST

  

**Description**: Submit new weather data.

  

```json

{

"data": [

{"Date": "2045-05-01", "Region": "Mystic Falls", "Temperature (K)": 295, "Rainfall (mm)": 8}

]

}

```

  

---

  

### ➕ `/new-price-data` — POST

  

**Description**: Submit new price data.

  

```json

{

"data": [

{"Date": "2045-05-01", "Region": "Mystic Falls", "Commodity": "Tomato", "Price per Unit (Silver Drachma/kg)": 58.7}

]

}

```

  

---

  

## 📊 Evaluation Metrics

  

- RMSE (rolling forecast): 4.2 – 7.1 across regions

- R²: 0.70 – 0.89

- Model type: XGBoost/ LightGBM

- Docker size: ~700MB

- RAM usage: <2GB

  

---

  

## 🧠 Authors & Contributors

  

Team AgroChill — University of Moratuwa

Contact: your_email@domain.com

  

---

  

## 🏁 Submission Checklist

  

- [x] Code & models packaged

- [x] Dockerfile included

- [x] APIs tested and documented

- [x] Report and Presentation attached

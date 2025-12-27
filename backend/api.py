from fastapi import FastAPI
import joblib, requests, pandas as pd
from datetime import datetime

app = FastAPI()
model = joblib.load("../model/rain_model.pkl")

THRESHOLD = 0.35
FEATURES = [
    "temperature_2m",
    "relative_humidity_2m",
    "cloud_cover",
    "pressure_msl",
    "wind_speed_10m",
    "hour"
]

def get_lat_lon(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    return requests.get(url).json()["results"][0]["latitude"], \
           requests.get(url).json()["results"][0]["longitude"]

@app.get("/predict")
def predict(city: str):
    lat, lon = get_lat_lon(city)

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,relative_humidity_2m,"
        "cloud_cover,pressure_msl,wind_speed_10m,precipitation"
        "&timezone=America/New_York"
    )

    hourly = requests.get(url).json()["hourly"]
    df = pd.DataFrame(hourly)
    row = df.iloc[0]
    row["hour"] = datetime.now().hour

    X = row[FEATURES].values.reshape(1, -1)
    prob = float(model.predict_proba(X)[0][1])

    return {
        "city": city,
        "rain_probability": round(prob, 2),
        "rain_next_hour": prob >= THRESHOLD,
        "threshold": THRESHOLD
    }

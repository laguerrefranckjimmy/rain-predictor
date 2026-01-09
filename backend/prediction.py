import requests
import numpy as np
from backend.config import RAIN_THRESHOLD
from backend.convertcity import get_lat_lon


def fetch_hourly_weather(lat: float, lon: float):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability",
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def predict_rain(city: str, model):
    lat, lon = get_lat_lon(city)
    weather = fetch_hourly_weather(lat, lon)

    # Next hour prediction
    temp = weather["hourly"]["temperature_2m"][0]
    humidity = weather["hourly"]["relative_humidity_2m"][0]

    X = np.array([[temp, humidity]])

    rain_probability = float(model.predict_proba(X)[0][1])
    rain_expected = rain_probability >= RAIN_THRESHOLD

    return {
        "city": city,
        "latitude": lat,
        "longitude": lon,
        "rain_probability": round(rain_probability, 3),
        "rain_next_hour": rain_expected,
        "threshold": RAIN_THRESHOLD
    }
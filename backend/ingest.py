import pandas as pd
import requests
from convertcity import get_lat_lon

def fetch_weather(city):
    lat, lon = get_lat_lon(city)

    url = (
        "https://archive-api.open-meteo.com/v1/archive"
        f"?latitude={lat}&longitude={lon}"
        "&start_date=2023-01-01"
        "&end_date=2024-12-31"
        "&hourly=temperature_2m,relative_humidity_2m,"
        "cloud_cover,precipitation,pressure_msl,wind_speed_10m"
        "&timezone=America/New_York"
    )

    data = requests.get(url).json()["hourly"]
    df = pd.DataFrame(data)
    return df

df = fetch_weather("Miami")
df.to_csv("../data/weather_hourly.csv", index=False)

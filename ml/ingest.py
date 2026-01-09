import pandas as pd
import requests
import boto3

import sys
from pathlib import Path
# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.config import S3_BUCKET, DATA_KEY, CITIES
from backend.convertcity import get_lat_lon


s3 = boto3.client("s3")

def fetch_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=precipitation_probability,temperature_2m,relative_humidity_2m"
        "&timezone=America/New_York"
    )
    return requests.get(url).json()

rows = []

for city in CITIES:
    lat, lon = get_lat_lon(city)
    data = fetch_weather(lat, lon)

    for i in range(len(data["hourly"]["temperature_2m"])):
        rows.append({
            "city": city,
            "temp": data["hourly"]["temperature_2m"][i],
            "humidity": data["hourly"]["humidity"][i],
            "rain": int(data["hourly"]["precipitation_probability"][i] > 30)
        })

df = pd.DataFrame(rows)
local_csv = "/tmp/weather.csv"
df.to_csv(local_csv, index=False)

s3.upload_file(local_csv, S3_BUCKET, DATA_KEY)
print("✅ CSV uploaded to S3")

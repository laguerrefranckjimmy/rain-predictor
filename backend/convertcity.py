import requests

def get_lat_lon(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    res = requests.get(url).json()

    if "results" not in res:
        raise ValueError("City not found")

    loc = res["results"][0]
    return loc["latitude"], loc["longitude"]

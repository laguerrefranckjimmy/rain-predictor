import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("../data/weather_hourly.csv")
df["time"] = pd.to_datetime(df["time"])

# Feature: hour of day
df["hour"] = df["time"].dt.hour

# Label: rain or not
df["rain"] = (df["precipitation"] > 0).astype(int)

FEATURES = [
    "temperature_2m",
    "relative_humidity_2m",
    "cloud_cover",
    "pressure_msl",
    "wind_speed_10m",
    "hour"
]

X = df[FEATURES]
y = df["rain"]



X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)

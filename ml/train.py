import boto3
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression
from backend.config import S3_BUCKET, DATA_KEY, MODEL_KEY

s3 = boto3.client("s3")

csv_path = "/tmp/weather.csv"
model_path = "/tmp/rain_model.pkl"

s3.download_file(S3_BUCKET, DATA_KEY, csv_path)

df = pd.read_csv(csv_path)

X = df[["temp", "humidity"]]
y = df["rain"]

model = LogisticRegression()
model.fit(X, y)

joblib.dump(model, model_path)
s3.upload_file(model_path, S3_BUCKET, MODEL_KEY)

print("✅ Model trained & uploaded to S3")

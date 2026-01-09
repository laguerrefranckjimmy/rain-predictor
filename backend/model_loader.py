import boto3
import joblib
import os
from backend.config import S3_BUCKET, MODEL_KEY

s3 = boto3.client("s3")
LOCAL_MODEL_PATH = "/tmp/rain_model.pkl"

model = None

def load_model():
    global model
    try:
        s3.download_file(S3_BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)
        model = joblib.load(LOCAL_MODEL_PATH)
        print("✅ Model loaded from S3")
    except Exception as e:
        model = None
        print("⚠️ Model not available yet:", e)

def get_model():
    return model
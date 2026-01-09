import boto3
import joblib
import os
from backend.config import S3_BUCKET, MODEL_KEY

# Where the model will be stored locally
LOCAL_MODEL_PATH = "/tmp/rain_model.pkl"

# Global model object
model = None

# S3 client (uses EC2 IAM role)
s3 = boto3.client("s3")


def load_model():
    """Download model from S3 and load it into memory."""
    global model
    try:
        # Download model from S3
        s3.download_file(S3_BUCKET, MODEL_KEY, LOCAL_MODEL_PATH)
        # Load model
        model = joblib.load(LOCAL_MODEL_PATH)
        print("✅ Model loaded from S3")
    except Exception as e:
        model = None
        print("⚠️ Model not available yet:", e)


def get_model():
    return model
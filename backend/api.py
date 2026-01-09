from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from backend.model_loader import load_model, get_model
from backend.prediction import predict_rain

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    load_model()  # safe even if model missing
    yield
    # Shutdown logic (if any)
    # e.g., closing DB connections, cleanup

# Create app with lifespan
app = FastAPI(lifespan=lifespan)

# API endpoint
@app.get("/predict")
def predict(city: str):
    model = get_model()
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not trained yet. Please try again later."
        )
    return predict_rain(city, model)

# Serve React frontend
app.mount(
    "/",
    StaticFiles(directory="frontend/dist", html=True),
    name="frontend",
)

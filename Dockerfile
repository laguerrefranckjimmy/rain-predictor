FROM python:3.10-slim

WORKDIR /app

# Copy backend code only
COPY backend/ ./backend/
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

# Start the FastAPI server
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "80"]
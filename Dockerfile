FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY ml/ ml/
COPY frontend/dist frontend/dist

EXPOSE 80

CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "80"]
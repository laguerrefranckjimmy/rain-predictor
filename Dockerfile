FROM python:3.10-slim

WORKDIR /app
COPY backend/ ./backend/
COPY model/ ./model/
COPY data/ ./data/
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "80"]
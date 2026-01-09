# Stage 1: Build React
FROM node:20 as frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Stage 2: Build backend + combine frontend
FROM python:3.10-slim
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY ml/ ml/

# Copy frontend build from previous stage
COPY --from=frontend-build /app/frontend/dist frontend/dist

EXPOSE 80
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "80"]
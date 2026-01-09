#!/bin/bash
set -e

echo "⏳ Ingesting data..."
python ml/ingest.py

echo "⏳ Training model..."
python ml/train.py

echo "♻ Reloading model in API..."
docker restart rain-predictor-container

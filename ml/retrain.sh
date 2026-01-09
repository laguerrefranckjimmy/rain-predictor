#!/bin/bash
set -e

echo "==== Retrain started at $(date) ===="

# Go to project directory
cd /home/ec2-user/ml

# Activate virtual environment
source .venv/bin/activate

# Use python3 explicitly
echo "⏳ Ingesting data..."
python3 backend/ingest.py

echo "⏳ Training model..."
python3 backend/train.py

echo "==== Retrain completed at $(date) ===="
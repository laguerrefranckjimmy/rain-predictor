#!/bin/bash
set -e

echo "==== Retrain started at $(date) ===="

# Go to project directory
cd /home/ec2-user/app/ml

# Activate virtual environment
source .venv/bin/activate

# Use python3 explicitly
echo "⏳ Ingesting data..."
python3 ingest.py

echo "⏳ Training model..."
python3 train.py

echo "==== Retrain completed at $(date) ===="
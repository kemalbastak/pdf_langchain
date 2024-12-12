#!/bin/bash

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head

# Start the FastAPI app
echo "Starting FastAPI server..."
python main.py
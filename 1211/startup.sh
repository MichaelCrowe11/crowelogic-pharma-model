#!/bin/bash
set -e

echo "=========================================="
echo "CroweLogic-Pharma NeuroDebian Startup"
echo "=========================================="

# Start Ollama service in background
echo "Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama to initialize..."
sleep 10

# Check if model exists, if not create it
echo "Checking for CroweLogic-Pharma model..."
if ! ollama list | grep -q "CroweLogic-Pharma"; then
    echo "Creating CroweLogic-Pharma model from Modelfile..."
    ollama create CroweLogic-Pharma:120b-v2 -f /app/Modelfile
else
    echo "Model already exists"
fi

# Start API server
echo "Starting FastAPI server..."
cd /app
python3 api_server.py

# Keep container running
wait $OLLAMA_PID

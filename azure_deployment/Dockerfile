# CroweLogic-Pharma Azure Deployment Dockerfile
# Multi-stage build for optimized deployment

FROM python:3.10-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create application directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY models/ ./models/
COPY training_data/ ./training_data/
COPY scripts/ ./scripts/

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose port for API
EXPOSE 11434 8000

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Ollama service..."\n\
ollama serve &\n\
sleep 5\n\
echo "Building CroweLogic-Pharma model..."\n\
ollama create CroweLogic-Pharma:latest -f /app/models/CroweLogicPharmaModelfile\n\
echo "Model ready!"\n\
tail -f /dev/null\n\
' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

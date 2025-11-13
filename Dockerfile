# CroweLogic Pharma Model - Pharmaceutical Data Generation
# Author: Michael Crowe
# Description: Generate large-scale pharmaceutical datasets for AI/ML training

FROM python:3.10-slim

LABEL maintainer="Michael Crowe"
LABEL description="Pharmaceutical compound data generation for AI/ML training"
LABEL version="1.0"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files (excluding large files via .dockerignore)
COPY *.py ./
COPY *.sh ./
COPY *.md ./

# Create necessary directories
RUN mkdir -p logs cache generated_data/batches

# Make scripts executable
RUN chmod +x *.sh 2>/dev/null || true

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command: show available commands
CMD ["python3", "-c", "print('\\nCroweLogic Pharma Model - Docker Environment\\n' + '='*50 + '\\n\\nAvailable commands:\\n  • python3 generate_10m_fast.py\\n  • python3 evaluate_dataset_quality.py\\n  • python3 collect_cloud_results.py\\n\\nFor documentation, see README.md\\n')"]

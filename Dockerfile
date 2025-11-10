FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs cache generated_data/batches

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BATCH_ID=0
ENV BATCH_SIZE=1000

# Default command (can be overridden)
CMD python generate_batch.py --batch ${BATCH_ID} --batch-size ${BATCH_SIZE}

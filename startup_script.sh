#!/bin/bash
set -e

echo "Starting pharma data generation batch job..."

# Update system
sudo apt-get update
sudo apt-get install -y python3-pip git awscli

# Clone repository
cd /home/ubuntu
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git || echo "Repo already cloned"
cd crowelogic-pharma-model

# Install dependencies
pip3 install -r requirements.txt

# Create directories
mkdir -p logs cache generated_data/batches

# Determine batch ID from instance metadata
if [ -f /sys/hypervisor/uuid ]; then
    # AWS EC2
    INSTANCE_ID=$(ec2-metadata --instance-id | cut -d " " -f 2)
    BATCH_ID=$(aws ec2 describe-tags --region us-east-1 --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=BatchID" --query "Tags[0].Value" --output text)
else
    # GCP
    BATCH_ID=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/batch-id" -H "Metadata-Flavor: Google")
fi

echo "Running batch generation for batch $BATCH_ID..."

# Run batch generation
python3 generate_batch.py --batch $BATCH_ID --batch-size 1000 2>&1 | tee logs/batch_${BATCH_ID}.log

# Upload results to cloud storage (UPDATE BUCKET NAME)
# For AWS S3:
aws s3 cp generated_data/batches/batch_${BATCH_ID}.jsonl s3://pharma-batch-20251110-michaelcrowe/batches/
aws s3 cp generated_data/batches/batch_${BATCH_ID}_stats.json s3://pharma-batch-20251110-michaelcrowe/batches/
aws s3 cp logs/batch_${BATCH_ID}.log s3://pharma-batch-20251110-michaelcrowe/logs/

# For GCP Cloud Storage:
# gsutil cp generated_data/batches/batch_${BATCH_ID}.jsonl gs://your-pharma-bucket/batches/
# gsutil cp generated_data/batches/batch_${BATCH_ID}_stats.json gs://your-pharma-bucket/batches/
# gsutil cp logs/batch_${BATCH_ID}.log gs://your-pharma-bucket/logs/

echo "Batch $BATCH_ID complete!"

# Optional: Shutdown instance to save costs
sudo shutdown -h now

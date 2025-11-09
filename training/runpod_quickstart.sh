#!/bin/bash
# RunPod Quick Start Script for CroweLogic-Pharma Training
# Run this script ON the RunPod GPU instance after uploading datasets

set -e  # Exit on error

echo "======================================================================"
echo "CroweLogic-Pharma RunPod Training Setup"
echo "======================================================================"
echo ""

# Check if running on GPU
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ ERROR: nvidia-smi not found. Are you on a GPU instance?"
    exit 1
fi

echo "✓ GPU detected:"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
echo ""

# Install dependencies
echo "======================================================================"
echo "Installing dependencies..."
echo "======================================================================"
echo ""

pip install --quiet --upgrade pip

echo "Installing transformers, datasets, peft..."
pip install --quiet transformers datasets peft

echo "Installing bitsandbytes (4-bit quantization)..."
pip install --quiet bitsandbytes

echo "Installing accelerate, trl..."
pip install --quiet accelerate trl

echo "Installing wandb (optional logging)..."
pip install --quiet wandb

echo ""
echo "✓ All dependencies installed"
echo ""

# Check for datasets
echo "======================================================================"
echo "Checking for datasets..."
echo "======================================================================"
echo ""

TRAIN_FILE="/workspace/crowelogic_pharma_100k_train.jsonl"
VAL_FILE="/workspace/crowelogic_pharma_100k_val.jsonl"

if [ -f "$TRAIN_FILE" ]; then
    TRAIN_LINES=$(wc -l < "$TRAIN_FILE")
    echo "✓ Training data found: $TRAIN_LINES examples"
else
    echo "❌ Training data not found at: $TRAIN_FILE"
    echo "   Please upload crowelogic_pharma_100k_train.jsonl to /workspace/"
    exit 1
fi

if [ -f "$VAL_FILE" ]; then
    VAL_LINES=$(wc -l < "$VAL_FILE")
    echo "✓ Validation data found: $VAL_LINES examples"
else
    echo "❌ Validation data not found at: $VAL_FILE"
    echo "   Please upload crowelogic_pharma_100k_val.jsonl to /workspace/"
    exit 1
fi

echo ""

# Check for training script
TRAIN_SCRIPT="/workspace/train_cloud_gpu.py"

if [ ! -f "$TRAIN_SCRIPT" ]; then
    echo "❌ Training script not found at: $TRAIN_SCRIPT"
    echo "   Please upload train_cloud_gpu.py to /workspace/"
    exit 1
fi

echo "✓ Training script found"
echo ""

# System info
echo "======================================================================"
echo "System Information"
echo "======================================================================"
echo ""

echo "GPU:"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader

echo ""
echo "CPU:"
cat /proc/cpuinfo | grep "model name" | head -1 | cut -d: -f2

echo ""
echo "RAM:"
free -h | grep Mem | awk '{print $2 " total, " $7 " available"}'

echo ""
echo "Disk:"
df -h /workspace | tail -1 | awk '{print $2 " total, " $4 " available"}'

echo ""

# Training configuration summary
echo "======================================================================"
echo "Training Configuration"
echo "======================================================================"
echo ""

echo "Model: Mistral-7B-v0.1"
echo "Method: QLoRA (4-bit quantization + LoRA)"
echo "Training examples: $TRAIN_LINES"
echo "Validation examples: $VAL_LINES"
echo "Estimated time: 4-8 hours"
echo "Output: /workspace/crowelogic-pharma-mistral-7b/"
echo ""

# Confirm before starting
echo "======================================================================"
echo "Ready to Start Training"
echo "======================================================================"
echo ""

read -p "Start training now? (yes/no): " START_TRAINING

if [ "$START_TRAINING" != "yes" ]; then
    echo ""
    echo "Training cancelled. To start manually:"
    echo "  cd /workspace"
    echo "  python3 train_cloud_gpu.py"
    echo ""
    exit 0
fi

echo ""
echo "======================================================================"
echo "Starting Training..."
echo "======================================================================"
echo ""

# Start training
cd /workspace
python3 train_cloud_gpu.py

# Check if training succeeded
if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================================"
    echo "Training Completed Successfully!"
    echo "======================================================================"
    echo ""

    echo "Model saved to: /workspace/crowelogic-pharma-mistral-7b/"
    echo ""

    echo "Download to your local machine:"
    echo "  1. Zip the model:"
    echo "     cd /workspace"
    echo "     zip -r crowelogic_pharma_model.zip crowelogic-pharma-mistral-7b/"
    echo ""
    echo "  2. Download via SCP (from your local M1 Mac):"
    echo "     scp root@<pod-ip>:/workspace/crowelogic_pharma_model.zip ~/"
    echo ""
    echo "  3. Or use RunPod's file browser to download"
    echo ""

    echo "⚠️  IMPORTANT: Terminate your pod to stop billing!"
    echo "   RunPod Dashboard → My Pods → Terminate"
    echo ""

else
    echo ""
    echo "======================================================================"
    echo "Training Failed"
    echo "======================================================================"
    echo ""
    echo "Check the error messages above."
    echo "Common issues:"
    echo "  - Out of memory: Reduce BATCH_SIZE in train_cloud_gpu.py"
    echo "  - Model download failed: Check internet connection"
    echo "  - CUDA errors: Check GPU compatibility"
    echo ""
fi

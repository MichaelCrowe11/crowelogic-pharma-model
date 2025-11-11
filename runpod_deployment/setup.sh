#!/bin/bash
# RunPod Setup Script

echo "=== RunPod Pharma Data Generation Setup ==="
echo ""

# Install dependencies
pip install requests tqdm

# Clone repo
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Create directories
mkdir -p logs generated_data/massive

echo ""
echo "✓ Setup complete!"
echo ""
echo "To start generation:"
echo "  nohup python3 generate_10m_optimized.py --target 5000000 --output-dir generated_data/massive > generation.out 2>&1 &"
echo ""
echo "To monitor:"
echo "  tail -f generation.out"
echo ""

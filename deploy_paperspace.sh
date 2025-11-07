#!/bin/bash
# CroweLogic-Pharma Paperspace Deployment Script

set -e

echo "🚀 CroweLogic-Pharma Paperspace Deployment"
echo "=========================================="
echo ""

# Configuration
APP_NAME="crowelogic-pharma"
MACHINE_TYPE="C7"  # 8 CPU, 30GB RAM - $0.07/hr (~$50/month if 24/7)
GPU_MACHINE_TYPE="P4000"  # GPU option - $0.51/hr (~$367/month if 24/7)

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if paperspace CLI is installed
if ! command -v paperspace &> /dev/null; then
    echo "❌ Paperspace CLI not found. Installing..."
    echo ""
    echo "Run: npm install -g paperspace-node"
    echo "Or visit: https://docs.paperspace.com/gradient/cli/"
    exit 1
fi

# Check authentication
if ! paperspace machines list &> /dev/null; then
    echo "❌ Not authenticated with Paperspace"
    echo "Run: paperspace login"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites met${NC}"
echo ""

# Choose machine type
echo -e "${BLUE}🔧 Choose machine type:${NC}"
echo "1. CPU (C7: 8 CPU, 30GB RAM, \$0.07/hr)"
echo "2. GPU (P4000: 8GB GPU, \$0.51/hr) - For 33B-70B models"
echo ""
read -p "Enter choice (1 or 2): " MACHINE_CHOICE

if [ "$MACHINE_CHOICE" = "2" ]; then
    SELECTED_MACHINE=$GPU_MACHINE_TYPE
    MODEL_SIZE="70b"
    BASE_MODEL="llama3.1:70b"
else
    SELECTED_MACHINE=$MACHINE_TYPE
    MODEL_SIZE="3b"
    BASE_MODEL="llama3.2:latest"
fi

echo ""
echo -e "${BLUE}📦 Creating Dockerfile...${NC}"

cat > Dockerfile.paperspace << EOF
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    ca-certificates \\
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Create app directory
WORKDIR /app

# Copy model files
COPY models/ /app/models/
COPY training_data/ /app/training_data/

# Environment
ENV OLLAMA_HOST=0.0.0.0:11434
ENV BASE_MODEL=${BASE_MODEL}

# Setup script
RUN cat > /app/setup.sh << 'SETUP'
#!/bin/bash
set -e

echo "Starting Ollama service..."
ollama serve &
OLLAMA_PID=\$!

echo "Waiting for Ollama to start..."
sleep 15

echo "Pulling base model (\${BASE_MODEL})..."
ollama pull \${BASE_MODEL}

echo "Creating CroweLogic-Pharma model..."
# Update Modelfile with correct base
sed "s|FROM.*|FROM \${BASE_MODEL}|" /app/models/CroweLogicPharmaModelfile-practical > /tmp/Modelfile
ollama create CroweLogic-Pharma:latest -f /tmp/Modelfile

echo "✅ CroweLogic-Pharma model ready!"
echo "API available at http://0.0.0.0:11434"

wait \$OLLAMA_PID
SETUP

RUN chmod +x /app/setup.sh

EXPOSE 11434

CMD ["/app/setup.sh"]
EOF

# Build Docker image
echo -e "${BLUE}🔨 Building Docker image...${NC}"
docker build -f Dockerfile.paperspace -t $APP_NAME:paperspace .

echo -e "${GREEN}✅ Docker image built${NC}"
echo ""

# Method 1: Gradient Deployments (Recommended)
echo -e "${BLUE}🚀 Deploying via Gradient Deployments...${NC}"

# Create deployment spec
cat > gradient-deployment.yaml << EOF
image: $APP_NAME:paperspace
port: 11434
resources:
  replicas: 1
  instanceType: $SELECTED_MACHINE
env:
  - name: OLLAMA_HOST
    value: "0.0.0.0:11434"
  - name: BASE_MODEL
    value: "$BASE_MODEL"
EOF

# Save and push Docker image to Paperspace registry
echo -e "${BLUE}📤 Pushing image to Paperspace...${NC}"
docker save $APP_NAME:paperspace | gzip > /tmp/crowelogic-pharma-paperspace.tar.gz

echo ""
echo -e "${YELLOW}⚠️  Manual steps required:${NC}"
echo ""
echo "1. Upload Docker image to Paperspace:"
echo "   - Go to: https://console.paperspace.com/gradient"
echo "   - Navigate to: Containers → Private Registry"
echo "   - Upload: /tmp/crowelogic-pharma-paperspace.tar.gz"
echo ""
echo "2. Create Deployment:"
echo "   - Navigate to: Deployments → Create"
echo "   - Container: Select your uploaded image"
echo "   - Machine: $SELECTED_MACHINE"
echo "   - Port: 11434"
echo "   - Click: Deploy"
echo ""
echo "3. Alternative - Use Paperspace Notebook:"

cat > paperspace_notebook_setup.py << 'PYTHON'
#!/usr/bin/env python3
"""
Run this in a Paperspace Gradient Notebook
"""

import os
import subprocess

print("🚀 Setting up CroweLogic-Pharma in Paperspace Notebook")
print("=" * 60)

# Install Ollama
print("\n📦 Installing Ollama...")
subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True)

# Start Ollama
print("\n🔄 Starting Ollama service...")
subprocess.Popen(["ollama", "serve"])

import time
time.sleep(10)

# Choose model based on GPU
import torch
has_gpu = torch.cuda.is_available()
base_model = "llama3.1:70b" if has_gpu else "llama3.2:latest"

print(f"\n📥 Pulling base model: {base_model}")
subprocess.run(f"ollama pull {base_model}", shell=True)

# Clone repository
print("\n📂 Cloning CroweLogic-Pharma repository...")
if not os.path.exists("crowelogic-pharma-model"):
    subprocess.run("git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git", shell=True)

os.chdir("crowelogic-pharma-model")

# Update Modelfile
print("\n🔧 Creating custom model...")
with open("models/CroweLogicPharmaModelfile-practical", "r") as f:
    modelfile = f.read()

# Update base model
modelfile = modelfile.split('\n')
modelfile[0] = f"FROM {base_model}"
modelfile = '\n'.join(modelfile)

with open("/tmp/Modelfile", "w") as f:
    f.write(modelfile)

# Create model
subprocess.run("ollama create CroweLogic-Pharma:latest -f /tmp/Modelfile", shell=True)

print("\n✅ CroweLogic-Pharma is ready!")
print("\nTest with:")
print('ollama run CroweLogic-Pharma:latest "What are the therapeutic benefits of hericenones?"')
print("\nOr use the API:")
print(f"curl http://localhost:11434/api/generate -d '{{'model':'CroweLogic-Pharma:latest','prompt':'Your question'}}'")
PYTHON

chmod +x paperspace_notebook_setup.py

echo ""
echo "4. Or run setup script in Paperspace Notebook:"
echo "   - Create new Gradient Notebook (Free GPU available!)"
echo "   - Upload: paperspace_notebook_setup.py"
echo "   - Run: python paperspace_notebook_setup.py"
echo ""
echo -e "${GREEN}📄 Files created:${NC}"
echo "   - Dockerfile.paperspace"
echo "   - gradient-deployment.yaml"
echo "   - paperspace_notebook_setup.py"
echo "   - /tmp/crowelogic-pharma-paperspace.tar.gz"
echo ""
echo "🎉 Paperspace deployment guide complete!"

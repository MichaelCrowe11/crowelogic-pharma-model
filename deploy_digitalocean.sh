#!/bin/bash
# CroweLogic-Pharma DigitalOcean Deployment Script

set -e

echo "🚀 CroweLogic-Pharma DigitalOcean Deployment"
echo "==========================================="
echo ""

# Configuration
APP_NAME="crowelogic-pharma"
REGION="nyc3"  # New York
DROPLET_SIZE="c-4"  # 4 CPU, 8GB RAM, ~$48/month
DOCKER_IMAGE="$APP_NAME:latest"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo "❌ doctl CLI not found. Installing..."
    echo ""
    echo "Please run:"
    echo "  1. Download: https://github.com/digitalocean/doctl/releases"
    echo "  2. Install and add to PATH"
    echo "  3. Authenticate: doctl auth init"
    exit 1
fi

# Check authentication
if ! doctl account get &> /dev/null; then
    echo "❌ Not authenticated with DigitalOcean"
    echo "Run: doctl auth init"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites met${NC}"
echo ""

# Step 1: Build optimized Docker image
echo -e "${BLUE}📦 Building Docker image...${NC}"
cat > Dockerfile.digitalocean << 'EOF'
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Create app directory
WORKDIR /app

# Copy model files
COPY models/ /app/models/
COPY training_data/ /app/training_data/

# Setup script
COPY <<'SETUP' /app/setup.sh
#!/bin/bash
set -e

echo "Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
sleep 10

# Pull base model
echo "Pulling base model (llama3.2)..."
ollama pull llama3.2:latest

# Create CroweLogic-Pharma model
echo "Creating CroweLogic-Pharma model..."
ollama create CroweLogic-Pharma:latest -f /app/models/CroweLogicPharmaModelfile-practical

echo "✅ Model ready!"
echo "Keeping Ollama running..."
wait $OLLAMA_PID
SETUP

RUN chmod +x /app/setup.sh

# Expose Ollama port
EXPOSE 11434

# Run setup
CMD ["/app/setup.sh"]
EOF

docker build -f Dockerfile.digitalocean -t $DOCKER_IMAGE .
echo -e "${GREEN}✅ Docker image built${NC}"
echo ""

# Step 2: Deploy to DigitalOcean App Platform (easier) or Droplet
echo -e "${BLUE}🔧 Choose deployment method:${NC}"
echo "1. App Platform (Managed, auto-scaling)"
echo "2. Droplet (Full control, cheaper for 24/7)"
echo ""
read -p "Enter choice (1 or 2): " DEPLOY_METHOD

if [ "$DEPLOY_METHOD" = "1" ]; then
    # App Platform deployment
    echo -e "${BLUE}📤 Deploying to App Platform...${NC}"

    # Create container registry if not exists
    doctl registry create $APP_NAME-registry || true

    # Login to registry
    doctl registry login

    # Tag and push image
    REGISTRY_URL=$(doctl registry get --format URL --no-header)
    docker tag $DOCKER_IMAGE $REGISTRY_URL/$DOCKER_IMAGE
    docker push $REGISTRY_URL/$DOCKER_IMAGE

    # Create app spec
    cat > app.yaml << EOF
name: $APP_NAME
region: $REGION
services:
- name: pharma-api
  image:
    registry_type: DOCR
    repository: $DOCKER_IMAGE
    tag: latest
  http_port: 11434
  instance_count: 1
  instance_size_slug: professional-s  # 4 CPU, 8GB RAM
  routes:
  - path: /
EOF

    # Deploy app
    doctl apps create --spec app.yaml

    echo -e "${GREEN}✅ Deployed to App Platform!${NC}"
    echo ""
    echo "View your app:"
    doctl apps list

else
    # Droplet deployment
    echo -e "${BLUE}💧 Creating Droplet...${NC}"

    # Create droplet with Docker pre-installed
    DROPLET_ID=$(doctl compute droplet create $APP_NAME \
        --region $REGION \
        --size $DROPLET_SIZE \
        --image docker-20-04 \
        --ssh-keys $(doctl compute ssh-key list --format ID --no-header | head -1) \
        --wait \
        --format ID \
        --no-header)

    echo -e "${GREEN}✅ Droplet created: $DROPLET_ID${NC}"

    # Get droplet IP
    DROPLET_IP=$(doctl compute droplet get $DROPLET_ID --format PublicIPv4 --no-header)
    echo "IP Address: $DROPLET_IP"
    echo ""

    # Wait for droplet to be ready
    echo "Waiting for droplet to be ready..."
    sleep 30

    # Save Docker image
    echo -e "${BLUE}📦 Saving Docker image...${NC}"
    docker save $DOCKER_IMAGE | gzip > crowelogic-pharma.tar.gz

    # Upload and run
    echo -e "${BLUE}📤 Uploading to droplet...${NC}"
    scp -o StrictHostKeyChecking=no crowelogic-pharma.tar.gz root@$DROPLET_IP:/tmp/

    ssh -o StrictHostKeyChecking=no root@$DROPLET_IP << 'ENDSSH'
cd /tmp
gunzip crowelogic-pharma.tar.gz
docker load < crowelogic-pharma.tar
docker run -d -p 11434:11434 --name crowelogic-pharma crowelogic-pharma:latest
echo "Container started!"
ENDSSH

    echo -e "${GREEN}✅ Deployed to Droplet!${NC}"
    echo ""
    echo "🌐 Access your API at: http://$DROPLET_IP:11434"
    echo ""
    echo "Test with:"
    echo "curl http://$DROPLET_IP:11434/api/generate -d '{\"model\":\"CroweLogic-Pharma:latest\",\"prompt\":\"What are hericenones?\"}'"
fi

echo ""
echo "🎉 DigitalOcean deployment complete!"

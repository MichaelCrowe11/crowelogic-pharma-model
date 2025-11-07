#!/bin/bash
# CroweLogic-Pharma CLI Deployment Script
# Supports: Paperspace, DigitalOcean, Railway, Fly.io

set -e

echo "🚀 CroweLogic-Pharma CLI Deployment"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Choose platform
echo -e "${BLUE}Choose deployment platform:${NC}"
echo "1. Paperspace Gradient (recommended for ML)"
echo "2. DigitalOcean (simple, reliable)"
echo "3. Railway (easiest, auto-deploy from GitHub)"
echo "4. Fly.io (global edge deployment)"
echo ""
read -p "Enter choice (1-4): " PLATFORM

case $PLATFORM in
    1)
        echo -e "${GREEN}Deploying to Paperspace Gradient...${NC}"

        # Check if gradient CLI is installed
        if ! command -v gradient &> /dev/null; then
            echo -e "${YELLOW}Installing Paperspace Gradient CLI...${NC}"
            npm install -g @paperspace/gradient-cli

            echo ""
            echo "Please authenticate:"
            echo "1. Get API key from: https://console.paperspace.com/account/user"
            echo "2. Run: gradient apiKey YOUR_KEY"
            exit 0
        fi

        # Create deployment spec
        cat > gradient-spec.json << 'EOF'
{
  "name": "crowelogic-pharma",
  "projectId": "YOUR_PROJECT_ID",
  "spec": {
    "image": "ollama/ollama:latest",
    "command": ["sh", "-c", "ollama serve & sleep 20 && ollama pull llama3.2:latest && curl -sL https://raw.githubusercontent.com/MichaelCrowe11/crowelogic-pharma-model/master/models/CroweLogicPharmaModelfile-practical -o /tmp/modelfile && ollama create CroweLogic-Pharma:latest -f /tmp/modelfile && echo 'Model ready!' && tail -f /dev/null"],
    "port": 11434,
    "resources": {
      "replicas": 1,
      "instanceType": "C5"
    }
  }
}
EOF

        echo ""
        echo -e "${YELLOW}Note: You need to update the projectId in gradient-spec.json${NC}"
        echo "Get your project ID from: gradient projects list"
        echo ""
        echo "Then run: gradient deployments create --optionsFile gradient-spec.json"
        ;;

    2)
        echo -e "${GREEN}Deploying to DigitalOcean...${NC}"

        # Check if doctl is installed
        if ! command -v doctl &> /dev/null; then
            echo -e "${RED}doctl CLI not found!${NC}"
            echo ""
            echo "Install with:"
            echo "  Windows: choco install doctl"
            echo "  Mac: brew install doctl"
            echo "  Linux: snap install doctl"
            echo ""
            echo "Then authenticate: doctl auth init"
            exit 1
        fi

        APP_NAME="crowelogic-pharma"
        REGION="nyc3"
        SIZE="s-2vcpu-4gb"  # $24/month

        echo "Creating droplet..."
        DROPLET_ID=$(doctl compute droplet create $APP_NAME \
            --region $REGION \
            --size $SIZE \
            --image docker-20-04 \
            --wait \
            --format ID \
            --no-header)

        echo -e "${GREEN}✅ Droplet created: $DROPLET_ID${NC}"

        # Get IP
        DROPLET_IP=$(doctl compute droplet get $DROPLET_ID --format PublicIPv4 --no-header)
        echo "IP: $DROPLET_IP"

        echo "Waiting for droplet to be ready..."
        sleep 30

        echo "Deploying model..."
        ssh -o StrictHostKeyChecking=no root@$DROPLET_IP << 'ENDSSH'
docker run -d \
  --name crowelogic-pharma \
  -p 11434:11434 \
  ollama/ollama:latest \
  sh -c "ollama serve & sleep 20 && ollama pull llama3.2:latest && curl -sL https://raw.githubusercontent.com/MichaelCrowe11/crowelogic-pharma-model/master/models/CroweLogicPharmaModelfile-practical -o /tmp/modelfile && ollama create CroweLogic-Pharma:latest -f /tmp/modelfile && tail -f /dev/null"
ENDSSH

        echo ""
        echo -e "${GREEN}✅ Deployed successfully!${NC}"
        echo ""
        echo "Endpoint: http://$DROPLET_IP:11434"
        echo ""
        echo "Test with:"
        echo "curl http://$DROPLET_IP:11434/api/generate -d '{\"model\":\"CroweLogic-Pharma:latest\",\"prompt\":\"What are hericenones?\"}'"
        ;;

    3)
        echo -e "${GREEN}Deploying to Railway...${NC}"

        # Check if railway CLI is installed
        if ! command -v railway &> /dev/null; then
            echo -e "${YELLOW}Installing Railway CLI...${NC}"
            npm install -g @railway/cli

            echo ""
            echo "Please authenticate:"
            echo "Run: railway login"
            exit 0
        fi

        # Create railway.json
        cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile.universal"
  },
  "deploy": {
    "startCommand": "/app/start.sh",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

        echo "Initializing Railway project..."
        railway init

        echo "Deploying..."
        railway up

        echo ""
        echo -e "${GREEN}✅ Deployed to Railway!${NC}"
        echo ""
        echo "Get your domain with: railway domain"
        ;;

    4)
        echo -e "${GREEN}Deploying to Fly.io...${NC}"

        # Check if flyctl is installed
        if ! command -v flyctl &> /dev/null; then
            echo -e "${YELLOW}Installing Fly.io CLI...${NC}"
            curl -L https://fly.io/install.sh | sh

            echo ""
            echo "Please authenticate:"
            echo "Run: flyctl auth login"
            exit 0
        fi

        # Create fly.toml
        cat > fly.toml << 'EOF'
app = "crowelogic-pharma"

[build]
  dockerfile = "Dockerfile.universal"

[env]
  OLLAMA_HOST = "0.0.0.0:11434"
  BASE_MODEL = "llama3.2:latest"

[[services]]
  internal_port = 11434
  protocol = "tcp"

  [[services.ports]]
    port = 11434
    handlers = ["http"]

[http_service]
  internal_port = 11434
  force_https = false
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  cpu_kind = "shared"
  cpus = 4
  memory_mb = 8192
EOF

        echo "Launching Fly.io app..."
        flyctl launch --no-deploy

        echo "Deploying..."
        flyctl deploy

        echo ""
        echo -e "${GREEN}✅ Deployed to Fly.io!${NC}"
        echo ""
        echo "Get status: flyctl status"
        echo "Get URL: flyctl info"
        ;;

    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"

#!/bin/bash

# CroweLogic-Pharma Pro (70b) Azure Deployment Script
# Deploys a high-performance pharmaceutical AI with llama3.1:70b

set -e

# Ensure we operate from the repository root regardless of invocation path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Support optional legacy vs current deployment directories
if [ -d "azure_deployment" ]; then
  DEPLOY_DIR="azure_deployment"
elif [ -d "1211" ]; then
  DEPLOY_DIR="1211"
else
  echo "Error: Could not find deployment assets directory (expected azure_deployment/ or 1211/)." >&2
  exit 1
fi

CONFIG_FILE="${DEPLOY_DIR}/deployment_config_70b.json"

if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: Deployment config not found at $CONFIG_FILE" >&2
  exit 1
fi

# Allow caller to override build mode
BUILD_MODE="remote"  # default to remote ACR build to avoid local disk pressure
AUTO_SCALE_MEMORY=false
RESOURCE_GROUP_OVERRIDE=""
LOCATION_OVERRIDE=""
ACI_NAME_OVERRIDE=""
DNS_LABEL_OVERRIDE=""
CPU_OVERRIDE=""
MEMORY_OVERRIDE=""
SKIP_CONFIRMATION=false

usage() {
  cat <<'EOF'
Usage: ./deploy_70b.sh [options]

Options:
  --local-build              Build Docker image locally before push.
  --remote-build             Build image remotely in ACR (default).
  --resource-group <name>    Override resource group from config.
  --location <region>        Override Azure region/location.
  --aci-name <name>          Override container instance name.
  --dns-label <label>        Override public DNS label.
  --cpu <count>              Override requested CPU cores.
  --memory <gb>              Override memory in GB.
  --auto-scale-memory        Automatically recreate with 128GB if load fails.
  --yes                      Skip interactive confirmation prompt.
  --help, -h                 Show this help message.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --local-build)
      BUILD_MODE="local"
      shift
      ;;
    --remote-build)
      BUILD_MODE="remote"
      shift
      ;;
    --resource-group)
      RESOURCE_GROUP_OVERRIDE="$2"
      shift 2
      ;;
    --location)
      LOCATION_OVERRIDE="$2"
      shift 2
      ;;
    --aci-name)
      ACI_NAME_OVERRIDE="$2"
      shift 2
      ;;
    --dns-label)
      DNS_LABEL_OVERRIDE="$2"
      shift 2
      ;;
    --cpu)
      CPU_OVERRIDE="$2"
      shift 2
      ;;
    --memory)
      MEMORY_OVERRIDE="$2"
      shift 2
      ;;
    --auto-scale-memory)
      AUTO_SCALE_MEMORY=true
      shift
      ;;
    --yes)
      SKIP_CONFIRMATION=true
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done
echo "========================================="
echo "CroweLogic-Pharma Pro (70b) Deployment"
echo "========================================="
echo ""

RESOURCE_GROUP=${RESOURCE_GROUP_OVERRIDE:-$(jq -r '.resource_group' "$CONFIG_FILE")}
LOCATION=${LOCATION_OVERRIDE:-$(jq -r '.location' "$CONFIG_FILE")}
ACR_NAME=$(jq -r '.acr_name' "$CONFIG_FILE")
ACI_NAME=${ACI_NAME_OVERRIDE:-$(jq -r '.aci_name' "$CONFIG_FILE")}
DNS_LABEL=${DNS_LABEL_OVERRIDE:-$(jq -r '.dns_label' "$CONFIG_FILE")}
CPU=${CPU_OVERRIDE:-$(jq -r '.compute.cpu' "$CONFIG_FILE")}
MEMORY=${MEMORY_OVERRIDE:-$(jq -r '.compute.memory_gb' "$CONFIG_FILE")}

IMAGE_NAME="crowelogic-pharma-pro:latest"
FULL_IMAGE_REF="${ACR_NAME}.azurecr.io/${IMAGE_NAME}"

echo "Configuration:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Container: $ACI_NAME"
echo "  Resources: $CPU CPU, ${MEMORY}GB RAM"
echo "  Endpoint: http://${DNS_LABEL}.${LOCATION}.azurecontainer.io:11434"
echo ""

# Step 1: Build Docker image
if [[ "$BUILD_MODE" == "remote" ]]; then
  echo "Step 1: Building Docker image for 70b model (remote ACR build)..."
  az acr build \
    --registry "$ACR_NAME" \
    --image "$IMAGE_NAME" \
    --file "${DEPLOY_DIR}/Dockerfile-70b" \
    "$SCRIPT_DIR"
else
  echo "Step 1: Building Docker image for 70b model (local Docker build)..."
  docker build \
    -f "${DEPLOY_DIR}/Dockerfile-70b" \
    -t "$FULL_IMAGE_REF" \
    "$SCRIPT_DIR"

  echo ""
  echo "Step 2: Pushing image to Azure Container Registry..."
  az acr login --name "$ACR_NAME"
  docker push "$FULL_IMAGE_REF"
  echo ""
fi

echo ""

DEPLOY_STEP_LABEL="Step 2"
if [[ "$BUILD_MODE" == "local" ]]; then
  DEPLOY_STEP_LABEL="Step 3"
fi

echo "${DEPLOY_STEP_LABEL}: Deploying to Azure Container Instances..."
echo "⚠️  This will provision:"
echo "    - ${CPU} CPU cores"
echo "    - ${MEMORY}GB RAM"
echo ""

if [[ "$SKIP_CONFIRMATION" == false ]]; then
  read -p "Continue with deployment? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      echo "Deployment cancelled."
      exit 1
  fi
else
  echo "Auto-approved via --yes."
fi

# Get ACR credentials
ACR_PASSWORD=$(az acr credential show --name "$ACR_NAME" --query "passwords[0].value" --output tsv)

# Create container instance
az container create \
  --resource-group "$RESOURCE_GROUP" \
  --name "$ACI_NAME" \
  --image "$FULL_IMAGE_REF" \
  --registry-login-server "${ACR_NAME}.azurecr.io" \
  --registry-username "$ACR_NAME" \
  --registry-password "$ACR_PASSWORD" \
  --dns-name-label "$DNS_LABEL" \
  --cpu "$CPU" \
  --memory "$MEMORY" \
  --ports 11434 8000 \
  --ip-address Public \
  --os-type Linux \
  --location "$LOCATION" \
  --restart-policy Always \
  --environment-variables \
    OLLAMA_HOST=0.0.0.0:11434 \
    OLLAMA_MAX_LOADED_MODELS=1 \
    OLLAMA_NUM_PARALLEL=1

echo ""
echo "========================================="
echo "✅ Deployment Complete!"
echo "========================================="
echo ""
echo "Container is starting up..."
echo "The 70b model will be downloaded on first startup (15-20 minutes)"
echo ""
echo "Endpoint: http://${DNS_LABEL}.${LOCATION}.azurecontainer.io:11434"
echo "Model: CroweLogic-Pharma-Pro:latest"
echo ""
echo "Monitor logs with:"
echo "  az container logs --resource-group $RESOURCE_GROUP --name $ACI_NAME --follow"
echo ""
echo "Test the model with:"
echo "  curl -X POST http://${DNS_LABEL}.${LOCATION}.azurecontainer.io:11434/api/generate \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"model\": \"CroweLogic-Pharma-Pro:latest\", \"prompt\": \"Test query\", \"stream\": false}'"
echo ""
echo "========================================="

# Post-deploy health check: probe the Ollama API for memory-related load failures and optionally scale memory
ENDPOINT="http://${DNS_LABEL}.${LOCATION}.azurecontainer.io:11434"
echo "Checking model status at $ENDPOINT..."
sleep 8
HEALTH_OUT=$(curl -s -X POST "$ENDPOINT/api/generate" -H "Content-Type: application/json" -d '{"model":"CroweLogic-Pharma-Pro:latest","prompt":"health check","stream":false}' || true)

if echo "$HEALTH_OUT" | grep -qiE "memory|required|requires more system memory|unable to load"; then
  echo "Detected model load error:"
  echo "$HEALTH_OUT"

  if [[ "$AUTO_SCALE_MEMORY" == "true" ]]; then
    echo "Auto-scale enabled: will attempt to recreate container with increased memory (128GB)."
    NEW_MEMORY=128
  else
    read -p "Model requires more memory. Recreate container with ${NEW_MEMORY:-128}GB memory? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      echo "Skipping auto-scale. You can recreate the container manually with higher memory or quantize the model." 
      exit 0
    fi
    NEW_MEMORY=128
  fi

  echo "Recreating container with ${NEW_MEMORY}GB memory..."
  az container delete --resource-group "$RESOURCE_GROUP" --name "$ACI_NAME" --yes || true

  # recreate with larger memory
  az container create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$ACI_NAME" \
    --image "$FULL_IMAGE_REF" \
    --registry-login-server "${ACR_NAME}.azurecr.io" \
    --registry-username "$ACR_NAME" \
    --registry-password "$ACR_PASSWORD" \
    --dns-name-label "$DNS_LABEL" \
    --cpu "$CPU" \
    --memory "$NEW_MEMORY" \
    --ports 11434 8000 \
    --ip-address Public \
    --os-type Linux \
    --location "$LOCATION" \
    --restart-policy Always \
    --environment-variables \
      OLLAMA_HOST=0.0.0.0:11434 \
      OLLAMA_MAX_LOADED_MODELS=1 \
      OLLAMA_NUM_PARALLEL=1

  echo "Waiting 20s for container to start and attempt model load..."
  sleep 20
  SECOND_OUT=$(curl -s -X POST "$ENDPOINT/api/generate" -H "Content-Type: application/json" -d '{"model":"CroweLogic-Pharma-Pro:latest","prompt":"health check","stream":false}' || true)
  echo "Post-recreate check output:" 
  echo "$SECOND_OUT"
  if echo "$SECOND_OUT" | grep -qiE "memory|required|requires more system memory|unable to load"; then
    echo "Model still failing to load after increasing memory. Next recommended steps: quantize model, use a GPU-backed instance, or increase memory further." 
    exit 1
  else
    echo "Model loaded successfully after memory increase (or returned a non-memory error)." 
  fi
fi

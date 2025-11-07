#!/bin/bash

# Script to check Azure deployment status

echo "Checking CroweLogic-Pharma Azure Deployment Status..."
echo "=" * 70

# Check if ACI exists
echo -e "\n1. Checking Azure Container Instance..."
az container show \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci \
  --query "{Name:name,State:instanceView.state,IP:ipAddress.fqdn,Ports:ipAddress.ports}" \
  --output table 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "\n✓ Container Instance found"

    # Get endpoint
    ENDPOINT=$(az container show \
      --resource-group crowelogic-pharma-rg \
      --name crowelogic-pharma-aci \
      --query "ipAddress.fqdn" \
      --output tsv 2>/dev/null)

    if [ -n "$ENDPOINT" ]; then
        echo -e "\n✓ Endpoint URL: http://$ENDPOINT:11434"
        echo -e "✓ API URL: http://$ENDPOINT:11434/api/generate"

        echo -e "\n2. Testing connectivity..."
        timeout 5 curl -s "http://$ENDPOINT:11434" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "✓ Model is online and accessible!"
            echo -e "\nRun test script:"
            echo "  python test_deployment.py http://$ENDPOINT:11434"
        else
            echo "⚠ Container is running but model may still be initializing..."
            echo "  (Ollama needs to build the model on first startup)"
        fi
    fi
else
    echo "✗ Container Instance not found or not yet created"
    echo "  Deployment may still be in progress..."
fi

echo -e "\n3. Checking ACR images..."
az acr repository list \
  --name crowelogicpharma60881 \
  --output table 2>/dev/null

echo -e "\n4. Checking container logs (last 20 lines)..."
az container logs \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci \
  --tail 20 2>/dev/null || echo "No logs available yet"

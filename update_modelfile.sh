#!/bin/bash

# Script to update the Modelfile in the Azure container

echo "Copying corrected Modelfile to Azure container..."

# Read the local corrected Model file content
MODELFILE_CONTENT=$(cat /workspaces/crowelogic-pharma-model/models/CroweLogicPharmaModelfile)

# Use Azure CLI to update the file in the container
az container exec \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci \
  --exec-command "/bin/sh -c 'cat > /app/models/CroweLogicPharmaModelfile << '\''MODELFILE_EOF'\''
$MODELFILE_CONTENT
MODELFILE_EOF
'"

echo "Modelfile updated successfully!"
echo "Now recreating the CroweLogic-Pharma model..."

# Recreate the model
az container exec \
  --resource-group crowelogic-pharma-rg \
  --name crowelogic-pharma-aci \
  --exec-command "ollama create CroweLogic-Pharma:latest -f /app/models/CroweLogicPharmaModelfile"

echo "Model recreated!"

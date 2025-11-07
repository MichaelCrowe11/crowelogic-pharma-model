# CroweLogic-Pharma 70B GPU Deployment (AKS)

End-to-end plan for running the 70B CroweLogic-Pharma model on Azure Kubernetes Service (AKS) with GPU acceleration. This pathway avoids ACI capacity limits and provides the VRAM required for reliable 70B inference.

---

## 1. Prerequisites

- Azure CLI `>= 2.60`
- `kubectl` installed
- Subscription access to GPU SKUs (e.g., `Standard_NC24ads_A100_v4`)
- Existing Azure Container Registry (ACR), e.g., `crowelogicpharma60881`
- Quota for chosen GPU SKU in the target region (request increase if needed)

Set helpful variables:

```bash
export SUBSCRIPTION="366202b8-255e-4d8f-8a95-b43466cacb10"
export RESOURCE_GROUP="crowelogic-pharma-gpu-rg"
export LOCATION="eastus"
export ACR_NAME="crowelogicpharma60881"
export AKS_NAME="crowelogic-pharma-aks"
export GPU_POOL="gpu"
export NAMESPACE="pharma-ai"
export IMAGE_TAG="crowelogic-pharma-pro-gpu:latest"
```

---

## 2. Build and Push the GPU Image

Use the new `1211/Dockerfile-70b-gpu` base to build within ACR (no local GPU required):

```bash
az login --tenant <tenant-id>
az account set --subscription "$SUBSCRIPTION"

az acr build \
  --registry "$ACR_NAME" \
  --image "$IMAGE_TAG" \
  --file 1211/Dockerfile-70b-gpu \
  .
```

> The resulting image reference will be `"$ACR_NAME".azurecr.io/"$IMAGE_TAG"`.

---

## 3. Provision AKS with GPU Capacity

1. **Create resource group (if needed)**
   ```bash
   az group create --name "$RESOURCE_GROUP" --location "$LOCATION"
   ```

2. **Create AKS control plane with a small system node pool**
   ```bash
   az aks create \
     --resource-group "$RESOURCE_GROUP" \
     --name "$AKS_NAME" \
     --location "$LOCATION" \
     --node-count 1 \
     --node-vm-size Standard_D8ds_v5 \
     --enable-managed-identity \
     --attach-acr "$ACR_NAME"
   ```

3. **Add a dedicated GPU node pool** (tainting ensures only GPU workloads land here):
   ```bash
   az aks nodepool add \
     --resource-group "$RESOURCE_GROUP" \
     --cluster-name "$AKS_NAME" \
     --name "$GPU_POOL" \
     --node-count 1 \
     --node-vm-size Standard_NC24ads_A100_v4 \
     --node-taints sku=gpu:NoSchedule \
     --labels agentpool=gpu
   ```
   > Adjust `--node-count` or choose another SKU (e.g., `Standard_ND96asr_A100_v4`) if additional VRAM is required.

4. **Fetch cluster credentials**
   ```bash
   az aks get-credentials --resource-group "$RESOURCE_GROUP" --name "$AKS_NAME"
   ```

---

## 4. Deploy the GPU Workload

1. **Create namespace**
   ```bash
   kubectl create namespace "$NAMESPACE"
   ```

2. **Review and customize** `kubernetes/ollama-gpu-deployment.yaml`:
   - Update the `image:` field to `"$ACR_NAME".azurecr.io/"$IMAGE_TAG"`
   - Confirm `nodeSelector.agentpool` matches the GPU pool label (`gpu` above)
   - Adjust `tolerations` to match the taint (`sku=gpu:NoSchedule`)
   - Optionally replace `emptyDir` with an Azure Disk or File PVC for persistent model cache

3. **Apply manifests**
   ```bash
   kubectl apply -n "$NAMESPACE" -f kubernetes/ollama-gpu-deployment.yaml
   ```

4. **Watch rollout**
   ```bash
   kubectl rollout status deployment/crowelogic-pharma-gpu -n "$NAMESPACE"
   kubectl get pods -n "$NAMESPACE"
   ```

5. **Obtain external endpoint**
   ```bash
   kubectl get service crowelogic-pharma-gpu -n "$NAMESPACE"
   ```
   The `EXTERNAL-IP` exposes port `11434` (Ollama) and `8000` (REST API).

---

## 5. Post-Deployment Tasks

- **Model Warm-Up:** first start downloads `llama3.1:70b` (~40 GB). Monitor progress:
  ```bash
  kubectl logs -f deploy/crowelogic-pharma-gpu -n "$NAMESPACE"
  ```
- **Verification:**
  ```bash
  curl -X POST http://<EXTERNAL-IP>:11434/api/generate \
       -H 'Content-Type: application/json' \
       -d '{"model": "CroweLogic-Pharma-Pro:latest", "prompt": "GPU health check", "stream": false}'
  ```
- **GPU Utilization:**
  ```bash
  kubectl exec -n "$NAMESPACE" deploy/crowelogic-pharma-gpu -- nvidia-smi
  ```

---

## 6. Scaling and Reliability

- **Increase replicas** once VRAM/CPU allow (requires additional GPUs per pod)
- **Autoscale GPU pool**:
  ```bash
  az aks nodepool update \
    --resource-group "$RESOURCE_GROUP" \
    --cluster-name "$AKS_NAME" \
    --name "$GPU_POOL" \
    --enable-cluster-autoscaler \
    --min-count 1 \
    --max-count 3
  ```
- **Horizontal Pod Autoscaler** can trigger new pods if GPU pool scales out
- **Persistent storage**: swap `emptyDir` for Azure Disk/File to retain the model across pod restarts

---

## 7. Cost Controls

- Stop GPU node pool when idle:
  ```bash
  az aks nodepool scale --resource-group "$RESOURCE_GROUP" --cluster-name "$AKS_NAME" --name "$GPU_POOL" --node-count 0
  ```
- Use `--priority Spot` when adding the GPU pool to leverage spot pricing (availability varies)
- Track GPU costs via Azure Cost Management alerts

---

## 8. Rollback / Cleanup

```bash
kubectl delete namespace "$NAMESPACE"
az aks nodepool delete --resource-group "$RESOURCE_GROUP" --cluster-name "$AKS_NAME" --name "$GPU_POOL"
az aks delete --resource-group "$RESOURCE_GROUP" --name "$AKS_NAME" --yes
```

Keep the GPU image in ACR for future redeployments.

---

### Summary
- `1211/Dockerfile-70b-gpu` builds a GPU-compatible Ollama image
- `kubernetes/ollama-gpu-deployment.yaml` runs the workload on AKS GPU nodes
- `DEPLOYMENT_GPU_AKS.md` (this file) documents the step-by-step path

This approach delivers consistent GPU capacity, bypassing ACI limitations and enabling reliable 70B inference.

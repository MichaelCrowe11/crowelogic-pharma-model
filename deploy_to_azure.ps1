# CroweLogic-Pharma Azure Deployment Script
# Deploys to Azure Container Instance

param(
    [string]$ResourceGroup = "crowelogic-pharma-rg",
    [string]$Location = "eastus",
    [string]$AcrName = "crowelogicpharmaacr",
    [string]$ContainerName = "crowelogic-pharma-api",
    [string]$DnsLabel = "crowelogic-pharma"
)

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "CroweLogic-Pharma Azure Deployment" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Azure CLI
Write-Host "[1/7] Checking Azure CLI..." -ForegroundColor Yellow
$azVersion = az version 2>&1 | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Azure CLI not found" -ForegroundColor Red
    Write-Host "Install from: https://aka.ms/installazurecliwindows" -ForegroundColor Yellow
    exit 1
}
Write-Host "  Azure CLI version: $($azVersion.'azure-cli')" -ForegroundColor Green

# Step 2: Check login status
Write-Host ""
Write-Host "[2/7] Checking Azure login..." -ForegroundColor Yellow
$account = az account show 2>&1 | ConvertFrom-Json
if ($LASTEXITCODE -ne 0) {
    Write-Host "  Logging in..." -ForegroundColor Yellow
    az login
    $account = az account show | ConvertFrom-Json
}
Write-Host "  Logged in as: $($account.user.name)" -ForegroundColor Green
Write-Host "  Subscription: $($account.name)" -ForegroundColor Green

# Step 3: Create resource group
Write-Host ""
Write-Host "[3/7] Creating resource group: $ResourceGroup" -ForegroundColor Yellow
az group create --name $ResourceGroup --location $Location --output table

# Step 4: Create Azure Container Registry
Write-Host ""
Write-Host "[4/7] Creating Azure Container Registry: $AcrName" -ForegroundColor Yellow
az acr create `
    --resource-group $ResourceGroup `
    --name $AcrName `
    --sku Standard `
    --admin-enabled true `
    --location $Location `
    --output table

if ($LASTEXITCODE -ne 0) {
    Write-Host "  ACR creation failed (may already exist)" -ForegroundColor Yellow
}

# Step 5: Build and push Docker image
Write-Host ""
Write-Host "[5/7] Building and pushing Docker image..." -ForegroundColor Yellow
Write-Host "  This may take 10-15 minutes..." -ForegroundColor Gray

# Login to ACR
az acr login --name $AcrName

# Build using ACR Tasks (faster, uses cloud resources)
$imageName = "$AcrName.azurecr.io/crowelogic-pharma:latest"
Write-Host "  Building image: $imageName" -ForegroundColor Gray

az acr build `
    --registry $AcrName `
    --image crowelogic-pharma:latest `
    --file azure_deployment/Dockerfile `
    . `
    --platform linux

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host "  Image built and pushed successfully!" -ForegroundColor Green

# Step 6: Get ACR credentials
Write-Host ""
Write-Host "[6/7] Getting ACR credentials..." -ForegroundColor Yellow
$acrServer = az acr show --name $AcrName --query loginServer -o tsv
$acrUser = az acr credential show --name $AcrName --query username -o tsv
$acrPassword = az acr credential show --name $AcrName --query "passwords[0].value" -o tsv

# Step 7: Deploy to Azure Container Instance
Write-Host ""
Write-Host "[7/7] Deploying to Azure Container Instance..." -ForegroundColor Yellow
Write-Host "  Container name: $ContainerName" -ForegroundColor Gray
Write-Host "  DNS label: $DnsLabel" -ForegroundColor Gray
Write-Host "  Resources: 4 CPU, 16GB RAM" -ForegroundColor Gray

az container create `
    --resource-group $ResourceGroup `
    --name $ContainerName `
    --image $imageName `
    --cpu 4 `
    --memory 16 `
    --registry-login-server $acrServer `
    --registry-username $acrUser `
    --registry-password $acrPassword `
    --dns-name-label $DnsLabel `
    --ports 8000 11434 `
    --environment-variables OLLAMA_HOST=0.0.0.0 `
    --output json | ConvertFrom-Json | Out-File -FilePath "deployment_result.json"

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Container deployment failed" -ForegroundColor Red
    exit 1
}

# Get deployment details
$containerInfo = az container show `
    --resource-group $ResourceGroup `
    --name $ContainerName `
    --output json | ConvertFrom-Json

$fqdn = $containerInfo.ipAddress.fqdn
$ip = $containerInfo.ipAddress.ip

# Wait for container to start
Write-Host ""
Write-Host "Waiting for container to start (this may take 2-3 minutes)..." -ForegroundColor Yellow
Start-Sleep -Seconds 60

# Check health
Write-Host ""
Write-Host "Checking service health..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0
$ready = $false

while ($attempt -lt $maxAttempts -and !$ready) {
    $attempt++
    Write-Host "  Attempt $attempt/$maxAttempts..." -ForegroundColor Gray

    try {
        $response = Invoke-WebRequest -Uri "http://$($fqdn):8000/health" -TimeoutSec 5 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            $ready = $true
            Write-Host "  Service is ready!" -ForegroundColor Green
        }
    } catch {
        Start-Sleep -Seconds 10
    }
}

# Display results
Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "API Endpoints:" -ForegroundColor Cyan
Write-Host "  Health:        http://$($fqdn):8000/health" -ForegroundColor White
Write-Host "  Documentation: http://$($fqdn):8000/docs" -ForegroundColor White
Write-Host "  Query API:     http://$($fqdn):8000/api/query" -ForegroundColor White
Write-Host "  Ollama:        http://$($fqdn):11434" -ForegroundColor White
Write-Host ""
Write-Host "Container Info:" -ForegroundColor Cyan
Write-Host "  FQDN:          $fqdn" -ForegroundColor White
Write-Host "  IP Address:    $ip" -ForegroundColor White
Write-Host "  Resource Group: $ResourceGroup" -ForegroundColor White
Write-Host ""
Write-Host "Test the API:" -ForegroundColor Cyan
Write-Host '  Invoke-WebRequest -Uri "http://'$fqdn':8000/api/query" -Method POST -ContentType "application/json" -Body ''{"query": "What are hericenones?"}''' -ForegroundColor White
Write-Host ""
Write-Host "View logs:" -ForegroundColor Cyan
Write-Host "  az container logs --resource-group $ResourceGroup --name $ContainerName" -ForegroundColor White
Write-Host ""

# Save deployment info
$deploymentInfo = @{
    fqdn = $fqdn
    ip = $ip
    apiEndpoint = "http://$($fqdn):8000"
    docsUrl = "http://$($fqdn):8000/docs"
    healthUrl = "http://$($fqdn):8000/health"
    ollamaUrl = "http://$($fqdn):11434"
    containerName = $ContainerName
    resourceGroup = $ResourceGroup
    deploymentTime = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
} | ConvertTo-Json

Set-Content -Path "azure_deployment_info.json" -Value $deploymentInfo

Write-Host "Deployment info saved to: azure_deployment_info.json" -ForegroundColor Yellow
Write-Host ""
Write-Host "[SUCCESS] CroweLogic-Pharma deployed to Azure!" -ForegroundColor Green

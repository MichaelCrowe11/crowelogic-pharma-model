# RunPod Deployment - Quick Start

**Generate 5M examples in 18-24 hours for ~$4-5**

## Step 1: Create RunPod Account

1. Go to https://www.runpod.io/
2. Sign up with email or GitHub
3. Add $10 credits (minimum)

## Step 2: Deploy Pod

1. Click "Deploy" → "Pods"
2. Select Template: **"RunPod Pytorch"** or **"Ubuntu"**
3. Configure:
   - **GPU Type:** Select **"CPU"** (cheapest) or **"RTX A4000"** if available
   - **vCPU:** 16-32 cores
   - **RAM:** 32GB minimum
   - **Container Disk:** 50GB
   - **Volume Disk:** 100GB
4. Click "Deploy"

## Step 3: Connect via SSH

From RunPod dashboard, get your connection details:

```bash
ssh root@YOUR_POD_IP -p YOUR_SSH_PORT
```

## Step 4: Setup and Run

```bash
# Download and run setup
wget https://raw.githubusercontent.com/MichaelCrowe11/crowelogic-pharma-model/main/runpod_deployment/setup.sh
chmod +x setup.sh
./setup.sh

# Start generation (5M examples)
cd crowelogic-pharma-model
nohup python3 generate_10m_optimized.py --target 5000000 --output-dir generated_data/massive > generation.out 2>&1 &

# Monitor progress
tail -f generation.out
```

## Step 5: Download Results (after 18-24 hours)

```bash
# On RunPod, compress results
cd crowelogic-pharma-model/generated_data/massive
tar -czf massive_5m.tar.gz massive_10m*.jsonl

# From your Mac, download
scp -P YOUR_SSH_PORT root@YOUR_POD_IP:/workspace/crowelogic-pharma-model/generated_data/massive/massive_5m.tar.gz ./
```

## Step 6: Terminate Pod ⚠️

**IMPORTANT:** Terminate the pod when done to stop charges!

1. Go to RunPod console
2. Find your pod
3. Click "Terminate"

---

## Expected Output

- **Time:** 18-24 hours
- **Examples:** 5,000,000
- **File Size:** ~5-8GB
- **Cost:** ~$4-5

---

## Monitor Progress Remotely

```bash
# Check from your Mac
ssh root@YOUR_POD_IP -p YOUR_SSH_PORT 'tail -20 /workspace/crowelogic-pharma-model/generation.out'
```

---

## Cost Breakdown

**16-core CPU Pod:** $0.20/hour × 20 hours = **$4**
**32-core CPU Pod:** $0.30/hour × 18 hours = **$5.40**

---

**You're ready!** Go to https://www.runpod.io/ and deploy your pod!

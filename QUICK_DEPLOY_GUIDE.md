# 🚀 CroweLogic-Pharma Quick Deployment Guide

Choose your platform based on your needs:

## 🏆 Recommended: RunPod (Fastest & Easiest)

**Why RunPod:**
- ✅ Deploy in 2 minutes
- ✅ GPU from $0.20/hr
- ✅ Pre-built Ollama templates
- ✅ Pay-per-second billing
- ✅ No credit card for $5 trial

### RunPod Deployment (2 Minutes)

1. **Go to RunPod**: https://runpod.io
2. **Sign up** (Get $5 free credit)
3. **Deploy:**
   - Click "Deploy" → "Pods"
   - Select "Ollama" from Community templates
   - Choose GPU: RTX 4000 (~$0.20/hr) or A4000 (~$0.30/hr)
   - Click "Deploy"
4. **Access:**
   - Copy the endpoint URL
   - Use HTTP endpoint (port 11434)

5. **Configure Model:**
```bash
# SSH into pod or use web terminal
ollama pull llama3.2:latest

# Clone your repo
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Create model
ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile-practical
```

**Cost:** ~$15/month (if running 24/7 on RTX 4000)

---

## 💧 DigitalOcean (Simple & Reliable)

**Why DigitalOcean:**
- ✅ Very simple setup
- ✅ Predictable pricing
- ✅ Great documentation
- ✅ Easy scaling

### Prerequisites
```bash
# Install doctl
# Windows: choco install doctl
# Mac: brew install doctl
# Linux: snap install doctl

# Authenticate
doctl auth init
```

### Deploy
```bash
cd crowelogic-pharma-model
chmod +x deploy_digitalocean.sh
./deploy_digitalocean.sh
```

**Cost:** ~$48/month (4 CPU, 8GB RAM droplet)

---

## 🎨 Paperspace (GPU Power)

**Why Paperspace:**
- ✅ Free GPU in Gradient Notebooks
- ✅ Great for experimentation
- ✅ ML-optimized infrastructure

### Option 1: Gradient Notebook (FREE GPU!)

1. **Go to**: https://console.paperspace.com/gradient
2. **Create Notebook**:
   - Runtime: PyTorch
   - Machine: Free-GPU or P4000
   - Auto-shutdown: 6 hours
3. **Run Setup:**
```bash
# Upload and run paperspace_notebook_setup.py
python paperspace_notebook_setup.py
```

### Option 2: Gradient Deployment

```bash
# Install Paperspace CLI
npm install -g paperspace-node

# Authenticate
paperspace login

# Deploy
cd crowelogic-pharma-model
chmod +x deploy_paperspace.sh
./deploy_paperspace.sh
```

**Cost:**
- Notebooks: FREE (with auto-shutdown)
- Deployment: ~$50/month (CPU) or ~$367/month (GPU P4000)

---

## 🆚 Platform Comparison

| Feature | RunPod | DigitalOcean | Paperspace |
|---------|--------|--------------|------------|
| **Ease of Setup** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **GPU Support** | ✅ Excellent | ❌ No | ✅ Good |
| **Cost (CPU)** | ~$15/mo | ~$48/mo | ~$50/mo |
| **Cost (GPU)** | ~$144/mo | N/A | ~$367/mo |
| **Free Tier** | $5 credit | $200 credit | Free GPU notebooks |
| **Best For** | ML workloads | General apps | Experimentation |

---

## 🎯 My Recommendation

1. **Start with RunPod** (fastest, cheapest for GPU)
2. **Test with Paperspace Free GPU** (no risk)
3. **Production: DigitalOcean** (reliable, predictable)

---

## 🧪 Testing Your Deployment

Once deployed, test with:

```bash
# Replace YOUR_ENDPOINT with your actual endpoint
curl -X POST http://YOUR_ENDPOINT:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "CroweLogic-Pharma:latest",
    "prompt": "What are the neuroprotective mechanisms of hericenones from Lion'\''s Mane mushroom?",
    "stream": false
  }'
```

---

## 📊 Expected Performance

| Model Size | GPU Needed | Response Time | Cost/Month |
|------------|------------|---------------|------------|
| 3B (llama3.2) | No | 2-5 seconds | $15-50 |
| 13B | Optional | 5-10 seconds | $50-150 |
| 33B | Yes | 8-15 seconds | $150-250 |
| 70B | Yes (8GB+) | 15-30 seconds | $300-500 |

---

## 🆘 Need Help?

1. Check deployment logs
2. Verify Ollama is running: `curl http://endpoint:11434`
3. List models: `ollama list`
4. Test base model first: `ollama run llama3.2`

---

**Questions?** Open an issue on GitHub or check the docs in each deployment script.

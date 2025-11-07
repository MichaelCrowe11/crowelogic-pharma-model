# 🚀 Deploy CroweLogic-Pharma RIGHT NOW

Choose your deployment method (from easiest to most advanced):

---

## 🏆 Option 1: RunPod (RECOMMENDED - 2 Minutes)

**Fastest and easiest GPU deployment**

### Step-by-step:

1. **Sign up**: https://runpod.io (get $5 free credit)

2. **Deploy Ollama Template**:
   - Click "Deploy" → "Pods"
   - Search for "Ollama" in templates
   - Select GPU: RTX 4000 ($0.20/hr)
   - Click "Deploy Pod"

3. **Setup your model** (via web terminal or SSH):
```bash
# Clone repository
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Pull base model
ollama pull llama3.2:latest

# Create your model
ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile-practical

# Test it
ollama run CroweLogic-Pharma:latest "What are the therapeutic benefits of hericenones?"
```

**Done! Your endpoint is ready at the URL shown in RunPod dashboard.**

**Cost**: ~$15/month (if running 24/7) or pay-per-second when you use it

---

## ⚡ Option 2: Docker Compose (Works Anywhere - 5 Minutes)

**Deploy to ANY cloud provider with Docker**

### Step-by-step:

1. **Get a server** (choose one):
   - DigitalOcean: $48/month (4 CPU, 8GB RAM)
   - Linode: $36/month (4 CPU, 8GB RAM)
   - Hetzner: €16/month (4 CPU, 8GB RAM) - CHEAPEST!
   - AWS EC2: t3.large instance
   - Any VPS with Docker installed

2. **SSH into your server**:
```bash
ssh root@your-server-ip
```

3. **Clone and deploy**:
```bash
# Install Docker if not present
curl -fsSL https://get.docker.com | sh

# Clone repository
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Deploy!
docker-compose -f docker-compose.cloud.yml up -d

# Watch logs
docker-compose -f docker-compose.cloud.yml logs -f
```

4. **Wait 2-3 minutes** for the model to download and build

5. **Test it**:
```bash
curl -X POST http://your-server-ip:11434/api/generate \
  -d '{"model":"CroweLogic-Pharma:latest","prompt":"What are hericenones?","stream":false}'
```

**Done! Your API is live.**

---

## 🎨 Option 3: Paperspace Free GPU (Best for Testing - FREE!)

**Perfect for experimentation with no cost**

### Step-by-step:

1. **Sign up**: https://console.paperspace.com/gradient

2. **Create Notebook**:
   - Click "Notebooks" → "Create"
   - Runtime: PyTorch or TensorFlow
   - Machine: **Free-GPU** ⚡
   - Auto-shutdown: 6 hours

3. **Run in notebook terminal**:
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama
ollama serve &

sleep 10

# Clone repository
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Pull and create model
ollama pull llama3.2:latest
ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile-practical

# Test
ollama run CroweLogic-Pharma:latest "Explain the neuroprotective effects of Lion's Mane"
```

**Done! Use it for free as long as you want (auto-shuts down after 6 hours of inactivity)**

**Cost**: FREE! ✅

---

## 💧 Option 4: DigitalOcean App Platform (Managed - 10 Minutes)

**Fully managed, auto-scaling deployment**

### Step-by-step:

1. **Install CLI**:
```bash
# Windows
choco install doctl

# Mac
brew install doctl

# Linux
snap install doctl
```

2. **Authenticate**:
```bash
doctl auth init
```

3. **Deploy**:
```bash
cd crowelogic-pharma-model
chmod +x deploy_digitalocean.sh
./deploy_digitalocean.sh
```

4. **Follow prompts** and choose App Platform option

**Done! DigitalOcean manages everything for you**

**Cost**: ~$60/month (managed platform)

---

## 🎯 Quick Comparison

| Option | Setup Time | Cost | GPU | Best For |
|--------|------------|------|-----|----------|
| **RunPod** | 2 min | $15/mo | ✅ | Production, GPU needs |
| **Docker Compose** | 5 min | $16-48/mo | ❌ | Full control, any provider |
| **Paperspace** | 3 min | FREE | ✅ | Testing, experimentation |
| **DigitalOcean** | 10 min | $60/mo | ❌ | Managed, hands-off |

---

## 🧪 After Deployment - Test Your Model

```bash
# Basic health check
curl http://your-endpoint:11434

# List models
curl http://your-endpoint:11434/api/tags

# Generate response
curl -X POST http://your-endpoint:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "CroweLogic-Pharma:latest",
    "prompt": "What are the therapeutic applications of hericenones from Lion'\''s Mane mushroom for Alzheimer'\''s disease?",
    "stream": false
  }'
```

---

## 🆘 Troubleshooting

### Model not found?
```bash
ollama list  # Check if model exists
ollama pull llama3.2:latest  # Pull base model
ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile-practical
```

### Ollama not responding?
```bash
# Check if running
curl http://localhost:11434

# Restart Ollama
pkill ollama
ollama serve &
```

### Out of memory?
- Use smaller base model: `llama3.2:latest` (3B) instead of larger models
- Increase server RAM (upgrade to 16GB)

---

## 📊 What You Get

Once deployed, you have a full pharmaceutical AI API with:

- ✅ 300+ training examples (mushroom cultivation + pharma knowledge)
- ✅ ChEMBL drug target integration
- ✅ SMILES molecule analysis
- ✅ Medicinal chemistry expertise
- ✅ Clinical trial design guidance
- ✅ ADME-Tox prediction capabilities
- ✅ Regulatory compliance knowledge

---

## 🎉 Next Steps After Deployment

1. **Build a web interface** (React + your API)
2. **Create API documentation** (Swagger/OpenAPI)
3. **Set up monitoring** (track usage, performance)
4. **Add authentication** (API keys, rate limiting)
5. **Scale up** (larger models, more resources)

---

**Questions?** Check the full guides:
- `QUICK_DEPLOY_GUIDE.md` - Detailed platform comparison
- `deploy_digitalocean.sh` - DigitalOcean script
- `deploy_paperspace.sh` - Paperspace script
- `deploy_runpod.py` - RunPod Python script

**Ready to deploy?** Pick an option above and let's go! 🚀

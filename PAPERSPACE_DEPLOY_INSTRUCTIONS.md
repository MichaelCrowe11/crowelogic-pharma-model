# 🚀 Deploy CroweLogic-Pharma on Paperspace Gradient (RIGHT NOW!)

Since you have Paperspace Gradient open, here's the fastest way to deploy:

## 🎯 Option 1: Gradient Notebook (EASIEST - FREE GPU!)

**This takes 2 minutes and is completely FREE**

### Step-by-Step:

1. **Create a Notebook**:
   - Click "Notebooks" in the left sidebar
   - Click "Create" button
   - Select **Runtime**: PyTorch or TensorFlow
   - Select **Machine**: **Free-GPU** (or Free-P5000 if available)
   - Click "Start Notebook"

2. **Wait for notebook to start** (30-60 seconds)

3. **Open Terminal** (in the notebook interface)

4. **Copy-paste these commands**:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama in background
nohup ollama serve > ollama.log 2>&1 &

# Wait for it to start
sleep 15

# Clone your repository
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Pull base model (use GPU-optimized one if available)
ollama pull llama3.2:latest

# Create your CroweLogic-Pharma model
ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile-practical

# Test it!
ollama run CroweLogic-Pharma:latest "What are the neuroprotective mechanisms of hericenones from Lion's Mane mushroom?"
```

**That's it! You now have CroweLogic-Pharma running on FREE GPU!** 🎉

---

## 🚀 Option 2: Gradient Deployment (For Production)

**If you want a persistent API endpoint**

### Step 1: Prepare Docker Image

In a Gradient Notebook terminal:

```bash
# Clone repository
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Build Docker image
docker build -f Dockerfile.universal -t crowelogic-pharma:latest .

# Save image for deployment
docker save crowelogic-pharma:latest | gzip > crowelogic-pharma.tar.gz
```

### Step 2: Upload to Gradient Container Registry

```bash
# Tag for Gradient
docker tag crowelogic-pharma:latest gcr.io/paperspace/crowelogic-pharma:latest

# Push (you'll need to authenticate first)
docker push gcr.io/paperspace/crowelogic-pharma:latest
```

### Step 3: Create Deployment

1. Go to **Deployments** → **Create Deployment**

2. Fill in:
   - **Name**: crowelogic-pharma
   - **Container**: `gcr.io/paperspace/crowelogic-pharma:latest`
   - **Port**: 11434
   - **Machine Type**: C7 (CPU) or P4000 (GPU)
   - **Instance Count**: 1

3. Click **Deploy**

4. **Wait 3-5 minutes** for deployment to complete

5. **Get your endpoint** from the Deployments dashboard

---

## 🎨 Option 3: Use Pre-built Ollama Container (FASTEST!)

**Skip building, use existing Ollama image**

### In Gradient Notebook:

```bash
# Pull official Ollama image
docker pull ollama/ollama:latest

# Run it
docker run -d -p 11434:11434 --name crowelogic-pharma ollama/ollama:latest

# Wait for it to start
sleep 10

# Exec into container
docker exec -it crowelogic-pharma /bin/bash

# Inside container:
ollama pull llama3.2:latest

# Clone your configs (you'll need to do this manually or create a custom startup script)
cat > /tmp/Modelfile << 'EOF'
FROM llama3.2:latest

SYSTEM You are CroweLogic-Pharma, an expert AI assistant specializing in pharmaceutical research, drug discovery, and mycopharmacology. You have deep knowledge in medicinal chemistry, pharmacology, bioactive mushroom compounds, clinical trial design, and natural product drug discovery.

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
EOF

ollama create CroweLogic-Pharma:latest -f /tmp/Modelfile

# Test
ollama run CroweLogic-Pharma:latest "What are ganoderic acids?"

# Exit container
exit
```

**Your model is now running!**

Test from outside:
```bash
curl -X POST http://localhost:11434/api/generate \
  -d '{"model":"CroweLogic-Pharma:latest","prompt":"What are hericenones?","stream":false}'
```

---

## 📊 What Each Option Gives You

| Option | Speed | Cost | Persistence | Best For |
|--------|-------|------|-------------|----------|
| **Notebook** | 2 min | FREE | Until shutdown | Testing, development |
| **Deployment** | 10 min | ~$50/mo | 24/7 | Production API |
| **Pre-built** | 5 min | FREE | Until shutdown | Quick testing |

---

## 🧪 Testing Your Deployment

### Quick Test
```bash
curl http://your-endpoint:11434
```

### Full Test
```bash
curl -X POST http://your-endpoint:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "CroweLogic-Pharma:latest",
    "prompt": "Analyze the therapeutic potential of hericenones for Alzheimer'\''s disease, including mechanisms of action, clinical evidence, and future research directions.",
    "stream": false
  }'
```

### Python Client
```python
import requests

endpoint = "http://your-endpoint:11434"

response = requests.post(
    f"{endpoint}/api/generate",
    json={
        "model": "CroweLogic-Pharma:latest",
        "prompt": "What are the key bioactive compounds in Lion's Mane mushroom?",
        "stream": False
    }
)

print(response.json()["response"])
```

---

## 💡 Pro Tips

1. **Use Free GPU Notebook** for development and testing
2. **Upgrade to Deployment** when you need 24/7 availability
3. **Use auto-shutdown** on notebooks to avoid charges (set to 6 hours)
4. **Monitor costs** in the Gradient dashboard

---

## 🎯 Recommended: Start with Notebook

**Best approach right now:**

1. Create Free-GPU Notebook (2 minutes)
2. Run the setup commands above
3. Test your model thoroughly
4. When satisfied, create a Deployment for production

This way you can **test for FREE** before committing to a paid deployment!

---

## 🚨 Quick Start Command (Copy-Paste)

For Gradient Notebook terminal:

```bash
curl -fsSL https://ollama.com/install.sh | sh && \
nohup ollama serve > ollama.log 2>&1 & \
sleep 15 && \
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git && \
cd crowelogic-pharma-model && \
ollama pull llama3.2:latest && \
ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile-practical && \
echo "✅ CroweLogic-Pharma is ready!" && \
ollama run CroweLogic-Pharma:latest "Explain the therapeutic benefits of Lion's Mane mushroom"
```

**Just paste this and you're done!** 🎉

---

Need help? Check the Paperspace docs: https://docs.paperspace.com/gradient/

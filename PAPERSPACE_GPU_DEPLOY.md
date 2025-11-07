# 🎮 Deploy CroweLogic-Pharma to Paperspace with GPU

## 🏆 Best Options for GPU Deployment

---

## ⚡ Option 1: Gradient Notebook (FREE GPU!)

**Perfect for testing and development - NO COST!**

### Step-by-Step:

1. **Go to Paperspace**: https://console.paperspace.com/gradient/notebooks

2. **Create Notebook**:
   - Click **"Create"**
   - Runtime: **PyTorch** or **TensorFlow**
   - Machine: **Free-GPU** or **Free-P5000**
   - Auto-shutdown: **6 hours**
   - Click **"Start Notebook"**

3. **Wait for notebook to start** (~30 seconds)

4. **Open Terminal** (in Jupyter interface)

5. **Run this one-liner**:

```bash
curl -fsSL https://ollama.com/install.sh | sh && \
nohup ollama serve > ollama.log 2>&1 & \
sleep 20 && \
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git && \
cd crowelogic-pharma-model && \
ollama pull llama3.2:latest && \
ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile-practical && \
echo "✅ CroweLogic-Pharma ready!" && \
ollama run CroweLogic-Pharma:latest "What are the neuroprotective mechanisms of hericenones?"
```

**That's it! You now have a FREE GPU-powered pharmaceutical AI!**

### Use It:

```bash
# Interactive mode
ollama run CroweLogic-Pharma:latest

# API mode
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "CroweLogic-Pharma:latest",
    "prompt": "Analyze the therapeutic potential of Lion'\''s Mane for Alzheimer'\''s",
    "stream": false
  }'
```

**Cost**: **FREE!** ✨ (Auto-shuts down after 6 hours of inactivity)

---

## 🚀 Option 2: Gradient Deployment (Production with GPU)

**For 24/7 availability with GPU**

### Via Web UI (Easiest):

1. **Go to**: https://console.paperspace.com/gradient/deployments

2. **Click** "Create Deployment"

3. **Fill in the form**:

   **Machine**:
   - Select **P4000** ($0.51/hr, 8GB GPU) - Good for 3B-13B models
   - Or **P5000** ($0.78/hr, 16GB GPU) - Good for 33B models

   **Name**:
   ```
   crowelogic-pharma
   ```

   **Image**:
   ```
   ollama/ollama:latest
   ```

   **Command** (click to expand):
   ```bash
   sh -c "ollama serve & sleep 20 && ollama pull llama3.2:latest && curl -sL https://raw.githubusercontent.com/MichaelCrowe11/crowelogic-pharma-model/master/models/CroweLogicPharmaModelfile-practical -o /tmp/modelfile && ollama create CroweLogic-Pharma:latest -f /tmp/modelfile && echo 'Model ready!' && tail -f /dev/null"
   ```

   **Port**:
   ```
   11434
   ```

   **Replicas**:
   ```
   1
   ```

4. **Click "Deploy"**

5. **Wait 5-10 minutes** for:
   - Container to start
   - Model to download
   - GPU to initialize

6. **Get your endpoint** from Deployments dashboard

### Test It:

```bash
# Replace with your actual endpoint
ENDPOINT="https://your-deployment.paperspacegradient.com"

# Health check
curl $ENDPOINT:11434

# Test model
curl -X POST $ENDPOINT:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "CroweLogic-Pharma:latest",
    "prompt": "What are ganoderic acids and their anticancer mechanisms?",
    "stream": false
  }'
```

**Cost**:
- **P4000** (8GB): $0.51/hr = ~$367/month (24/7)
- **P5000** (16GB): $0.78/hr = ~$561/month (24/7)

💡 **Tip**: Stop deployment when not in use to save money!

---

## 🎯 GPU Selection Guide

| Model Size | GPU Needed | Paperspace Machine | Cost/Hour | Monthly (24/7) |
|------------|------------|-------------------|-----------|----------------|
| **3B** (llama3.2) | Optional | Free-GPU | FREE | FREE |
| **7B-13B** | 8GB+ | P4000 | $0.51 | $367 |
| **33B** | 16GB+ | P5000 | $0.78 | $561 |
| **70B** | 24GB+ | P6000 | $1.10 | $792 |

---

## 🆚 Notebook vs Deployment

| Feature | Notebook (Free-GPU) | Deployment (P4000) |
|---------|--------------------|--------------------|
| **Cost** | FREE ✅ | $367/month |
| **GPU** | Yes (Free-GPU) | Yes (8GB) |
| **Uptime** | Auto-shutdown 6hr | 24/7 |
| **Best For** | Testing, dev | Production API |
| **Setup Time** | 2 minutes | 5 minutes |

---

## 🔥 Quick Start (Copy-Paste)

### For Free Notebook:
```bash
# In Paperspace Notebook terminal:
curl -fsSL https://ollama.com/install.sh | sh && nohup ollama serve > ollama.log 2>&1 & sleep 20 && git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git && cd crowelogic-pharma-model && ollama pull llama3.2:latest && ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile-practical
```

### For Deployment:
Use the web UI with values above ↑

---

## 💡 Pro Tips

1. **Start with Free Notebook** - Test everything before paying
2. **Use auto-shutdown** - Notebooks auto-stop after 6 hours to save money
3. **Upgrade model** - Use `llama3.1:70b` on P6000 for better pharmaceutical knowledge
4. **Monitor GPU usage** - Check utilization in Paperspace dashboard
5. **Set spending limits** - Configure in Account settings

---

## 🎨 Using Larger Models with More GPU

For better pharmaceutical research capabilities:

### llama3.1:70b (Recommended for Production)

**In Notebook/Deployment, use P6000 (24GB GPU) and:**

```bash
ollama pull llama3.1:70b

# Update model to use 70B base
sed 's|llama3.2:latest|llama3.1:70b|' models/CroweLogicPharmaModelfile-practical > /tmp/Modelfile

ollama create CroweLogic-Pharma:70b -f /tmp/Modelfile
```

**Benefits**:
- Much better reasoning
- More accurate pharmaceutical knowledge
- Better citation and references
- Improved chemical analysis

**Cost**: P6000 @ $1.10/hr

---

## 🧪 Test Your Deployment

```python
import requests

endpoint = "http://localhost:11434"  # or your deployment URL

# Test pharmaceutical query
response = requests.post(
    f"{endpoint}/api/generate",
    json={
        "model": "CroweLogic-Pharma:latest",
        "prompt": """Analyze hericenone-C from Lion's Mane mushroom:
        1. Chemical structure and properties
        2. Mechanism of action for neuroprotection
        3. Clinical evidence for Alzheimer's disease
        4. Recommended dosages and safety profile
        5. Future research directions""",
        "stream": False
    }
)

print(response.json()["response"])
```

---

## 🆘 Troubleshooting

### GPU not detected?
```bash
# Check GPU availability
nvidia-smi

# Restart Ollama to use GPU
pkill ollama
ollama serve &
```

### Out of memory?
- Use smaller model (llama3.2:latest instead of 70b)
- Or upgrade to larger GPU (P5000/P6000)

### Slow responses?
- GPU is loading - first request always slower
- Check GPU utilization with `nvidia-smi`
- Consider larger GPU for bigger models

---

## 🎉 Ready to Deploy?

**Fastest**: Free Notebook (2 minutes, FREE)
**Best**: Deployment with P4000 (5 minutes, $367/month)

**My Recommendation**: Start with **Free Notebook** to test, then deploy to **P4000** when ready for production!

---

**Need help?** Check Paperspace docs: https://docs.paperspace.com/gradient/

# 🚀 Deploy CroweLogic-Pharma to Hugging Face (Private + FREE GPU!)

## ⭐ Why Hugging Face Spaces?

- ✅ **FREE GPU** (T4 GPU included!)
- ✅ **Private Space** (only you can access)
- ✅ **Beautiful Gradio UI** (ready to use)
- ✅ **Shareable** (can invite specific people)
- ✅ **No credit card needed**

---

## 🚀 Deploy in 3 Steps

### Step 1: Create Hugging Face Account

1. Go to: https://huggingface.co/join
2. Sign up (free)
3. Verify your email

### Step 2: Create Private Space

1. Go to: https://huggingface.co/new-space

2. Fill in:
   - **Owner**: Your username
   - **Space name**: `crowelogic-pharma`
   - **License**: MIT
   - **Select SDK**: **Docker**
   - **Space hardware**: **T4 small** (FREE GPU!)
   - **Visibility**: **🔒 Private** ← IMPORTANT!

3. Click **"Create Space"**

### Step 3: Upload Files

You have 2 options:

#### Option A: Via Web UI (Easiest)

1. In your new Space, click **"Files"** tab

2. Upload these files:
   ```
   app.py
   requirements_hf.txt
   Dockerfile.huggingface (rename to: Dockerfile)
   README_HF.md (rename to: README.md)
   ```

3. Create `models/` folder and upload:
   ```
   models/CroweLogicPharmaModelfile-practical
   ```

4. Wait 5-10 minutes for build to complete

#### Option B: Via Git (Advanced)

```bash
# In your crowelogic-pharma-model directory

# Install git-lfs
git lfs install

# Clone your new Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/crowelogic-pharma
cd crowelogic-pharma

# Copy files
cp ../app.py .
cp ../requirements_hf.txt requirements.txt
cp ../Dockerfile.huggingface Dockerfile
cp ../README_HF.md README.md
cp -r ../models .

# Commit and push
git add .
git commit -m "Initial deployment of CroweLogic-Pharma"
git push
```

---

## 🎨 Your Space Will Look Like This:

```
┌─────────────────────────────────────────┐
│  🍄 CroweLogic-Pharma AI                │
│  Pharmaceutical Research Assistant       │
├─────────────────────────────────────────┤
│                                         │
│  [Ask CroweLogic-Pharma]               │
│  ┌─────────────────────────────────┐   │
│  │ Your question here...           │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Temperature: ──●────── 0.7            │
│  Max Length:  ──●────── 2000           │
│                                         │
│  [🔬 Analyze]                          │
│                                         │
│  Response:                             │
│  ┌─────────────────────────────────┐   │
│  │ AI response appears here...     │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Example Queries:                      │
│  • Neuroprotective mechanisms...       │
│  • Clinical trial design...            │
└─────────────────────────────────────────┘
```

---

## 🔒 Privacy Settings

Your Space is **PRIVATE** by default with `private: true` in README.md

### Who Can Access:

- ✅ **Only you** (the owner)
- ✅ **People you invite** (via Share settings)
- ❌ **NOT public** (hidden from search/explore)

### To Invite Others:

1. Go to your Space settings
2. Click **"Sharing"**
3. Add email addresses
4. They get private access link

---

## 💰 Cost

**COMPLETELY FREE!** ✨

- Free T4 GPU included
- No credit card required
- Unlimited inference
- Private hosting

**Note**: Space sleeps after 48 hours of inactivity (free tier). Just visit URL to wake it up!

---

## 🧪 Testing Your Deployment

Once deployed, your Space will be at:
```
https://huggingface.co/spaces/YOUR_USERNAME/crowelogic-pharma
```

Test queries:
- "What are the neuroprotective mechanisms of hericenones?"
- "Design a Phase II trial for Lion's Mane in Alzheimer's"
- "Analyze ganoderic acids for cancer treatment"

---

## ⚙️ Configuration Options

### Use Larger Model (Better Results)

Edit `Dockerfile.huggingface` and change:
```bash
ollama pull llama3.2:latest
```
to:
```bash
ollama pull llama3.1:70b  # Requires paid GPU (A10G or A100)
```

### Enable Paid GPU (Optional)

For larger models, upgrade Space hardware:
- **A10G Small**: $0.60/hr (24GB GPU)
- **A100 Large**: $3.15/hr (40GB GPU)

---

## 🎯 File Checklist

Make sure you upload these files:

```
crowelogic-pharma/
├── Dockerfile              (from Dockerfile.huggingface)
├── README.md               (from README_HF.md)
├── app.py                  (Gradio interface)
├── requirements.txt        (from requirements_hf.txt)
└── models/
    └── CroweLogicPharmaModelfile-practical
```

---

## 🔥 Quick Commands

### Create Space via CLI:

```bash
# Install Hugging Face CLI
pip install huggingface_hub[cli]

# Login
huggingface-cli login

# Create private Space
huggingface-cli space create crowelogic-pharma \
  --sdk docker \
  --private \
  --hardware t4-small
```

### Upload files:

```bash
cd crowelogic-pharma-model

# Upload all at once
huggingface-cli upload \
  YOUR_USERNAME/crowelogic-pharma \
  . \
  --repo-type space \
  --include "app.py" "Dockerfile.huggingface" "README_HF.md" "requirements_hf.txt" "models/*"
```

---

## 🆘 Troubleshooting

### Build failing?
- Check Dockerfile syntax
- Ensure all files are uploaded
- Check Space logs in "Logs" tab

### Out of memory?
- Use smaller model (llama3.2:latest)
- Or upgrade to A10G GPU

### Slow first load?
- First request always slow (pulling model)
- Subsequent requests fast
- Space sleeps after 48hr inactivity (free tier)

---

## 💡 Pro Tips

1. **Keep it private** - Your proprietary pharmaceutical AI!
2. **Use free T4 GPU** - Perfect for 3B-13B models
3. **Upgrade for larger models** - A10G for 33B-70B models
4. **Share selectively** - Invite collaborators only
5. **Monitor usage** - Check Space analytics

---

## 🎉 Ready to Deploy?

1. **Sign up**: https://huggingface.co/join
2. **Create Space**: https://huggingface.co/new-space
3. **Upload files**: Use web UI or CLI
4. **Wait 10 minutes**: For build to complete
5. **Access your private AI**: Only you can see it!

---

**Questions?**
- Hugging Face Docs: https://huggingface.co/docs/hub/spaces
- Discord: https://huggingface.co/join/discord

---

**Your pharmaceutical AI, private and powerful! 🍄**

# 🚀 Deploy CroweLogic-Pharma via CLI (READY TO RUN)

You have Railway and Fly.io installed! Here are your options:

---

## ⚡ Option 1: Railway (EASIEST - Recommended)

### Deploy in 3 commands:

```bash
cd crowelogic-pharma-model

# 1. Login to Railway
railway login

# 2. Initialize project (creates new Railway project)
railway init

# 3. Deploy!
railway up
```

**That's it!** Railway will:
- Build your Docker image
- Deploy it automatically
- Give you a public URL

### Get your URL:
```bash
railway domain
```

### Check logs:
```bash
railway logs
```

### Open in browser:
```bash
railway open
```

**Cost**: $5/month credit (free tier), then ~$10-20/month

---

## 🌐 Option 2: Fly.io (Global Edge)

### Deploy in 2 commands:

```bash
cd crowelogic-pharma-model

# 1. Authenticate (if not already)
flyctl auth login

# 2. Launch and deploy
flyctl launch --now
```

Answer the prompts:
- **App name**: crowelogic-pharma (or leave blank for random)
- **Region**: Choose closest to you
- **PostgreSQL**: No
- **Redis**: No

**That's it!** Fly will deploy automatically.

### Get status:
```bash
flyctl status
```

### View logs:
```bash
flyctl logs
```

### Get URL:
```bash
flyctl info
```

**Cost**: Free tier (3 shared CPUs, 256MB RAM), then ~$15-30/month for larger machines

---

## 🎯 Which Should You Use?

| Feature | Railway | Fly.io |
|---------|---------|---------|
| **Ease** | ⭐⭐⭐⭐⭐ Easiest | ⭐⭐⭐⭐ Very easy |
| **Speed** | ⭐⭐⭐⭐ Fast | ⭐⭐⭐⭐⭐ Fastest (edge) |
| **Free Tier** | $5 credit | 3 shared CPUs |
| **Cost** | ~$10-20/mo | ~$15-30/mo |
| **Best For** | Simple deployment | Global distribution |

**My recommendation**: Start with **Railway** (it's the easiest)

---

## 📝 Full Railway Deployment Script

Copy-paste this entire block:

```bash
cd crowelogic-pharma-model
railway login
railway init --name crowelogic-pharma
railway up
railway domain
echo "Deployment complete! Get your URL with: railway domain"
```

---

## 📝 Full Fly.io Deployment Script

Copy-paste this entire block:

```bash
cd crowelogic-pharma-model
flyctl auth login
flyctl launch --now --name crowelogic-pharma --region iad --vm-size shared-cpu-4x
flyctl status
echo "Deployment complete! Get your URL with: flyctl info"
```

---

## 🧪 After Deployment - Test It

Once deployed, test with:

```bash
# Replace YOUR_URL with actual URL
curl http://YOUR_URL:11434

# Test the model
curl -X POST http://YOUR_URL:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "CroweLogic-Pharma:latest",
    "prompt": "What are the neuroprotective benefits of hericenones?",
    "stream": false
  }'
```

---

## 🎉 Ready?

Pick one and run the commands!

**EASIEST**: Railway (3 commands)
**FASTEST**: Fly.io (2 commands)

# Deploy CroweLogic-Pharma-7B Model NOW

**Status**: ✅ Ready for immediate deployment
**Dataset**: 96,349 examples (86,714 train / 9,635 val)
**Target Model**: 7B parameter pharmaceutical AI
**Platform**: RunPod, Lambda Labs, or Google Colab
**Cost**: $5-15 total
**Time**: 2-4 hours

---

## 🚀 Quick Start (5 Minutes to Launch)

### Option A: RunPod (Recommended - Cheapest & Easiest)

**1. Sign up for RunPod**
- Go to https://www.runpod.io/
- Create account
- Add $10-20 credit

**2. Create Pod**
```
Template: RunPod Pytorch 2.1
GPU: RTX 4090 (24GB) - $0.34/hr
Storage: 50GB
```

**3. Upload Dataset**
```bash
# In RunPod terminal
cd /workspace
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Datasets are in GitHub (under 100MB, should be there)
ls -lh datasets/crowelogic_pharma_train.jsonl
ls -lh datasets/crowelogic_pharma_val.jsonl
```

**4. Start Training**
```bash
# Set environment variables
export WANDB_API_KEY="your-wandb-key"  # Get from wandb.ai (free account)
export HF_TOKEN="your-hf-token"        # Get from huggingface.co

# Launch training
python3 training/train_cloud_gpu.py \
  --model_name "mistralai/Mistral-7B-v0.1" \
  --train_data "datasets/crowelogic_pharma_train.jsonl" \
  --val_data "datasets/crowelogic_pharma_val.jsonl" \
  --output_dir "models/crowelogic-pharma-7b" \
  --num_epochs 3 \
  --batch_size 4 \
  --learning_rate 2e-4
```

**Cost**: ~$2-4 for complete training (6-12 hours on RTX 4090)

---

## Option B: Lambda Labs (Fast GPUs)

**1. Sign up**: https://lambdalabs.com/
**2. Launch Instance**:
```
GPU: 1x A100 (40GB) - $1.10/hr
Instance: PyTorch 2.0+
```

**3. Same setup as RunPod above**

**Cost**: ~$6-12 for training (5-10 hours on A100)

---

## Option C: Google Colab (Free Tier Possible)

**1. Open Colab**: https://colab.research.google.com/

**2. Connect to GPU**:
```python
# Check GPU
!nvidia-smi
```

**3. Clone and Setup**:
```bash
!git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git
%cd crowelogic-pharma-model

# Install dependencies
!pip install -q transformers datasets peft accelerate bitsandbytes wandb tqdm
```

**4. Train**:
```python
!python training/train_cloud_gpu.py \
  --model_name "mistralai/Mistral-7B-v0.1" \
  --train_data "datasets/crowelogic_pharma_train.jsonl" \
  --val_data "datasets/crowelogic_pharma_val.jsonl" \
  --output_dir "models/crowelogic-pharma-7b" \
  --num_epochs 2 \
  --batch_size 2
```

**Cost**: Free (with T4 GPU) or $10/month (Colab Pro with A100)

---

## 📊 What to Expect

### Training Progress

```
Epoch 1/3: 100%|██████████| 21679/21679 [2:15:34<00:00]
  Train Loss: 1.234
  Val Loss: 1.456
  Perplexity: 4.28

Epoch 2/3: 100%|██████████| 21679/21679 [2:15:34<00:00]
  Train Loss: 0.987
  Val Loss: 1.123
  Perplexity: 3.07

Epoch 3/3: 100%|██████████| 21679/21679 [2:15:34<00:00]
  Train Loss: 0.765
  Val Loss: 0.987
  Perplexity: 2.68

✓ Training complete!
✓ Model saved to: models/crowelogic-pharma-7b
```

### Timeline

- **RTX 4090**: 6-12 hours ($2-4)
- **A100**: 5-10 hours ($5-12)
- **T4 (Colab)**: 15-20 hours (Free)

### Expected Quality

- **MedQA Score**: 55-65% (vs GPT-4: 78%)
- **Pharmaceutical Knowledge**: Strong on drug properties, molecular analysis
- **Cost per Query**: $0.0005 (200x cheaper than GPT-4)

---

## 🎯 After Training

### Download Your Model

```bash
# From RunPod/Lambda
zip -r crowelogic-pharma-7b.zip models/crowelogic-pharma-7b/
# Download via RunPod web interface or scp
```

### Test Your Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./models/crowelogic-pharma-7b")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

# Test pharmaceutical question
question = "What is the mechanism of action of aspirin?"
inputs = tokenizer(question, return_tensors="pt")
outputs = model.generate(**inputs, max_length=200)
answer = tokenizer.decode(outputs[0])

print(answer)
# Expected: "Aspirin works by inhibiting COX-1 and COX-2 enzymes..."
```

### Deploy as API

```bash
# Use the included API (already in repo)
cd api
docker build -t crowelogic-pharma-api .
docker run -p 8000:8000 crowelogic-pharma-api

# Test
curl http://localhost:8000/query \
  -d '{"question": "What is the molecular weight of ibuprofen?"}'
```

---

## 📈 Monitoring Training

### Weights & Biases (Recommended)

1. Create free account: https://wandb.ai/
2. Get API key
3. Training will auto-log to W&B dashboard
4. View:
   - Loss curves
   - Learning rate schedule
   - GPU utilization
   - Sample predictions

### Local Logs

```bash
# Watch training progress
tail -f training.log

# Check GPU usage
watch nvidia-smi
```

---

## 🐛 Troubleshooting

### Out of Memory

```bash
# Reduce batch size
--batch_size 2  # or even 1

# Use gradient checkpointing (already enabled)
```

### Slow Training

```bash
# Use mixed precision (already enabled)
# Check GPU utilization
nvidia-smi

# Should see >90% GPU utilization
```

### Connection Drops

```bash
# Use tmux/screen to keep training running
tmux new -s training
python3 training/train_cloud_gpu.py ...
# Detach: Ctrl+B, then D
# Reattach: tmux attach -t training
```

---

## 💡 Pro Tips

1. **Start with 1 epoch** to validate pipeline (~2 hours)
2. **Use W&B** to track experiments
3. **Save checkpoints** every 1000 steps (already configured)
4. **Test on validation set** before full training
5. **Use tmux** to prevent disconnection issues

---

## 🎯 Next Steps After 7B Training

While your 7B model trains, you can:

1. **Continue building 10M infrastructure** (parallel development)
2. **Design evaluation benchmarks**
3. **Plan 13B/34B/70B scale-up**
4. **Set up deployment infrastructure**
5. **Explore CroweChain testnet**

---

## 📊 Cost Summary

| Platform | GPU | Time | Cost | Quality |
|----------|-----|------|------|---------|
| **RunPod RTX 4090** | 24GB | 8h | **$2.70** | Good |
| Lambda A100 | 40GB | 6h | $6.60 | Better |
| RunPod A100 | 80GB | 5h | $12.00 | Best |
| Colab Free | T4 | 18h | **$0** | Good |
| Colab Pro | A100 | 6h | $10/mo | Better |

**Recommended**: RunPod RTX 4090 ($2.70 total)

---

## 🚀 Deploy Command (Copy-Paste)

### Complete RunPod Setup

```bash
# 1. SSH into RunPod pod
# 2. Copy-paste this entire block:

cd /workspace && \
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git && \
cd crowelogic-pharma-model && \
pip install -q transformers datasets peft accelerate bitsandbytes wandb tqdm && \
export WANDB_API_KEY="your-key-here" && \
export HF_TOKEN="your-token-here" && \
nohup python3 training/train_cloud_gpu.py \
  --model_name "mistralai/Mistral-7B-v0.1" \
  --train_data "datasets/crowelogic_pharma_train.jsonl" \
  --val_data "datasets/crowelogic_pharma_val.jsonl" \
  --output_dir "models/crowelogic-pharma-7b" \
  --num_epochs 3 \
  --batch_size 4 \
  --learning_rate 2e-4 \
  > training.log 2>&1 &

# 3. Monitor progress:
tail -f training.log
```

---

## ✅ Success Checklist

- [ ] RunPod account created & funded ($10-20)
- [ ] Pod launched (RTX 4090 recommended)
- [ ] Repository cloned
- [ ] Training started
- [ ] W&B dashboard monitoring
- [ ] Estimated completion time noted

**Training will complete in 6-12 hours. Check back tomorrow for your trained model!**

---

*Your 7B model will be training while we build toward 10M examples and the 70B flagship model!* 🎯

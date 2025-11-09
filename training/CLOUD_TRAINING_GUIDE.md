# CroweLogic-Pharma Cloud Training Guide

Complete guide for training Mistral-7B with QLoRA on cloud GPU platforms.

## Dataset Summary

✅ **Generated 100,000 training examples**
- Training: 95,000 examples (95%)
- Validation: 5,000 examples (5%)
- Total size: ~33.6 MB
- Composition:
  - 75% Pharmaceutical knowledge (molecular properties, mechanisms, clinical)
  - 16% Crowe Logic architectural patterns
  - 7% Code implementations (TypeScript/Python)
  - 2% System design patterns

**Files:**
- `crowelogic_pharma_100k_train.jsonl`
- `crowelogic_pharma_100k_val.jsonl`
- `crowelogic_pharma_100k_full.jsonl`

## Why Cloud Training is Required

**Local M1 Mac Limitations:**
- ❌ 8GB RAM insufficient (Mistral-7B needs ~26GB even with optimizations)
- ❌ Training failed with "Invalid buffer size: 26.49 GiB" error
- ❌ Estimated 60-90 minutes per epoch (too slow)

**Cloud GPU Advantages:**
- ✅ 24-80GB VRAM (A100, A6000, H100)
- ✅ CUDA support for 4-bit quantization (QLoRA)
- ✅ 4-8 hours total training time
- ✅ Cost: $10-40 depending on platform

---

## Option 1: RunPod (Recommended - Easy Setup)

**Cost:** $0.39/hr (RTX 4090) to $1.89/hr (A100 80GB)

### Setup Steps:

1. **Create RunPod Account**
   ```
   Visit: https://www.runpod.io/
   Sign up with email/Google
   Add credits: $10-20 minimum
   ```

2. **Deploy GPU Pod**
   ```
   Templates → PyTorch 2.1
   GPU: RTX 4090 24GB or A100 40GB
   Container Disk: 50GB
   Volume Disk: 20GB (optional)
   ```

3. **Upload Datasets**
   ```bash
   # On your M1 Mac, zip datasets:
   cd ~
   zip -r crowelogic_datasets.zip crowelogic_pharma_100k_*.jsonl

   # Upload via RunPod web interface or:
   scp crowelogic_datasets.zip root@<pod-ip>:/workspace/

   # On pod, unzip:
   unzip /workspace/crowelogic_datasets.zip -d /workspace/
   ```

4. **Upload Training Script**
   ```bash
   scp ~/train_cloud_gpu.py root@<pod-ip>:/workspace/
   ```

5. **Install Dependencies**
   ```bash
   # SSH into pod (get SSH command from RunPod dashboard)
   ssh root@<pod-ip> -p <port>

   # Install packages
   pip install transformers datasets peft bitsandbytes accelerate trl wandb
   ```

6. **Start Training**
   ```bash
   cd /workspace
   python train_cloud_gpu.py
   ```

7. **Monitor Training**
   ```
   Watch logs in terminal
   Or use Weights & Biases (set USE_WANDB=True in script)
   ```

8. **Download Trained Model**
   ```bash
   # On pod, zip model:
   zip -r crowelogic-pharma-mistral-7b.zip /workspace/crowelogic-pharma-mistral-7b/

   # Download to M1 Mac:
   scp root@<pod-ip>:/workspace/crowelogic-pharma-mistral-7b.zip ~/
   ```

9. **Terminate Pod**
   ```
   Important: Stop pod immediately after downloading to avoid charges!
   RunPod → My Pods → Terminate
   ```

**Estimated Cost:** $5-15 total (4-8 hours × $0.39-1.89/hr)

---

## Option 2: Google Colab Pro

**Cost:** $10/month subscription (includes 100 compute units)

### Setup Steps:

1. **Subscribe to Colab Pro**
   ```
   Visit: https://colab.research.google.com/
   Upgrade to Colab Pro ($10/month)
   Get A100 GPU access
   ```

2. **Create New Notebook**
   ```python
   # Cell 1: Check GPU
   !nvidia-smi

   # Cell 2: Install dependencies
   !pip install transformers datasets peft bitsandbytes accelerate trl

   # Cell 3: Upload datasets
   from google.colab import files
   # Upload crowelogic_pharma_100k_train.jsonl
   # Upload crowelogic_pharma_100k_val.jsonl

   # Or mount Google Drive:
   from google.colab import drive
   drive.mount('/content/drive')
   ```

3. **Upload Training Script**
   ```python
   # Copy train_cloud_gpu.py content into notebook
   # Or upload file via Colab interface
   ```

4. **Modify Paths**
   ```python
   # In train_cloud_gpu.py, change:
   TRAIN_FILE = "/content/crowelogic_pharma_100k_train.jsonl"
   VAL_FILE = "/content/crowelogic_pharma_100k_val.jsonl"
   ```

5. **Run Training**
   ```python
   !python train_cloud_gpu.py
   ```

6. **Download Model**
   ```python
   # Zip and download
   !zip -r crowelogic_pharma_model.zip /content/crowelogic-pharma-mistral-7b
   from google.colab import files
   files.download('/content/crowelogic_pharma_model.zip')
   ```

**Pros:**
- Easy to use
- Jupyter notebook interface
- Good for experimentation

**Cons:**
- 12-hour session limit (training may disconnect)
- Need to reconnect and resume
- Slower than dedicated GPU pod

---

## Option 3: Lambda Labs

**Cost:** $1.10/hr (A100 40GB) to $1.99/hr (A100 80GB)

### Setup Steps:

1. **Create Account**
   ```
   Visit: https://lambdalabs.com/service/gpu-cloud
   Sign up and add payment method
   Minimum $25 credit
   ```

2. **Launch Instance**
   ```
   GPU Cloud → Launch Instance
   GPU: A100 (40GB or 80GB)
   Region: Choose closest to you
   SSH Key: Upload your public key
   ```

3. **Connect & Setup**
   ```bash
   ssh ubuntu@<instance-ip>

   # Install dependencies
   pip install transformers datasets peft bitsandbytes accelerate trl
   ```

4. **Upload Data & Script**
   ```bash
   # From M1 Mac:
   scp ~/crowelogic_pharma_100k_*.jsonl ubuntu@<instance-ip>:/home/ubuntu/
   scp ~/train_cloud_gpu.py ubuntu@<instance-ip>:/home/ubuntu/
   ```

5. **Update Paths**
   ```bash
   # Edit script on instance
   nano train_cloud_gpu.py

   # Change paths:
   TRAIN_FILE = "/home/ubuntu/crowelogic_pharma_100k_train.jsonl"
   VAL_FILE = "/home/ubuntu/crowelogic_pharma_100k_val.jsonl"
   ```

6. **Start Training**
   ```bash
   # Use screen to persist training if SSH disconnects
   screen -S training
   python train_cloud_gpu.py

   # Detach: Ctrl+A then D
   # Reattach: screen -r training
   ```

7. **Download Model**
   ```bash
   # From M1 Mac:
   scp -r ubuntu@<instance-ip>:/home/ubuntu/crowelogic-pharma-mistral-7b ~/
   ```

8. **Terminate Instance**
   ```
   Lambda Labs → Instances → Terminate
   ```

---

## Option 4: Modal (Code-First Platform)

**Cost:** $0.60-1.50/hr (GPU pricing)

Modal is a serverless platform with Python SDK. Great for reproducible training.

### Setup Steps:

1. **Install Modal**
   ```bash
   pip install modal
   modal token new  # Authenticate
   ```

2. **Create Modal Training Script**
   ```python
   # modal_train.py
   import modal

   stub = modal.Stub("crowelogic-pharma-training")

   @stub.function(
       gpu="A100",
       timeout=28800,  # 8 hours
       image=modal.Image.debian_slim().pip_install([
           "transformers", "datasets", "peft",
           "bitsandbytes", "accelerate", "trl"
       ])
   )
   def train():
       # Your training code here
       import train_cloud_gpu
       train_cloud_gpu.main()

   @stub.local_entrypoint()
   def main():
       train.remote()
   ```

3. **Deploy & Run**
   ```bash
   modal run modal_train.py
   ```

**Pros:**
- Automatic scaling
- Pay only for GPU time used
- Version control for training runs

**Cons:**
- Requires Python SDK knowledge
- More complex setup

---

## Training Configuration Summary

Current `train_cloud_gpu.py` settings:

```python
Model: Mistral-7B-v0.1
Method: QLoRA (4-bit quantization)

LoRA Parameters:
- Rank: 16
- Alpha: 32
- Dropout: 0.05
- Target modules: All attention + MLP layers

Training:
- Batch size: 4 per device
- Gradient accumulation: 4 (effective batch = 16)
- Learning rate: 2e-4
- Epochs: 3
- Max sequence length: 512

Dataset:
- Training: 95,000 examples
- Validation: 5,000 examples
```

**Expected Training Time:**
- RTX 4090: 6-8 hours
- A100 40GB: 4-6 hours
- A100 80GB: 3-5 hours

**Expected Results:**
- Final model size: ~16MB (LoRA adapters only)
- Full model with adapters: ~4GB
- Validation loss: Target < 1.0

---

## Post-Training: Model Integration

### 1. Convert to GGUF for Ollama (Optional)

```bash
# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Convert to GGUF
python convert.py \
  --model-path ~/crowelogic-pharma-mistral-7b \
  --outfile ~/CroweLogic-Pharma-7B.gguf

# Quantize (optional, for smaller size)
./quantize ~/CroweLogic-Pharma-7B.gguf \
  ~/CroweLogic-Pharma-7B-Q4_K_M.gguf Q4_K_M

# Import to Ollama
ollama create CroweLogic-Pharma:7b -f Modelfile
```

### 2. Push to Hugging Face Hub

```python
from transformers import AutoTokenizer
from peft import PeftModel, AutoModelForCausalLM

# Load model
base_model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
model = PeftModel.from_pretrained(base_model, "./crowelogic-pharma-mistral-7b")
tokenizer = AutoTokenizer.from_pretrained("./crowelogic-pharma-mistral-7b")

# Merge LoRA adapters (optional)
merged_model = model.merge_and_unload()

# Push to Hub
merged_model.push_to_hub("MichaelCrowe11/CroweLogic-Pharma-Mistral-7B")
tokenizer.push_to_hub("MichaelCrowe11/CroweLogic-Pharma-Mistral-7B")
```

### 3. Integrate into GitHub Repository

```bash
# Clone your repo
git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model
cd crowelogic-pharma-model

# Add model loading code
# See example in next section
```

---

## Using the Trained Model

### Local Inference (Python)

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Load model
base_model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    torch_dtype=torch.float16,
    device_map="auto"
)

model = PeftModel.from_pretrained(
    base_model,
    "./crowelogic-pharma-mistral-7b"
)

tokenizer = AutoTokenizer.from_pretrained("./crowelogic-pharma-mistral-7b")

# Query
def ask_model(question):
    prompt = f"<s>[INST] {question} [/INST]"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("[/INST]")[-1].strip()

# Test
response = ask_model("What is the mechanism of action of penicillin?")
print(response)
```

### Via Ollama (After GGUF Conversion)

```bash
# Run model
ollama run CroweLogic-Pharma:7b

# Query
>>> What is the molecular formula of aspirin?
>>> Explain the Crowe Logic multi-phase analysis pipeline.
```

---

## Cost Comparison

| Platform | GPU | Cost/Hour | Est. Total Cost | Pros | Cons |
|----------|-----|-----------|----------------|------|------|
| **RunPod** | RTX 4090 | $0.39 | $2.34-3.12 (6-8h) | Cheapest, easy | Community cloud |
| **RunPod** | A100 40GB | $1.29 | $5.16-7.74 (4-6h) | Fast, reliable | Mid-price |
| **RunPod** | A100 80GB | $1.89 | $5.67-9.45 (3-5h) | Fastest | Higher cost |
| **Lambda Labs** | A100 40GB | $1.10 | $4.40-6.60 (4-6h) | Good support | Limited availability |
| **Lambda Labs** | A100 80GB | $1.99 | $5.97-9.95 (3-5h) | Premium | Most expensive |
| **Google Colab Pro** | A100 | $10/mo | $10 (subscription) | Easy UI | 12h limit |
| **Modal** | A100 | ~$1.50 | $4.50-7.50 (3-5h) | Serverless | Complex setup |

**Recommendation:**
- **Best value:** RunPod RTX 4090 ($2.34-3.12)
- **Best speed:** RunPod A100 80GB ($5.67-9.45)
- **Easiest:** Google Colab Pro ($10/month subscription)

---

## Monitoring Training

### Check Training Progress

```bash
# Via terminal logs
tail -f /workspace/crowelogic-pharma-mistral-7b/trainer_state.json

# Via Weights & Biases (if enabled)
# Visit: https://wandb.ai/your-username/crowelogic-pharma-mistral
```

### Expected Metrics

```
Initial loss: ~3.5-4.0
After epoch 1: ~1.5-2.0
After epoch 2: ~1.0-1.5
After epoch 3: ~0.8-1.2
```

### GPU Memory Usage

```bash
# Monitor GPU
watch nvidia-smi

# Expected usage on A100 40GB:
# Model: ~8GB
# Training: ~20-30GB
# Peak: ~35GB
```

---

## Troubleshooting

### OOM (Out of Memory) Errors

```python
# Reduce batch size
BATCH_SIZE = 2  # or 1

# Reduce sequence length
MAX_SEQ_LENGTH = 256

# Reduce LoRA rank
LORA_R = 8
```

### Training Too Slow

```python
# Increase batch size (if GPU has memory)
BATCH_SIZE = 8

# Reduce validation frequency
EVAL_STEPS = 1000  # instead of 500
```

### Loss Not Decreasing

```python
# Increase learning rate
LEARNING_RATE = 3e-4

# Increase training epochs
NUM_EPOCHS = 4

# Check data quality
# Review sample examples to ensure proper formatting
```

---

## Next Steps

1. ✅ Choose cloud platform (RunPod recommended)
2. ✅ Upload datasets to cloud GPU
3. ✅ Run `train_cloud_gpu.py`
4. ✅ Monitor training (4-8 hours)
5. ✅ Download trained model
6. ✅ Test model locally
7. ✅ Convert to GGUF for Ollama (optional)
8. ✅ Push to Hugging Face Hub
9. ✅ Integrate into GitHub repo

---

## Support & Resources

- **RunPod Docs:** https://docs.runpod.io/
- **Lambda Labs:** https://lambdalabs.com/blog
- **Hugging Face:** https://huggingface.co/docs
- **LoRA Paper:** https://arxiv.org/abs/2106.09685
- **QLoRA Paper:** https://arxiv.org/abs/2305.14314

---

**Ready to train!** 🚀

Your 100,000 example dataset is prepared and the training script is optimized for cloud GPUs. Select a platform above and follow the steps to train your CroweLogic-Pharma model.

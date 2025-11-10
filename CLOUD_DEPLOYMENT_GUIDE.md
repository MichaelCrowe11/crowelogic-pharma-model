# Cloud Deployment Guide - 10M Dataset Generation

## Quick Start

```bash
# 1. Create deployment package
./cloud_deploy.sh runpod

# 2. Upload to cloud (instructions provided by script)
scp cloud_deployment_package.tar.gz root@<instance-ip>:/workspace/

# 3. SSH into cloud instance
ssh root@<instance-ip>

# 4. Setup and run
tar -xzf cloud_deployment_package.tar.gz
cd cloud_deployment_package
./cloud_setup.sh
./quick_start.sh
```

**Time to 10M examples:** 18-24 hours
**Cost:** $4-20 depending on platform

---

## Platform Comparison

| Platform | Instance Type | vCPUs | Cost/Hour | 24hr Cost | Speed | Difficulty |
|----------|---------------|-------|-----------|-----------|-------|------------|
| **RunPod** | CPU Pod | 32 | $0.20 | $5 | Fast | ⭐ Easy |
| **Vast.ai** | CPU | 32 | $0.15 | $4 | Fast | ⭐⭐ Medium |
| **Lambda Labs** | CPU | 32 | $0.50 | $12 | Fast | ⭐ Easy |
| **GCP** | n2-standard-32 | 32 | $0.77 | $18 | Fast | ⭐⭐⭐ Hard |
| **AWS** | c7i.8xlarge | 32 | $0.51 | $12 | Fast | ⭐⭐⭐ Hard |
| **Local M1 Mac** | 8 cores | 8 | $0 | $0 | Slow | ⭐ Easy |

**Recommended:** RunPod (best value, easy setup)

---

## Step-by-Step: RunPod Deployment

### 1. Create RunPod Account

1. Go to https://www.runpod.io/
2. Sign up (email or GitHub)
3. Add $100 credits (via credit card or crypto)
4. Verify email

### 2. Prepare Deployment Package

On your local Mac:

```bash
cd ~/crowelogic-pharma-model

# Create deployment package
./cloud_deploy.sh runpod

# This creates: cloud_deployment_package.tar.gz
ls -lh cloud_deployment_package.tar.gz
```

### 3. Deploy Pod on RunPod

1. **Go to Pods page:** https://www.runpod.io/console/pods
2. **Click "Deploy"**
3. **Select Template:**
   - Click "RunPod Pytorch" or "Ubuntu" template
4. **Configure Pod:**
   - **GPU Type:** Select "CPU" (cheapest) or "RTX A4000" (if you want GPU)
   - **vCPU:** 32 cores minimum
   - **RAM:** 64GB minimum
   - **Container Disk:** 50GB
   - **Volume Disk:** 100GB (for output)
5. **Expose Ports:** Enable HTTP service (port 8888)
6. **Deploy Pod** (takes 30-60 seconds)

### 4. Upload Deployment Package

You'll see your pod with an IP address and SSH port.

**Option A: Via SCP (recommended)**
```bash
# From your local machine
scp -P <SSH_PORT> cloud_deployment_package.tar.gz root@<POD_IP>:/workspace/
```

**Option B: Via RunPod Web Terminal**
1. Click "Connect" → "Web Terminal"
2. In terminal:
```bash
cd /workspace
# Then paste wget/curl command to download from your server
# Or use RunPod's file upload feature
```

### 5. SSH into Pod

```bash
# Get connection details from RunPod dashboard
ssh root@<POD_IP> -p <SSH_PORT>

# Or use RunPod's "Connect via SSH" button to get exact command
```

### 6. Setup and Run Generation

```bash
cd /workspace
tar -xzf cloud_deployment_package.tar.gz
cd cloud_deployment_package

# Install dependencies and setup
./cloud_setup.sh

# Start generation
./quick_start.sh

# This will start generation in background with nohup
```

### 7. Monitor Progress

**Option A: Check monitor script**
```bash
./monitor_10m_generation.sh
```

**Option B: Watch logs**
```bash
tail -f logs/generation_10m.log
```

**Option C: Check output file**
```bash
tail generation.out
```

**Option D: From local machine (keep checking)**
```bash
# Run this from your Mac every hour
ssh root@<POD_IP> -p <SSH_PORT> 'cd /workspace/cloud_deployment_package && ./monitor_10m_generation.sh'
```

### 8. Download Results

After 18-24 hours, generation completes:

```bash
# From your local Mac
cd ~/crowelogic-pharma-model

# Download the generated data
scp -P <SSH_PORT> -r root@<POD_IP>:/workspace/cloud_deployment_package/generated_data ./

# This downloads:
# - generated_data/massive_10m/batches/ (all batch files)
# - generated_data/massive_10m/massive_10m.jsonl (combined)
# - generated_data/massive_10m/massive_10m_train.jsonl (training set)
# - generated_data/massive_10m/massive_10m_val.jsonl (validation)
# - generated_data/massive_10m/massive_10m_test.jsonl (test)
```

**Alternative: Combine on cloud, download compressed**
```bash
# On the pod
cd /workspace/cloud_deployment_package/generated_data/massive_10m
tar -czf massive_10m_dataset.tar.gz massive_10m*.jsonl

# Then download
scp -P <SSH_PORT> root@<POD_IP>:/workspace/cloud_deployment_package/generated_data/massive_10m/massive_10m_dataset.tar.gz ./
```

### 9. Terminate Pod ⚠️ IMPORTANT

**Don't forget to terminate the pod when done!**

1. Go to RunPod console
2. Find your pod
3. Click "Terminate"
4. Confirm termination

**If you don't terminate:** You'll keep getting charged $0.20/hour!

---

## Cost Breakdown

### RunPod 32-core CPU Pod

**Hourly rate:** $0.20/hour

**Generation time:** 18-24 hours (estimate 20 hours avg)

**Total cost:** 20 hours × $0.20 = **$4**

**Data transfer:** Free (downloading results)

**Total:** ~$5 including buffer

### If Using GPU Pod (Optional)

**RTX A4000 (16GB):** $0.39/hour × 20 hours = **$8**

**RTX 4090 (24GB):** $0.69/hour × 20 hours = **$14**

(GPU won't speed up current generation much, CPU is fine)

---

## Troubleshooting

### Issue: Can't SSH into pod
**Solution:**
- Check SSH port (not always 22)
- Check IP address is correct
- Make sure pod status is "Running"
- Try web terminal as alternative

### Issue: Upload taking too long
**Solution:**
- Package is ~50MB, should take 1-2 minutes
- Check your internet speed
- Try web terminal upload
- Or use wget to pull from your server

### Issue: Setup fails
**Solution:**
```bash
# Check Python version
python3 --version  # Should be 3.8+

# Manually install dependencies
pip3 install requests tqdm

# Check if files are there
ls -la
```

### Issue: Generation is slow
**Solution:**
- Check CPU usage: `htop` or `top`
- Make sure 32 cores are allocated
- Check if swap is being used (bad): `free -h`
- Upgrade to more cores if needed

### Issue: Out of disk space
**Solution:**
```bash
# Check disk usage
df -h

# Clear cache if needed
rm -rf cache/*

# Or add volume storage in RunPod
```

### Issue: Process killed
**Solution:**
- Check logs: `tail logs/generation_10m.log`
- Check if out of memory: `dmesg | grep oom`
- Resume: `python3 generate_10m_optimized.py` (auto-resumes)

### Issue: Want to pause generation
**Solution:**
```bash
# Find process
ps aux | grep generate_10m

# Kill gracefully (saves checkpoint)
pkill -f generate_10m_optimized.py

# Resume later
python3 generate_10m_optimized.py
```

---

## Monitoring from Local Machine

Create this script on your Mac:

```bash
#!/bin/bash
# check_cloud_progress.sh

SSH_CMD="ssh root@<POD_IP> -p <SSH_PORT>"

echo "Checking cloud generation progress..."
$SSH_CMD "cd /workspace/cloud_deployment_package && ./monitor_10m_generation.sh"
```

Run every hour:
```bash
watch -n 3600 ./check_cloud_progress.sh
```

Or setup cron job:
```bash
# Check every hour and save to log
0 * * * * ~/crowelogic-pharma-model/check_cloud_progress.sh >> ~/generation_checks.log 2>&1
```

---

## Advanced: Multi-Instance Parallel Generation

Generate 10M faster by running multiple instances:

### Setup (5 instances × 2M each)

**Instance 1:** Generate 0-2M examples
```bash
python3 generate_10m_optimized.py --target 2000000 --output-dir generated_data/batch_1
```

**Instance 2:** Generate 2M-4M examples
```bash
# Use different synthetic seed
python3 generate_10m_optimized.py --target 2000000 --output-dir generated_data/batch_2
```

**Repeat for instances 3, 4, 5**

### Combine Results (local)
```bash
cd ~/crowelogic-pharma-model

# Download all batches
for i in 1 2 3 4 5; do
  scp -r root@<POD${i}_IP>:/workspace/generated_data/batch_$i ./batches/
done

# Combine
cat batches/batch_*/massive_10m.jsonl > massive_10m_combined.jsonl

# Count
wc -l massive_10m_combined.jsonl  # Should be 10M
```

**Time:** 4-5 hours instead of 20 hours
**Cost:** 5 instances × 5 hours × $0.20 = $5 (same cost!)

---

## Security Best Practices

### 1. Don't commit credentials
```bash
# Add to .gitignore
echo "cloud_deployment_package/" >> .gitignore
echo "*.pem" >> .gitignore
```

### 2. Use SSH keys (not passwords)
```bash
# Generate key
ssh-keygen -t ed25519 -f ~/.ssh/runpod_key

# Add to RunPod
# Go to Account → SSH Keys → Add key
```

### 3. Close ports when done
- Terminate pod immediately after download
- Don't leave running overnight if not generating

### 4. Monitor costs
- Set billing alerts in RunPod
- Check usage daily: https://www.runpod.io/console/user/billing

---

## Performance Expectations

### Generation Rate by Instance Type

| vCPUs | RAM | Examples/Hour | Time to 10M | Cost to 10M |
|-------|-----|---------------|-------------|-------------|
| 8 | 16GB | 140K | 72 hours | $14 |
| 16 | 32GB | 280K | 36 hours | $7 |
| 32 | 64GB | 560K | 18 hours | $4 |
| 64 | 128GB | 800K | 13 hours | $5 |

**Sweet spot:** 32 vCPUs (diminishing returns above this)

### Checkpoint Frequency

- **Every 10K examples:** ~1 minute on 32-core
- **Checkpoint size:** ~5MB
- **Resume overhead:** <30 seconds

---

## Download Optimization

### Compress Before Download
```bash
# On cloud instance
cd generated_data/massive_10m
tar -czf massive_10m.tar.gz massive_10m*.jsonl

# Download compressed
scp root@<POD_IP>:/workspace/.../massive_10m.tar.gz ./

# Local size: ~2-3GB compressed vs 8-10GB uncompressed
```

### Resume Interrupted Downloads
```bash
# Use rsync instead of scp
rsync -avz -P -e "ssh -p <SSH_PORT>" \
  root@<POD_IP>:/workspace/cloud_deployment_package/generated_data \
  ./

# -P shows progress and allows resume
# -z compresses during transfer
```

---

## Alternative Platforms

### Lambda Labs

**Pros:**
- High-quality hardware
- Good documentation
- Reliable

**Cons:**
- More expensive ($0.50/hr for CPU)
- Sometimes low availability

**Setup:**
```bash
./cloud_deploy.sh lambda
# Follow instructions
```

### Vast.ai

**Pros:**
- Cheapest option ($0.10-0.20/hr)
- Many instance choices

**Cons:**
- Community providers (less reliable)
- Setup can be tricky
- Mixed instance quality

**Setup:**
```bash
./cloud_deploy.sh vast
# Follow instructions
```

### AWS/GCP

**Pros:**
- Enterprise-grade
- Very reliable
- More control

**Cons:**
- Expensive ($0.50-1.00/hr)
- Complex setup
- Billing can be confusing

**Only use if:** You already have credits or enterprise account

---

## Post-Generation Checklist

After generation completes:

- [ ] Verify example count: `wc -l massive_10m.jsonl` (should be 10,000,000)
- [ ] Check file sizes (should be ~8-10GB total)
- [ ] Verify format: `head -1 massive_10m.jsonl | jq .`
- [ ] Download all files (train, val, test splits)
- [ ] **Terminate cloud instance**
- [ ] Upload to Hugging Face (optional)
- [ ] Begin model training

---

## Quick Reference

```bash
# Local: Create package
./cloud_deploy.sh runpod

# Local: Upload to cloud
scp -P <PORT> cloud_deployment_package.tar.gz root@<IP>:/workspace/

# Cloud: Setup
tar -xzf cloud_deployment_package.tar.gz && cd cloud_deployment_package
./cloud_setup.sh

# Cloud: Start
./quick_start.sh

# Cloud: Monitor
./monitor_10m_generation.sh

# Local: Check progress
ssh root@<IP> -p <PORT> 'cd /workspace/cloud_deployment_package && ./monitor_10m_generation.sh'

# Local: Download results
scp -P <PORT> -r root@<IP>:/workspace/cloud_deployment_package/generated_data ./

# Cloud/RunPod: Terminate pod (IMPORTANT!)
```

---

## Support

Questions? Issues?

1. Check logs: `logs/generation_10m.log`
2. Review this guide
3. GitHub issues: https://github.com/MichaelCrowe11/crowelogic-pharma-model/issues

---

**Ready to deploy!** 🚀

Start with: `./cloud_deploy.sh runpod`

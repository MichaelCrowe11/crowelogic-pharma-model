# Cloud Deployment - Quick Start

**Generate 100K+ compounds in 1 hour using cloud parallelization**

## What You'll Get

- **Speed:** 10-100x faster than single PC
- **Cost:** $1-5 for 100K compounds
- **Scale:** Unlimited parallelization
- **Automation:** Set it and forget it

---

## Option 1: Simple Cloud Deployment (Recommended)

### Step 1: Generate Deployment Scripts

```bash
cd ~/crowelogic-pharma-model

# Generate AWS deployment for 20 instances
python cloud_deploy.py --provider aws --num-instances 20

# Or GCP
python cloud_deploy.py --provider gcp --num-instances 20
```

This creates:
- `deploy_aws.sh` or `deploy_gcp.sh`
- `startup_script.sh`

### Step 2: Configure

Edit the generated scripts:

```bash
# In deploy_aws.sh or deploy_gcp.sh:
# - Update SSH key name
# - Update S3/GCS bucket name

# In startup_script.sh:
# - Update GitHub repo URL
# - Uncomment upload commands
```

### Step 3: Deploy

```bash
# AWS
chmod +x deploy_aws.sh
./deploy_aws.sh

# GCP
chmod +x deploy_gcp.sh
./deploy_gcp.sh
```

### Step 4: Monitor

```bash
# Monitor cloud storage for results
python collect_cloud_results.py --provider aws --bucket your-bucket --monitor
```

### Step 5: Collect & Combine

```bash
# Download and combine all batches
python collect_cloud_results.py --provider aws --bucket your-bucket --combine
```

---

## Option 2: Docker Local Testing

Test the system locally before deploying to cloud:

```bash
# Build Docker image
docker build -t pharma-batch .

# Run 5 batches in parallel
docker-compose up

# Results in: generated_data/batches/
```

---

## Cost Estimates

### AWS Spot Instances (t3.medium)

| Instances | Compounds | Time | Cost |
|-----------|-----------|------|------|
| 10 | 10K | 1hr | $0.10 |
| 20 | 20K | 1hr | $0.20 |
| 50 | 50K | 1hr | $0.50 |
| 100 | 100K | 1hr | $1.00 |

### GCP Preemptible (e2-standard-2)

| Instances | Compounds | Time | Cost |
|-----------|-----------|------|------|
| 10 | 10K | 1hr | $0.20 |
| 20 | 20K | 1hr | $0.40 |
| 50 | 50K | 1hr | $1.00 |
| 100 | 100K | 1hr | $2.00 |

---

## Architecture

```
Your PC
  ↓
cloud_deploy.py → Generates deployment scripts
  ↓
AWS/GCP
  ↓
20 instances × generate_batch.py (parallel)
  ↓
S3/GCS Storage (batch results)
  ↓
collect_cloud_results.py → Downloads & combines
  ↓
Final dataset (train/val/test splits)
```

---

## Files Created

- `cloud_deploy.py` - Orchestration script
- `generate_batch.py` - Batch generator (runs on cloud)
- `collect_cloud_results.py` - Results collector
- `combine_batches.py` - Batch combiner
- `Dockerfile` - Container definition
- `docker-compose.yml` - Local testing
- `CLOUD_DEPLOYMENT_GUIDE.md` - Full guide
- `PARALLEL_GENERATION_GUIDE.txt` - Multi-PC guide

---

## Quick Commands

```bash
# Generate deployment scripts
python cloud_deploy.py --provider aws --num-instances 20

# Deploy to cloud
./deploy_aws.sh   # or ./deploy_gcp.sh

# Monitor progress
python collect_cloud_results.py --provider aws --bucket your-bucket --monitor

# Collect results
python collect_cloud_results.py --provider aws --bucket your-bucket --combine

# Test locally first
docker-compose up
```

---

## Troubleshooting

**Instances not starting?**
- Check SSH key exists
- Verify AMI ID for your region (AWS)
- Check billing/quotas

**No results in storage?**
- Verify bucket name in startup_script.sh
- Check instance IAM permissions
- SSH into instance and check logs

**Network errors?**
- These are expected (DNS issues we saw earlier)
- Script has retry logic built-in
- Cached compounds will be reused

---

## Next Steps

1. **Test locally:** `docker-compose up`
2. **Generate scripts:** `python cloud_deploy.py --provider aws --num-instances 10`
3. **Configure:** Update SSH keys and bucket names
4. **Deploy:** `./deploy_aws.sh`
5. **Monitor:** `python collect_cloud_results.py --monitor`
6. **Collect:** `python collect_cloud_results.py --combine`

**Full documentation:** See `CLOUD_DEPLOYMENT_GUIDE.md`

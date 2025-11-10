# Deploy to AWS Cloud - Quick Start

**100 instances × 1 hour = 100K compounds for ~$1-2**

## Step 1: Run AWS Setup (5 minutes)

```bash
./aws_setup.sh
```

This will automatically:
- ✓ Install AWS CLI
- ✓ Configure your AWS credentials
- ✓ Create an S3 bucket
- ✓ Create SSH key
- ✓ Configure all scripts

## Step 2: Push Code to GitHub

```bash
git add .
git commit -m "Add cloud deployment"
git push
```

## Step 3: Deploy!

```bash
./deploy_aws.sh
```

Launches 100 instances that generate ~100K compounds in 1 hour!

## Step 4: Collect Results (after ~1 hour)

```bash
# Check what's generated
python3 collect_cloud_results.py --provider aws --bucket YOUR_BUCKET --monitor

# Download everything
python3 collect_cloud_results.py --provider aws --bucket YOUR_BUCKET --combine
```

---

**Cost:** ~$1-2 for 100K compounds
**Time:** ~1 hour
**Output:** 1M+ training examples

Ready? Run: `./aws_setup.sh`

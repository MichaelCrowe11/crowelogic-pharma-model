#!/bin/bash
# AWS Setup Script for Cloud Deployment

echo "========================================"
echo "AWS Cloud Deployment Setup"
echo "========================================"
echo ""

# Step 1: Install AWS CLI
echo "Step 1: Installing AWS CLI..."
if command -v aws &> /dev/null; then
    echo "✓ AWS CLI already installed"
    aws --version
else
    echo "Installing AWS CLI..."
    curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "/tmp/AWSCLIV2.pkg"
    sudo installer -pkg /tmp/AWSCLIV2.pkg -target /
    rm /tmp/AWSCLIV2.pkg
    echo "✓ AWS CLI installed"
fi

echo ""
echo "========================================"
echo "Step 2: AWS Credentials Setup"
echo "========================================"
echo ""
echo "You need AWS credentials to deploy instances."
echo ""
echo "To get your credentials:"
echo "1. Go to: https://console.aws.amazon.com/iam/home#/security_credentials"
echo "2. Click 'Create access key' under 'Access keys'"
echo "3. Download the credentials CSV"
echo ""
echo "Ready to configure? (You'll need Access Key ID and Secret Access Key)"
read -p "Press Enter to continue..."

# Configure AWS
aws configure

echo ""
echo "✓ AWS credentials configured!"
echo ""

# Step 3: Create S3 Bucket
echo "========================================"
echo "Step 3: Create S3 Bucket"
echo "========================================"
echo ""

# Generate unique bucket name
BUCKET_NAME="pharma-batch-$(date +%Y%m%d)-$(whoami)"
echo "Creating S3 bucket: $BUCKET_NAME"

aws s3 mb s3://$BUCKET_NAME --region us-east-1

if [ $? -eq 0 ]; then
    echo "✓ S3 bucket created: s3://$BUCKET_NAME"
    echo ""

    # Update startup script with bucket name
    echo "Updating startup_script.sh with bucket name..."
    sed -i.bak "s|s3://your-pharma-bucket|s3://$BUCKET_NAME|g" startup_script.sh

    # Uncomment S3 upload lines
    sed -i.bak 's|# aws s3 cp|aws s3 cp|g' startup_script.sh

    # Enable auto-shutdown to save costs
    sed -i.bak 's|# sudo shutdown -h now|sudo shutdown -h now|g' startup_script.sh

    echo "✓ startup_script.sh configured"
    echo ""
else
    echo "Error creating bucket. It may already exist or you may need different permissions."
    echo "You can create it manually at: https://s3.console.aws.amazon.com/s3/buckets"
fi

# Step 4: SSH Key Setup
echo "========================================"
echo "Step 4: SSH Key Setup"
echo "========================================"
echo ""

KEY_NAME="pharma-batch-key"
KEY_FILE="$HOME/.ssh/$KEY_NAME.pem"

if [ -f "$KEY_FILE" ]; then
    echo "✓ SSH key already exists: $KEY_FILE"
else
    echo "Creating EC2 key pair: $KEY_NAME"
    aws ec2 create-key-pair --key-name $KEY_NAME --query 'KeyMaterial' --output text > $KEY_FILE
    chmod 400 $KEY_FILE
    echo "✓ SSH key created: $KEY_FILE"
fi

# Update deploy script with key name
sed -i.bak "s|your-key-name|$KEY_NAME|g" deploy_aws.sh

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Configuration summary:"
echo "  S3 Bucket: $BUCKET_NAME"
echo "  SSH Key: $KEY_NAME"
echo "  Region: us-east-1"
echo "  Instances: 100 (spot instances)"
echo "  Expected cost: ~\$1-2 for 1 hour"
echo ""
echo "Next steps:"
echo "  1. Push your latest code to GitHub:"
echo "     git add ."
echo "     git commit -m 'Add cloud deployment scripts'"
echo "     git push"
echo ""
echo "  2. Deploy to AWS:"
echo "     ./deploy_aws.sh"
echo ""
echo "  3. Monitor progress:"
echo "     python3 collect_cloud_results.py --provider aws --bucket $BUCKET_NAME --monitor"
echo ""
echo "  4. Collect results (after ~1 hour):"
echo "     python3 collect_cloud_results.py --provider aws --bucket $BUCKET_NAME --combine"
echo ""
echo "Ready to deploy? Run: ./deploy_aws.sh"
echo ""

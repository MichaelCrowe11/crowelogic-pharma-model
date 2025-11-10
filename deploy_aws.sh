#!/bin/bash
# AWS Deployment Script
# Deploy 100 instances for batch generation

set -e

DEPLOYMENT_ID=20251110_045340
REGION=us-east-1
INSTANCE_TYPE=t3.medium
AMI_ID=ami-0c55b159cbfafe1f0  # Update for your region


# Launch batch 0
echo 'Launching pharma-batch-20251110_045340-0...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-0"},
        {"Key": "BatchID", "Value": "0"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 1
echo 'Launching pharma-batch-20251110_045340-1...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-1"},
        {"Key": "BatchID", "Value": "1"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 2
echo 'Launching pharma-batch-20251110_045340-2...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-2"},
        {"Key": "BatchID", "Value": "2"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 3
echo 'Launching pharma-batch-20251110_045340-3...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-3"},
        {"Key": "BatchID", "Value": "3"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 4
echo 'Launching pharma-batch-20251110_045340-4...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-4"},
        {"Key": "BatchID", "Value": "4"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 5
echo 'Launching pharma-batch-20251110_045340-5...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-5"},
        {"Key": "BatchID", "Value": "5"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 6
echo 'Launching pharma-batch-20251110_045340-6...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-6"},
        {"Key": "BatchID", "Value": "6"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 7
echo 'Launching pharma-batch-20251110_045340-7...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-7"},
        {"Key": "BatchID", "Value": "7"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 8
echo 'Launching pharma-batch-20251110_045340-8...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-8"},
        {"Key": "BatchID", "Value": "8"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 9
echo 'Launching pharma-batch-20251110_045340-9...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-9"},
        {"Key": "BatchID", "Value": "9"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 10
echo 'Launching pharma-batch-20251110_045340-10...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-10"},
        {"Key": "BatchID", "Value": "10"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 11
echo 'Launching pharma-batch-20251110_045340-11...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-11"},
        {"Key": "BatchID", "Value": "11"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 12
echo 'Launching pharma-batch-20251110_045340-12...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-12"},
        {"Key": "BatchID", "Value": "12"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 13
echo 'Launching pharma-batch-20251110_045340-13...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-13"},
        {"Key": "BatchID", "Value": "13"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 14
echo 'Launching pharma-batch-20251110_045340-14...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-14"},
        {"Key": "BatchID", "Value": "14"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 15
echo 'Launching pharma-batch-20251110_045340-15...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-15"},
        {"Key": "BatchID", "Value": "15"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 16
echo 'Launching pharma-batch-20251110_045340-16...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-16"},
        {"Key": "BatchID", "Value": "16"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 17
echo 'Launching pharma-batch-20251110_045340-17...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-17"},
        {"Key": "BatchID", "Value": "17"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 18
echo 'Launching pharma-batch-20251110_045340-18...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-18"},
        {"Key": "BatchID", "Value": "18"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 19
echo 'Launching pharma-batch-20251110_045340-19...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-19"},
        {"Key": "BatchID", "Value": "19"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 20
echo 'Launching pharma-batch-20251110_045340-20...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-20"},
        {"Key": "BatchID", "Value": "20"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 21
echo 'Launching pharma-batch-20251110_045340-21...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-21"},
        {"Key": "BatchID", "Value": "21"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 22
echo 'Launching pharma-batch-20251110_045340-22...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-22"},
        {"Key": "BatchID", "Value": "22"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 23
echo 'Launching pharma-batch-20251110_045340-23...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-23"},
        {"Key": "BatchID", "Value": "23"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 24
echo 'Launching pharma-batch-20251110_045340-24...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-24"},
        {"Key": "BatchID", "Value": "24"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 25
echo 'Launching pharma-batch-20251110_045340-25...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-25"},
        {"Key": "BatchID", "Value": "25"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 26
echo 'Launching pharma-batch-20251110_045340-26...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-26"},
        {"Key": "BatchID", "Value": "26"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 27
echo 'Launching pharma-batch-20251110_045340-27...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-27"},
        {"Key": "BatchID", "Value": "27"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 28
echo 'Launching pharma-batch-20251110_045340-28...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-28"},
        {"Key": "BatchID", "Value": "28"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 29
echo 'Launching pharma-batch-20251110_045340-29...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-29"},
        {"Key": "BatchID", "Value": "29"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 30
echo 'Launching pharma-batch-20251110_045340-30...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-30"},
        {"Key": "BatchID", "Value": "30"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 31
echo 'Launching pharma-batch-20251110_045340-31...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-31"},
        {"Key": "BatchID", "Value": "31"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 32
echo 'Launching pharma-batch-20251110_045340-32...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-32"},
        {"Key": "BatchID", "Value": "32"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 33
echo 'Launching pharma-batch-20251110_045340-33...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-33"},
        {"Key": "BatchID", "Value": "33"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 34
echo 'Launching pharma-batch-20251110_045340-34...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-34"},
        {"Key": "BatchID", "Value": "34"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 35
echo 'Launching pharma-batch-20251110_045340-35...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-35"},
        {"Key": "BatchID", "Value": "35"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 36
echo 'Launching pharma-batch-20251110_045340-36...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-36"},
        {"Key": "BatchID", "Value": "36"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 37
echo 'Launching pharma-batch-20251110_045340-37...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-37"},
        {"Key": "BatchID", "Value": "37"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 38
echo 'Launching pharma-batch-20251110_045340-38...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-38"},
        {"Key": "BatchID", "Value": "38"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 39
echo 'Launching pharma-batch-20251110_045340-39...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-39"},
        {"Key": "BatchID", "Value": "39"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 40
echo 'Launching pharma-batch-20251110_045340-40...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-40"},
        {"Key": "BatchID", "Value": "40"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 41
echo 'Launching pharma-batch-20251110_045340-41...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-41"},
        {"Key": "BatchID", "Value": "41"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 42
echo 'Launching pharma-batch-20251110_045340-42...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-42"},
        {"Key": "BatchID", "Value": "42"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 43
echo 'Launching pharma-batch-20251110_045340-43...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-43"},
        {"Key": "BatchID", "Value": "43"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 44
echo 'Launching pharma-batch-20251110_045340-44...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-44"},
        {"Key": "BatchID", "Value": "44"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 45
echo 'Launching pharma-batch-20251110_045340-45...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-45"},
        {"Key": "BatchID", "Value": "45"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 46
echo 'Launching pharma-batch-20251110_045340-46...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-46"},
        {"Key": "BatchID", "Value": "46"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 47
echo 'Launching pharma-batch-20251110_045340-47...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-47"},
        {"Key": "BatchID", "Value": "47"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 48
echo 'Launching pharma-batch-20251110_045340-48...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-48"},
        {"Key": "BatchID", "Value": "48"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 49
echo 'Launching pharma-batch-20251110_045340-49...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-49"},
        {"Key": "BatchID", "Value": "49"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 50
echo 'Launching pharma-batch-20251110_045340-50...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-50"},
        {"Key": "BatchID", "Value": "50"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 51
echo 'Launching pharma-batch-20251110_045340-51...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-51"},
        {"Key": "BatchID", "Value": "51"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 52
echo 'Launching pharma-batch-20251110_045340-52...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-52"},
        {"Key": "BatchID", "Value": "52"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 53
echo 'Launching pharma-batch-20251110_045340-53...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-53"},
        {"Key": "BatchID", "Value": "53"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 54
echo 'Launching pharma-batch-20251110_045340-54...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-54"},
        {"Key": "BatchID", "Value": "54"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 55
echo 'Launching pharma-batch-20251110_045340-55...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-55"},
        {"Key": "BatchID", "Value": "55"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 56
echo 'Launching pharma-batch-20251110_045340-56...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-56"},
        {"Key": "BatchID", "Value": "56"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 57
echo 'Launching pharma-batch-20251110_045340-57...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-57"},
        {"Key": "BatchID", "Value": "57"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 58
echo 'Launching pharma-batch-20251110_045340-58...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-58"},
        {"Key": "BatchID", "Value": "58"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 59
echo 'Launching pharma-batch-20251110_045340-59...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-59"},
        {"Key": "BatchID", "Value": "59"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 60
echo 'Launching pharma-batch-20251110_045340-60...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-60"},
        {"Key": "BatchID", "Value": "60"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 61
echo 'Launching pharma-batch-20251110_045340-61...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-61"},
        {"Key": "BatchID", "Value": "61"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 62
echo 'Launching pharma-batch-20251110_045340-62...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-62"},
        {"Key": "BatchID", "Value": "62"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 63
echo 'Launching pharma-batch-20251110_045340-63...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-63"},
        {"Key": "BatchID", "Value": "63"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 64
echo 'Launching pharma-batch-20251110_045340-64...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-64"},
        {"Key": "BatchID", "Value": "64"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 65
echo 'Launching pharma-batch-20251110_045340-65...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-65"},
        {"Key": "BatchID", "Value": "65"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 66
echo 'Launching pharma-batch-20251110_045340-66...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-66"},
        {"Key": "BatchID", "Value": "66"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 67
echo 'Launching pharma-batch-20251110_045340-67...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-67"},
        {"Key": "BatchID", "Value": "67"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 68
echo 'Launching pharma-batch-20251110_045340-68...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-68"},
        {"Key": "BatchID", "Value": "68"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 69
echo 'Launching pharma-batch-20251110_045340-69...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-69"},
        {"Key": "BatchID", "Value": "69"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 70
echo 'Launching pharma-batch-20251110_045340-70...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-70"},
        {"Key": "BatchID", "Value": "70"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 71
echo 'Launching pharma-batch-20251110_045340-71...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-71"},
        {"Key": "BatchID", "Value": "71"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 72
echo 'Launching pharma-batch-20251110_045340-72...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-72"},
        {"Key": "BatchID", "Value": "72"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 73
echo 'Launching pharma-batch-20251110_045340-73...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-73"},
        {"Key": "BatchID", "Value": "73"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 74
echo 'Launching pharma-batch-20251110_045340-74...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-74"},
        {"Key": "BatchID", "Value": "74"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 75
echo 'Launching pharma-batch-20251110_045340-75...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-75"},
        {"Key": "BatchID", "Value": "75"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 76
echo 'Launching pharma-batch-20251110_045340-76...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-76"},
        {"Key": "BatchID", "Value": "76"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 77
echo 'Launching pharma-batch-20251110_045340-77...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-77"},
        {"Key": "BatchID", "Value": "77"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 78
echo 'Launching pharma-batch-20251110_045340-78...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-78"},
        {"Key": "BatchID", "Value": "78"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 79
echo 'Launching pharma-batch-20251110_045340-79...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-79"},
        {"Key": "BatchID", "Value": "79"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 80
echo 'Launching pharma-batch-20251110_045340-80...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-80"},
        {"Key": "BatchID", "Value": "80"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 81
echo 'Launching pharma-batch-20251110_045340-81...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-81"},
        {"Key": "BatchID", "Value": "81"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 82
echo 'Launching pharma-batch-20251110_045340-82...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-82"},
        {"Key": "BatchID", "Value": "82"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 83
echo 'Launching pharma-batch-20251110_045340-83...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-83"},
        {"Key": "BatchID", "Value": "83"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 84
echo 'Launching pharma-batch-20251110_045340-84...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-84"},
        {"Key": "BatchID", "Value": "84"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 85
echo 'Launching pharma-batch-20251110_045340-85...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-85"},
        {"Key": "BatchID", "Value": "85"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 86
echo 'Launching pharma-batch-20251110_045340-86...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-86"},
        {"Key": "BatchID", "Value": "86"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 87
echo 'Launching pharma-batch-20251110_045340-87...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-87"},
        {"Key": "BatchID", "Value": "87"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 88
echo 'Launching pharma-batch-20251110_045340-88...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-88"},
        {"Key": "BatchID", "Value": "88"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 89
echo 'Launching pharma-batch-20251110_045340-89...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-89"},
        {"Key": "BatchID", "Value": "89"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 90
echo 'Launching pharma-batch-20251110_045340-90...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-90"},
        {"Key": "BatchID", "Value": "90"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 91
echo 'Launching pharma-batch-20251110_045340-91...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-91"},
        {"Key": "BatchID", "Value": "91"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 92
echo 'Launching pharma-batch-20251110_045340-92...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-92"},
        {"Key": "BatchID", "Value": "92"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 93
echo 'Launching pharma-batch-20251110_045340-93...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-93"},
        {"Key": "BatchID", "Value": "93"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 94
echo 'Launching pharma-batch-20251110_045340-94...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-94"},
        {"Key": "BatchID", "Value": "94"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 95
echo 'Launching pharma-batch-20251110_045340-95...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-95"},
        {"Key": "BatchID", "Value": "95"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 96
echo 'Launching pharma-batch-20251110_045340-96...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-96"},
        {"Key": "BatchID", "Value": "96"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 97
echo 'Launching pharma-batch-20251110_045340-97...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-97"},
        {"Key": "BatchID", "Value": "97"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 98
echo 'Launching pharma-batch-20251110_045340-98...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-98"},
        {"Key": "BatchID", "Value": "98"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

# Launch batch 99
echo 'Launching pharma-batch-20251110_045340-99...'
aws ec2 request-spot-instances \
  --region $REGION \
  --instance-count 1 \
  --type one-time \
  --launch-specification '{
    "ImageId": "$AMI_ID",
    "InstanceType": "$INSTANCE_TYPE",
    "KeyName": "pharma-batch-key",
    "UserData": "$(cat startup_script.sh | base64)",
    "TagSpecifications": [{
      "ResourceType": "instance",
      "Tags": [
        {"Key": "Name", "Value": "pharma-batch-20251110_045340-99"},
        {"Key": "BatchID", "Value": "99"},
        {"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}
      ]
    }]
  }'

sleep 2  # Rate limiting

echo 'Deployment complete!'
echo 'Monitor with: aws ec2 describe-instances --region $REGION --filters Name=tag:DeploymentID,Values=$DEPLOYMENT_ID'

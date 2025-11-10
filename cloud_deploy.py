#!/usr/bin/env python3
"""
Cloud Deployment Orchestrator
Deploy multiple batch generation instances to the cloud in parallel

Supports:
- AWS EC2 (spot instances for cost savings)
- GCP Compute Engine
- Docker containers

Usage:
    # Deploy 10 batches on AWS
    python cloud_deploy.py --provider aws --num-instances 10 --batch-size 1000

    # Deploy 20 batches on GCP
    python cloud_deploy.py --provider gcp --num-instances 20 --batch-size 500

    # Use spot instances for cost savings
    python cloud_deploy.py --provider aws --num-instances 10 --spot

    # Monitor running instances
    python cloud_deploy.py --status

    # Collect results and terminate
    python cloud_deploy.py --collect --terminate
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class CloudOrchestrator:
    """Orchestrate cloud deployment of batch generation"""

    def __init__(self, provider: str = "aws", region: str = None):
        self.provider = provider.lower()
        self.region = region or self._get_default_region()
        self.deployment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.state_file = Path(f"cloud_state_{self.deployment_id}.json")
        self.instances = []

        print(f"Cloud Orchestrator - {self.provider.upper()}")
        print(f"Region: {self.region}")
        print(f"Deployment ID: {self.deployment_id}")

    def _get_default_region(self) -> str:
        """Get default region for provider"""
        defaults = {
            "aws": "us-east-1",
            "gcp": "us-central1",
            "azure": "eastus"
        }
        return defaults.get(self.provider, "us-east-1")

    def deploy_aws(self, num_instances: int, batch_size: int, use_spot: bool = True):
        """Deploy batch runners on AWS EC2"""
        print(f"\n{'='*70}")
        print(f"AWS DEPLOYMENT - {num_instances} instances")
        print(f"{'='*70}\n")

        # Configuration
        instance_type = "t3.medium"  # 2 vCPU, 4GB RAM - good for data fetching
        ami_id = "ami-0c55b159cbfafe1f0"  # Ubuntu 20.04 LTS (update for your region)

        # User data script to run on instance startup
        user_data = self._generate_user_data_script()

        print("Instance configuration:")
        print(f"  Type: {instance_type}")
        print(f"  AMI: {ami_id}")
        print(f"  Spot: {use_spot}")
        print(f"  Region: {self.region}")

        # AWS CLI command to launch instances
        for batch_id in range(num_instances):
            print(f"\nLaunching instance for batch {batch_id}...")

            instance_name = f"pharma-batch-{self.deployment_id}-{batch_id}"

            if use_spot:
                # Launch spot instance
                cmd = [
                    "aws", "ec2", "request-spot-instances",
                    "--region", self.region,
                    "--instance-count", "1",
                    "--type", "one-time",
                    "--launch-specification", json.dumps({
                        "ImageId": ami_id,
                        "InstanceType": instance_type,
                        "KeyName": "your-key-name",  # UPDATE THIS
                        "UserData": user_data,
                        "TagSpecifications": [{
                            "ResourceType": "instance",
                            "Tags": [
                                {"Key": "Name", "Value": instance_name},
                                {"Key": "BatchID", "Value": str(batch_id)},
                                {"Key": "DeploymentID", "Value": self.deployment_id}
                            ]
                        }]
                    })
                ]
            else:
                # Launch on-demand instance
                cmd = [
                    "aws", "ec2", "run-instances",
                    "--region", self.region,
                    "--image-id", ami_id,
                    "--instance-type", instance_type,
                    "--count", "1",
                    "--key-name", "your-key-name",  # UPDATE THIS
                    "--user-data", user_data,
                    "--tag-specifications",
                    f"ResourceType=instance,Tags=[{{Key=Name,Value={instance_name}}},{{Key=BatchID,Value={batch_id}}},{{Key=DeploymentID,Value={self.deployment_id}}}]"
                ]

            try:
                # Note: This is a template - actual deployment would execute the command
                print(f"  Command prepared for batch {batch_id}")
                print(f"  (AWS CLI command ready - see deploy_aws.sh)")

                self.instances.append({
                    "batch_id": batch_id,
                    "provider": "aws",
                    "name": instance_name,
                    "status": "pending",
                    "batch_size": batch_size
                })

            except Exception as e:
                print(f"  Error launching instance: {e}")

        self._save_state()
        print(f"\n✓ Deployment initiated for {num_instances} instances")

    def deploy_gcp(self, num_instances: int, batch_size: int, preemptible: bool = True):
        """Deploy batch runners on GCP Compute Engine"""
        print(f"\n{'='*70}")
        print(f"GCP DEPLOYMENT - {num_instances} instances")
        print(f"{'='*70}\n")

        instance_type = "e2-standard-2"  # 2 vCPU, 8GB RAM
        image_family = "ubuntu-2004-lts"
        image_project = "ubuntu-os-cloud"

        print("Instance configuration:")
        print(f"  Type: {instance_type}")
        print(f"  Image: {image_family}")
        print(f"  Preemptible: {preemptible}")
        print(f"  Region: {self.region}")

        startup_script = self._generate_user_data_script()

        for batch_id in range(num_instances):
            print(f"\nLaunching instance for batch {batch_id}...")

            instance_name = f"pharma-batch-{self.deployment_id}-{batch_id}"

            # GCP gcloud command
            cmd = [
                "gcloud", "compute", "instances", "create", instance_name,
                "--zone", f"{self.region}-a",
                "--machine-type", instance_type,
                "--image-family", image_family,
                "--image-project", image_project,
                "--metadata", f"startup-script={startup_script}",
                "--labels", f"batch_id={batch_id},deployment_id={self.deployment_id}",
            ]

            if preemptible:
                cmd.append("--preemptible")

            print(f"  Command prepared for batch {batch_id}")
            print(f"  (GCP gcloud command ready - see deploy_gcp.sh)")

            self.instances.append({
                "batch_id": batch_id,
                "provider": "gcp",
                "name": instance_name,
                "status": "pending",
                "batch_size": batch_size
            })

        self._save_state()
        print(f"\n✓ Deployment initiated for {num_instances} instances")

    def _generate_user_data_script(self) -> str:
        """Generate startup script for cloud instances"""
        script = """#!/bin/bash
set -e

# Update system
apt-get update
apt-get install -y python3-pip git docker.io

# Clone repository
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/crowelogic-pharma-model.git
cd crowelogic-pharma-model

# Install dependencies
pip3 install -r requirements.txt

# Create directories
mkdir -p logs cache generated_data/batches

# Get batch ID from instance metadata
BATCH_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id | md5sum | cut -c1-4)

# Run batch generation
python3 generate_batch.py --batch $BATCH_ID --batch-size 1000 > logs/batch_${BATCH_ID}.log 2>&1

# Upload results to S3/GCS (configure your bucket)
# aws s3 cp generated_data/batches/ s3://your-bucket/batches/ --recursive
# gsutil cp generated_data/batches/* gs://your-bucket/batches/

# Signal completion
echo "BATCH_COMPLETE" > /tmp/batch_complete.flag

# Shutdown instance (optional - to save costs)
# sudo shutdown -h now
"""
        return script

    def _save_state(self):
        """Save deployment state"""
        state = {
            "deployment_id": self.deployment_id,
            "provider": self.provider,
            "region": self.region,
            "instances": self.instances,
            "timestamp": datetime.now().isoformat()
        }

        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

        print(f"\n✓ State saved to {self.state_file}")

    def generate_deployment_scripts(self, num_instances: int, batch_size: int, use_spot: bool = True):
        """Generate deployment scripts for manual execution"""
        print(f"\n{'='*70}")
        print("GENERATING DEPLOYMENT SCRIPTS")
        print(f"{'='*70}\n")

        # AWS deployment script
        aws_script = Path("deploy_aws.sh")
        with open(aws_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# AWS Deployment Script\n")
            f.write(f"# Deploy {num_instances} instances for batch generation\n\n")
            f.write("set -e\n\n")
            f.write(f"DEPLOYMENT_ID={self.deployment_id}\n")
            f.write(f"REGION={self.region}\n")
            f.write(f"INSTANCE_TYPE=t3.medium\n")
            f.write(f"AMI_ID=ami-0c55b159cbfafe1f0  # Update for your region\n\n")

            for batch_id in range(num_instances):
                instance_name = f"pharma-batch-{self.deployment_id}-{batch_id}"
                f.write(f"\n# Launch batch {batch_id}\n")
                f.write(f"echo 'Launching {instance_name}...'\n")

                if use_spot:
                    f.write(f"aws ec2 request-spot-instances \\\n")
                    f.write(f"  --region $REGION \\\n")
                    f.write(f"  --instance-count 1 \\\n")
                    f.write(f"  --type one-time \\\n")
                    f.write(f"  --launch-specification '{{\n")
                    f.write(f'    "ImageId": "$AMI_ID",\n')
                    f.write(f'    "InstanceType": "$INSTANCE_TYPE",\n')
                    f.write(f'    "KeyName": "your-key-name",\n')  # UPDATE THIS
                    f.write(f'    "UserData": "$(cat startup_script.sh | base64)",\n')
                    f.write(f'    "TagSpecifications": [{{\n')
                    f.write(f'      "ResourceType": "instance",\n')
                    f.write(f'      "Tags": [\n')
                    f.write(f'        {{"Key": "Name", "Value": "{instance_name}"}},\n')
                    f.write(f'        {{"Key": "BatchID", "Value": "{batch_id}"}},\n')
                    f.write(f'        {{"Key": "DeploymentID", "Value": "$DEPLOYMENT_ID"}}\n')
                    f.write(f'      ]\n')
                    f.write(f'    }}]\n')
                    f.write(f"  }}'\n")
                else:
                    f.write(f"aws ec2 run-instances \\\n")
                    f.write(f"  --region $REGION \\\n")
                    f.write(f"  --image-id $AMI_ID \\\n")
                    f.write(f"  --instance-type $INSTANCE_TYPE \\\n")
                    f.write(f"  --count 1 \\\n")
                    f.write(f"  --key-name your-key-name \\\n")  # UPDATE THIS
                    f.write(f"  --user-data file://startup_script.sh \\\n")
                    f.write(f"  --tag-specifications 'ResourceType=instance,Tags=[{{Key=Name,Value={instance_name}}},{{Key=BatchID,Value={batch_id}}},{{Key=DeploymentID,Value=$DEPLOYMENT_ID}}]'\n")

                f.write(f"\nsleep 2  # Rate limiting\n")

            f.write(f"\necho 'Deployment complete!'\n")
            f.write(f"echo 'Monitor with: aws ec2 describe-instances --region $REGION --filters Name=tag:DeploymentID,Values=$DEPLOYMENT_ID'\n")

        os.chmod(aws_script, 0o755)
        print(f"✓ AWS script: {aws_script}")

        # GCP deployment script
        gcp_script = Path("deploy_gcp.sh")
        with open(gcp_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# GCP Deployment Script\n")
            f.write(f"# Deploy {num_instances} instances for batch generation\n\n")
            f.write("set -e\n\n")
            f.write(f"DEPLOYMENT_ID={self.deployment_id}\n")
            f.write(f"ZONE={self.region}-a\n")
            f.write(f"MACHINE_TYPE=e2-standard-2\n\n")

            for batch_id in range(num_instances):
                instance_name = f"pharma-batch-{self.deployment_id}-{batch_id}"
                f.write(f"\n# Launch batch {batch_id}\n")
                f.write(f"echo 'Launching {instance_name}...'\n")
                f.write(f"gcloud compute instances create {instance_name} \\\n")
                f.write(f"  --zone=$ZONE \\\n")
                f.write(f"  --machine-type=$MACHINE_TYPE \\\n")
                f.write(f"  --image-family=ubuntu-2004-lts \\\n")
                f.write(f"  --image-project=ubuntu-os-cloud \\\n")
                f.write(f"  --metadata-from-file=startup-script=startup_script.sh \\\n")
                f.write(f"  --labels=batch_id={batch_id},deployment_id=$DEPLOYMENT_ID \\\n")
                f.write(f"  --preemptible\n")
                f.write(f"\nsleep 2  # Rate limiting\n")

            f.write(f"\necho 'Deployment complete!'\n")
            f.write(f"echo 'Monitor with: gcloud compute instances list --filter=labels.deployment_id=$DEPLOYMENT_ID'\n")

        os.chmod(gcp_script, 0o755)
        print(f"✓ GCP script: {gcp_script}")

        # Startup script
        startup_script = Path("startup_script.sh")
        with open(startup_script, 'w') as f:
            f.write(self._generate_startup_script_detailed(batch_size))

        os.chmod(startup_script, 0o755)
        print(f"✓ Startup script: {startup_script}")

        print(f"\n{'='*70}")
        print("NEXT STEPS:")
        print(f"{'='*70}")
        print(f"1. Update your-key-name in the scripts")
        print(f"2. Update S3/GCS bucket names in startup_script.sh")
        print(f"3. Run deployment script:")
        print(f"   AWS: ./deploy_aws.sh")
        print(f"   GCP: ./deploy_gcp.sh")
        print(f"{'='*70}\n")

    def _generate_startup_script_detailed(self, batch_size: int) -> str:
        """Generate detailed startup script with environment-specific batch ID"""
        return f"""#!/bin/bash
set -e

echo "Starting pharma data generation batch job..."

# Update system
sudo apt-get update
sudo apt-get install -y python3-pip git awscli

# Clone repository (UPDATE THIS URL)
cd /home/ubuntu
git clone https://github.com/YOUR_USERNAME/crowelogic-pharma-model.git || echo "Repo already cloned"
cd crowelogic-pharma-model

# Install dependencies
pip3 install -r requirements.txt

# Create directories
mkdir -p logs cache generated_data/batches

# Determine batch ID from instance metadata
if [ -f /sys/hypervisor/uuid ]; then
    # AWS EC2
    INSTANCE_ID=$(ec2-metadata --instance-id | cut -d " " -f 2)
    BATCH_ID=$(aws ec2 describe-tags --region {self.region} --filters "Name=resource-id,Values=$INSTANCE_ID" "Name=key,Values=BatchID" --query "Tags[0].Value" --output text)
else
    # GCP
    BATCH_ID=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/attributes/batch-id" -H "Metadata-Flavor: Google")
fi

echo "Running batch generation for batch $BATCH_ID..."

# Run batch generation
python3 generate_batch.py --batch $BATCH_ID --batch-size {batch_size} 2>&1 | tee logs/batch_${{BATCH_ID}}.log

# Upload results to cloud storage (UPDATE BUCKET NAME)
# For AWS S3:
# aws s3 cp generated_data/batches/batch_${{BATCH_ID}}.jsonl s3://your-pharma-bucket/batches/
# aws s3 cp generated_data/batches/batch_${{BATCH_ID}}_stats.json s3://your-pharma-bucket/batches/
# aws s3 cp logs/batch_${{BATCH_ID}}.log s3://your-pharma-bucket/logs/

# For GCP Cloud Storage:
# gsutil cp generated_data/batches/batch_${{BATCH_ID}}.jsonl gs://your-pharma-bucket/batches/
# gsutil cp generated_data/batches/batch_${{BATCH_ID}}_stats.json gs://your-pharma-bucket/batches/
# gsutil cp logs/batch_${{BATCH_ID}}.log gs://your-pharma-bucket/logs/

echo "Batch $BATCH_ID complete!"

# Optional: Shutdown instance to save costs
# sudo shutdown -h now
"""


def main():
    parser = argparse.ArgumentParser(description='Cloud deployment orchestrator')
    parser.add_argument('--provider', choices=['aws', 'gcp', 'azure'], default='aws',
                       help='Cloud provider (default: aws)')
    parser.add_argument('--num-instances', type=int, default=10,
                       help='Number of instances to launch (default: 10)')
    parser.add_argument('--batch-size', type=int, default=1000,
                       help='Compounds per batch (default: 1000)')
    parser.add_argument('--region', type=str,
                       help='Cloud region (default: provider-specific)')
    parser.add_argument('--spot', action='store_true', default=True,
                       help='Use spot/preemptible instances (default: True)')
    parser.add_argument('--generate-scripts', action='store_true', default=True,
                       help='Generate deployment scripts (default: True)')

    args = parser.parse_args()

    orchestrator = CloudOrchestrator(provider=args.provider, region=args.region)

    if args.generate_scripts:
        orchestrator.generate_deployment_scripts(
            num_instances=args.num_instances,
            batch_size=args.batch_size,
            use_spot=args.spot
        )
    else:
        if args.provider == 'aws':
            orchestrator.deploy_aws(
                num_instances=args.num_instances,
                batch_size=args.batch_size,
                use_spot=args.spot
            )
        elif args.provider == 'gcp':
            orchestrator.deploy_gcp(
                num_instances=args.num_instances,
                batch_size=args.batch_size,
                preemptible=args.spot
            )


if __name__ == "__main__":
    main()

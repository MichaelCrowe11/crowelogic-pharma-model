#!/usr/bin/env python3
"""
Azure Deployment Script for CroweLogic-Pharma
Deploys pharmaceutical AI model to Azure Container Instances or Azure ML
"""

import os
import sys
import json
import argparse
from pathlib import Path

class AzureDeployer:
    def __init__(self, deployment_type="aci"):
        self.deployment_type = deployment_type
        self.config = self.load_config()

    def load_config(self):
        """Load deployment configuration"""
        config_file = Path("azure_deployment/deployment_config.json")

        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            return self.create_default_config()

    def create_default_config(self):
        """Create default deployment configuration"""
        return {
            "subscription_id": "<your-subscription-id>",
            "resource_group": "crowelogic-pharma-rg",
            "location": "eastus",
            "acr_name": "crowelogicpharmaacr",
            "aci_name": "crowelogic-pharma-aci",
            "model_name": "CroweLogic-Pharma",
            "model_version": "latest",
            "compute": {
                "cpu": 4,
                "memory_gb": 16,
                "gpu_count": 0
            }
        }

    def save_config(self):
        """Save deployment configuration"""
        config_file = Path("azure_deployment/deployment_config.json")
        config_file.parent.mkdir(exist_ok=True)

        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

        print(f"✓ Configuration saved to {config_file}")

    def check_azure_cli(self):
        """Check if Azure CLI is installed"""
        import subprocess

        try:
            result = subprocess.run(
                ["az", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print("✓ Azure CLI found")
            return True
        except FileNotFoundError:
            print("⚠ Azure CLI not found")
            print("  Install from: https://docs.microsoft.com/cli/azure/install-azure-cli")
            return False

    def login_azure(self):
        """Login to Azure"""
        import subprocess

        print("\n=== Azure Login ===\n")
        print("Opening browser for authentication...")

        try:
            subprocess.run(["az", "login"], check=True)
            print("✓ Successfully logged in to Azure")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to login to Azure")
            return False

    def create_resource_group(self):
        """Create Azure resource group"""
        import subprocess

        print(f"\n=== Creating Resource Group ===\n")
        print(f"Name: {self.config['resource_group']}")
        print(f"Location: {self.config['location']}")

        cmd = [
            "az", "group", "create",
            "--name", self.config['resource_group'],
            "--location", self.config['location']
        ]

        try:
            subprocess.run(cmd, check=True)
            print("✓ Resource group created")
            return True
        except subprocess.CalledProcessError:
            print("⚠ Resource group may already exist")
            return True

    def create_container_registry(self):
        """Create Azure Container Registry"""
        import subprocess

        print(f"\n=== Creating Container Registry ===\n")
        print(f"Name: {self.config['acr_name']}")

        cmd = [
            "az", "acr", "create",
            "--resource-group", self.config['resource_group'],
            "--name", self.config['acr_name'],
            "--sku", "Basic"
        ]

        try:
            subprocess.run(cmd, check=True)
            print("✓ Container registry created")
            return True
        except subprocess.CalledProcessError:
            print("⚠ Container registry may already exist")
            return True

    def build_and_push_image(self):
        """Build Docker image and push to ACR"""
        import subprocess

        print(f"\n=== Building and Pushing Docker Image ===\n")

        # Login to ACR
        print("Logging in to ACR...")
        login_cmd = [
            "az", "acr", "login",
            "--name", self.config['acr_name']
        ]

        try:
            subprocess.run(login_cmd, check=True)
        except subprocess.CalledProcessError:
            print("✗ Failed to login to ACR")
            return False

        # Build image
        image_name = f"{self.config['acr_name']}.azurecr.io/crowelogic-pharma:latest"
        print(f"Building image: {image_name}")

        build_cmd = [
            "az", "acr", "build",
            "--registry", self.config['acr_name'],
            "--image", "crowelogic-pharma:latest",
            "--file", "azure_deployment/Dockerfile",
            "."
        ]

        try:
            subprocess.run(build_cmd, check=True)
            print("✓ Image built and pushed to ACR")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to build image")
            return False

    def deploy_to_aci(self):
        """Deploy to Azure Container Instances"""
        import subprocess

        print(f"\n=== Deploying to Azure Container Instances ===\n")

        # Update YAML with ACR name
        yaml_file = Path("azure_deployment/azure-container-instance.yaml")
        with open(yaml_file, 'r') as f:
            yaml_content = f.read()

        yaml_content = yaml_content.replace(
            "<your-acr-name>",
            self.config['acr_name']
        )

        # Write updated YAML
        updated_yaml = Path("azure_deployment/azure-container-instance-updated.yaml")
        with open(updated_yaml, 'w') as f:
            f.write(yaml_content)

        # Deploy
        cmd = [
            "az", "container", "create",
            "--resource-group", self.config['resource_group'],
            "--file", str(updated_yaml)
        ]

        try:
            subprocess.run(cmd, check=True)
            print("✓ Deployed to Azure Container Instances")

            # Get endpoint
            endpoint_cmd = [
                "az", "container", "show",
                "--resource-group", self.config['resource_group'],
                "--name", self.config['aci_name'],
                "--query", "ipAddress.fqdn",
                "--output", "tsv"
            ]

            result = subprocess.run(endpoint_cmd, capture_output=True, text=True, check=True)
            endpoint = result.stdout.strip()

            print(f"\n=== Deployment Complete ===")
            print(f"Endpoint: http://{endpoint}:11434")
            print(f"API Endpoint: http://{endpoint}:8000")

            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to deploy to ACI")
            return False

    def deploy_to_azure_ml(self):
        """Deploy to Azure Machine Learning"""
        try:
            from azure.ai.ml import MLClient
            from azure.identity import DefaultAzureCredential
            from azure.ai.ml.entities import Environment

            print(f"\n=== Deploying to Azure Machine Learning ===\n")

            # Create ML client
            credential = DefaultAzureCredential()
            ml_client = MLClient(
                credential=credential,
                subscription_id=self.config['subscription_id'],
                resource_group_name=self.config['resource_group']
            )

            # Create environment
            env_config = Path("azure_deployment/azure-ml-config.yaml")
            env = Environment(
                name="crowelogic-pharma-env",
                description="CroweLogic-Pharma pharmaceutical AI environment",
                conda_file=env_config
            )

            ml_client.environments.create_or_update(env)
            print("✓ Environment created in Azure ML")

            print("\n=== Azure ML Deployment Complete ===")
            print("Next steps:")
            print("1. Navigate to Azure ML Studio")
            print("2. Create a compute instance or cluster")
            print("3. Deploy the model as an online endpoint")

            return True

        except ImportError:
            print("⚠ Azure ML SDK not installed")
            print("  Install with: pip install azure-ai-ml azure-identity")
            return False
        except Exception as e:
            print(f"✗ Error deploying to Azure ML: {e}")
            return False

    def run_deployment(self):
        """Run complete deployment pipeline"""
        print("=" * 70)
        print("CroweLogic-Pharma Azure Deployment")
        print("=" * 70)

        # Check prerequisites
        if not self.check_azure_cli():
            return False

        # Save configuration
        self.save_config()

        # Login
        if not self.login_azure():
            return False

        # Create resources
        if not self.create_resource_group():
            return False

        # Deploy based on type
        if self.deployment_type == "aci":
            if not self.create_container_registry():
                return False

            if not self.build_and_push_image():
                return False

            if not self.deploy_to_aci():
                return False

        elif self.deployment_type == "azureml":
            if not self.deploy_to_azure_ml():
                return False

        else:
            print(f"✗ Unknown deployment type: {self.deployment_type}")
            return False

        print("\n" + "=" * 70)
        print("Deployment Complete!")
        print("=" * 70)

        return True

def main():
    parser = argparse.ArgumentParser(
        description="Deploy CroweLogic-Pharma to Azure"
    )
    parser.add_argument(
        "--type",
        choices=["aci", "azureml"],
        default="aci",
        help="Deployment type (default: aci)"
    )
    parser.add_argument(
        "--config",
        action="store_true",
        help="Only create configuration file"
    )

    args = parser.parse_args()

    deployer = AzureDeployer(deployment_type=args.type)

    if args.config:
        deployer.save_config()
        print("\nConfiguration created. Please edit deployment_config.json with your Azure details.")
    else:
        deployer.run_deployment()

if __name__ == "__main__":
    main()

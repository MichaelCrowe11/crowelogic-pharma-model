#!/usr/bin/env python3
"""
Deploy CroweLogic-Pharma to Paperspace Gradient with GPU
Uses Paperspace API directly for deployment
"""

import os
import sys
import json
import time
import requests

def paperspace_deploy():
    print("🚀 CroweLogic-Pharma Paperspace GPU Deployment")
    print("=" * 60)
    print()

    # Get API key
    api_key = os.getenv("PAPERSPACE_API_KEY")

    if not api_key:
        print("❌ PAPERSPACE_API_KEY not found!")
        print()
        print("Steps to get your API key:")
        print("1. Go to: https://console.paperspace.com/account/user")
        print("2. Click 'API Keys' tab")
        print("3. Create new API key")
        print("4. Set it: export PAPERSPACE_API_KEY='your-key'")
        print()
        print("Or pass it as argument:")
        print(f"  python {sys.argv[0]} YOUR_API_KEY")
        print()

        if len(sys.argv) > 1:
            api_key = sys.argv[1]
            print(f"✅ Using API key from argument")
        else:
            sys.exit(1)

    print("✅ API key found")
    print()

    # Deployment configuration
    deployment_config = {
        "name": "crowelogic-pharma",
        "image": "ollama/ollama:latest",
        "port": 11434,
        "resources": {
            "replicas": 1,
            "instanceType": "P4000"  # GPU instance
        },
        "env": {
            "OLLAMA_HOST": "0.0.0.0:11434"
        },
        "command": [
            "sh", "-c",
            """
            ollama serve &
            sleep 20 &&
            ollama pull llama3.2:latest &&
            curl -sL https://raw.githubusercontent.com/MichaelCrowe11/crowelogic-pharma-model/master/models/CroweLogicPharmaModelfile-practical -o /tmp/modelfile &&
            ollama create CroweLogic-Pharma:latest -f /tmp/modelfile &&
            echo 'Model ready!' &&
            tail -f /dev/null
            """
        ]
    }

    print("📋 Deployment Configuration:")
    print(f"  Name: {deployment_config['name']}")
    print(f"  GPU: {deployment_config['resources']['instanceType']}")
    print(f"  Port: {deployment_config['port']}")
    print()

    print("⚠️  Note: Paperspace Gradient API requires project ID")
    print("The easiest way to deploy is via their web interface:")
    print()
    print("🌐 Web Deployment (Recommended):")
    print("-" * 60)
    print("1. Go to: https://console.paperspace.com/gradient/deployments")
    print("2. Click 'Create Deployment'")
    print()
    print("Fill in:")
    print("  - Name: crowelogic-pharma")
    print("  - Machine: P4000 (GPU, $0.51/hr)")
    print("  - Image: ollama/ollama:latest")
    print("  - Port: 11434")
    print("  - Command:")
    print('    sh -c "ollama serve & sleep 20 && ollama pull llama3.2:latest && curl -sL https://raw.githubusercontent.com/MichaelCrowe11/crowelogic-pharma-model/master/models/CroweLogicPharmaModelfile-practical -o /tmp/modelfile && ollama create CroweLogic-Pharma:latest -f /tmp/modelfile && tail -f /dev/null"')
    print()
    print("3. Click 'Deploy'")
    print()
    print("-" * 60)
    print()

    print("🎨 Alternative: Use Free GPU Notebook")
    print("-" * 60)
    print("1. Go to: https://console.paperspace.com/gradient/notebooks")
    print("2. Create Notebook → Select 'Free-GPU'")
    print("3. In terminal, run:")
    print()
    print("   curl -fsSL https://ollama.com/install.sh | sh")
    print("   nohup ollama serve > ollama.log 2>&1 &")
    print("   sleep 15")
    print("   git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git")
    print("   cd crowelogic-pharma-model")
    print("   ollama pull llama3.2:latest")
    print("   ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile-practical")
    print()
    print("This gives you FREE GPU for testing!")
    print("-" * 60)
    print()

    # Save config for reference
    config_file = "paperspace_deployment_config.json"
    with open(config_file, "w") as f:
        json.dump(deployment_config, f, indent=2)

    print(f"✅ Configuration saved to: {config_file}")
    print()
    print("💡 For larger models (33B-70B), use these GPU options:")
    print("  - P4000: 8GB VRAM - Good for up to 13B models")
    print("  - P5000: 16GB VRAM - Good for up to 33B models")
    print("  - P6000: 24GB VRAM - Good for up to 70B models")
    print()

if __name__ == "__main__":
    paperspace_deploy()

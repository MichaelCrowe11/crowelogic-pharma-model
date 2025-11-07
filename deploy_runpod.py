#!/usr/bin/env python3
"""
CroweLogic-Pharma RunPod Deployment Script

RunPod is the easiest and cheapest option for GPU deployments.
This script helps you deploy via their API.
"""

import os
import json
import requests
import time
from typing import Optional

class RunPodDeployer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("RUNPOD_API_KEY")
        if not self.api_key:
            print("❌ RunPod API key not found!")
            print("\n1. Get your API key from: https://runpod.io/console/user/settings")
            print("2. Set it: export RUNPOD_API_KEY='your-key-here'")
            print("3. Or pass it to the script\n")
            exit(1)

        self.base_url = "https://api.runpod.io/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def query(self, query: str, variables: dict = None):
        """Execute GraphQL query"""
        response = requests.post(
            self.base_url,
            headers=self.headers,
            json={"query": query, "variables": variables}
        )
        return response.json()

    def get_gpu_types(self):
        """List available GPU types"""
        query = """
        query {
            gpuTypes {
                id
                displayName
                memoryInGb
                securePrice
                communityPrice
            }
        }
        """
        result = self.query(query)
        return result.get("data", {}).get("gpuTypes", [])

    def create_pod(self, name: str, gpu_type: str = "NVIDIA RTX 4000", docker_image: str = None):
        """Create a new pod"""

        # Default to Ollama template
        if not docker_image:
            docker_image = "ollama/ollama:latest"

        query = """
        mutation CreatePod($input: PodInput!) {
            podFindAndDeployOnDemand(input: $input) {
                id
                desiredStatus
                imageName
                machineId
                machine {
                    podHostId
                }
            }
        }
        """

        variables = {
            "input": {
                "cloudType": "COMMUNITY",
                "gpuTypeId": gpu_type,
                "name": name,
                "imageName": docker_image,
                "dockerArgs": "",
                "containerDiskInGb": 50,
                "volumeInGb": 0,
                "ports": "11434/http",
                "env": [
                    {"key": "OLLAMA_HOST", "value": "0.0.0.0:11434"}
                ]
            }
        }

        result = self.query(query, variables)
        return result

    def get_pod(self, pod_id: str):
        """Get pod details"""
        query = """
        query Pod($input: PodFilter!) {
            pod(input: $input) {
                id
                name
                runtime {
                    uptimeInSeconds
                    ports {
                        ip
                        isIpPublic
                        privatePort
                        publicPort
                        type
                    }
                }
            }
        }
        """
        variables = {"input": {"podId": pod_id}}
        result = self.query(query, variables)
        return result.get("data", {}).get("pod")

    def stop_pod(self, pod_id: str):
        """Stop a pod"""
        query = """
        mutation StopPod($input: PodStopInput!) {
            podStop(input: $input) {
                id
                desiredStatus
            }
        }
        """
        variables = {"input": {"podId": pod_id}}
        return self.query(query, variables)


def main():
    print("🚀 CroweLogic-Pharma RunPod Deployment")
    print("=" * 60)
    print()

    # Initialize deployer
    deployer = RunPodDeployer()

    # Show available GPUs
    print("📊 Available GPU Types:")
    print("-" * 60)
    gpus = deployer.get_gpu_types()

    affordable_gpus = [
        g for g in gpus
        if g.get("communityPrice", 999) < 0.5  # Under $0.50/hr
    ]

    for i, gpu in enumerate(affordable_gpus[:5], 1):
        price = gpu.get("communityPrice", gpu.get("securePrice", 0))
        print(f"{i}. {gpu['displayName']}")
        print(f"   Memory: {gpu['memoryInGb']} GB")
        print(f"   Price: ${price}/hr (~${price * 730:.0f}/month)")
        print()

    # Choose GPU
    print("💡 Recommended: RTX 4000 (Good balance of price/performance)")
    gpu_choice = input("Choose GPU (1-5) or press Enter for RTX 4000: ").strip()

    if gpu_choice and gpu_choice.isdigit():
        selected_gpu = affordable_gpus[int(gpu_choice) - 1]["id"]
    else:
        selected_gpu = "NVIDIA RTX 4000"

    print(f"\n✅ Selected: {selected_gpu}")
    print()

    # Create pod
    print("🔨 Creating pod...")
    result = deployer.create_pod(
        name="crowelogic-pharma",
        gpu_type=selected_gpu
    )

    if "errors" in result:
        print(f"❌ Error: {result['errors']}")
        return

    pod_data = result.get("data", {}).get("podFindAndDeployOnDemand")
    if not pod_data:
        print("❌ Failed to create pod")
        print(json.dumps(result, indent=2))
        return

    pod_id = pod_data["id"]
    print(f"✅ Pod created: {pod_id}")
    print()

    # Wait for pod to start
    print("⏳ Waiting for pod to start (this may take 1-2 minutes)...")
    for i in range(30):
        time.sleep(4)
        pod = deployer.get_pod(pod_id)

        if pod and pod.get("runtime"):
            runtime = pod["runtime"]
            ports = runtime.get("ports", [])

            if ports:
                print("\n✅ Pod is running!")
                print("-" * 60)

                # Find the public endpoint
                for port in ports:
                    if port.get("publicPort") == 11434:
                        ip = port.get("ip")
                        public_port = port.get("publicPort")
                        endpoint = f"http://{ip}:{public_port}"

                        print(f"🌐 Endpoint: {endpoint}")
                        print()
                        print("📝 Next steps:")
                        print()
                        print("1. SSH into your pod (get SSH command from RunPod console)")
                        print()
                        print("2. Setup CroweLogic-Pharma:")
                        print("   git clone https://github.com/MichaelCrowe11/crowelogic-pharma-model.git")
                        print("   cd crowelogic-pharma-model")
                        print("   ollama pull llama3.2:latest")
                        print("   ollama create CroweLogic-Pharma:latest -f models/CroweLogicPharmaModelfile-practical")
                        print()
                        print("3. Test your model:")
                        print(f"   curl -X POST {endpoint}/api/generate \\")
                        print('     -d \'{"model":"CroweLogic-Pharma:latest","prompt":"What are hericenones?"}\'')
                        print()
                        print("💰 Cost tracking:")
                        print(f"   - Running time: {runtime.get('uptimeInSeconds', 0) // 60} minutes")
                        print("   - Stop pod when not in use to save money!")
                        print(f"   - Stop command: python {__file__} --stop {pod_id}")
                        print()

                        # Save pod info
                        with open("runpod_deployment.json", "w") as f:
                            json.dump({
                                "pod_id": pod_id,
                                "endpoint": endpoint,
                                "gpu_type": selected_gpu,
                                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
                            }, f, indent=2)

                        print("✅ Deployment info saved to: runpod_deployment.json")
                        return

        print(".", end="", flush=True)

    print("\n⚠️  Pod is taking longer than expected to start.")
    print("Check status at: https://runpod.io/console/pods")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--stop" and len(sys.argv) > 2:
        pod_id = sys.argv[2]
        deployer = RunPodDeployer()
        print(f"🛑 Stopping pod: {pod_id}")
        result = deployer.stop_pod(pod_id)
        print("✅ Pod stopped")
    else:
        main()

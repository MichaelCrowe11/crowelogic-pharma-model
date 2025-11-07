#!/usr/bin/env python3
"""
Test script for deployed CroweLogic-Pharma model on Azure
"""

import requests
import json
import time
import sys

class DeploymentTester:
    def __init__(self, endpoint_url):
        """
        Initialize tester with Azure endpoint URL
        Args:
            endpoint_url: Full URL like http://your-endpoint.azurecontainer.io:11434
        """
        self.endpoint_url = endpoint_url.rstrip('/')
        self.api_url = f"{self.endpoint_url}/api/generate"

    def test_connectivity(self):
        """Test if the endpoint is reachable"""
        print("\n🔍 Testing connectivity...")
        try:
            response = requests.get(self.endpoint_url, timeout=10)
            print(f"✓ Endpoint is reachable (Status: {response.status_code})")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection failed: {e}")
            return False

    def query_model(self, prompt, stream=False):
        """Query the deployed model"""
        print(f"\n📤 Sending query: {prompt[:50]}...")

        payload = {
            "model": "CroweLogic-Pharma:latest",
            "prompt": prompt,
            "stream": stream
        }

        try:
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                print(f"✗ Request failed with status {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"✗ Request error: {e}")
            return None

    def run_test_suite(self):
        """Run complete test suite"""
        print("=" * 70)
        print("CroweLogic-Pharma Deployment Test Suite")
        print("=" * 70)
        print(f"Endpoint: {self.endpoint_url}")

        # Test 1: Connectivity
        if not self.test_connectivity():
            print("\n❌ Connectivity test failed. Deployment may not be ready.")
            return False

        # Test 2: Pharmaceutical Knowledge
        print("\n" + "=" * 70)
        print("TEST 1: Pharmaceutical Knowledge")
        print("=" * 70)

        response = self.query_model(
            "What are the key ADME properties to consider in drug development?"
        )

        if response:
            print("✓ Response received:")
            print(f"  {response[:200]}...")
        else:
            print("✗ Test 1 failed")
            return False

        time.sleep(2)

        # Test 3: Mushroom Expertise
        print("\n" + "=" * 70)
        print("TEST 2: Mycopharmacology Expertise")
        print("=" * 70)

        response = self.query_model(
            "Explain the neuroprotective mechanisms of hericenones from Lion's Mane mushroom."
        )

        if response:
            print("✓ Response received:")
            print(f"  {response[:200]}...")
        else:
            print("✗ Test 2 failed")
            return False

        time.sleep(2)

        # Test 4: ChEMBL Integration
        print("\n" + "=" * 70)
        print("TEST 3: ChEMBL Knowledge")
        print("=" * 70)

        response = self.query_model(
            "How do you interpret IC50 values in drug screening?"
        )

        if response:
            print("✓ Response received:")
            print(f"  {response[:200]}...")
        else:
            print("✗ Test 3 failed")
            return False

        time.sleep(2)

        # Test 5: Quantum Chemistry
        print("\n" + "=" * 70)
        print("TEST 4: Quantum Chemistry Integration")
        print("=" * 70)

        response = self.query_model(
            "What is HOMO-LUMO gap and why is it important in drug design?"
        )

        if response:
            print("✓ Response received:")
            print(f"  {response[:200]}...")
        else:
            print("✗ Test 4 failed")
            return False

        print("\n" + "=" * 70)
        print("✅ All tests passed!")
        print("=" * 70)
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_deployment.py <endpoint_url>")
        print("Example: python test_deployment.py http://crowelogic-pharma.eastus.azurecontainer.io:11434")
        sys.exit(1)

    endpoint = sys.argv[1]
    tester = DeploymentTester(endpoint)

    success = tester.run_test_suite()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script for CroweLogic-Pharma Pro (70b) deployment
Compares performance against the standard model
"""

import requests
import json
import time
import sys

class Pharma70bTester:
    def __init__(self, pro_endpoint, standard_endpoint=None):
        """
        Args:
            pro_endpoint: URL for 70b model (e.g., http://crowelogic-pharma-pro.eastus.azurecontainer.io:11434)
            standard_endpoint: Optional URL for standard model comparison
        """
        self.pro_endpoint = pro_endpoint.rstrip('/')
        self.standard_endpoint = standard_endpoint.rstrip('/') if standard_endpoint else None

    def query_model(self, endpoint, model_name, prompt):
        """Query a model and return response with timing"""
        url = f"{endpoint}/api/generate"

        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }

        start_time = time.time()
        try:
            response = requests.post(url, json=payload, timeout=300)
            elapsed = time.time() - start_time

            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "response": result.get('response', ''),
                    "elapsed": elapsed,
                    "eval_count": result.get('eval_count', 0),
                    "prompt_eval_count": result.get('prompt_eval_count', 0)
                }
            else:
                return {
                    "success": False,
                    "error": response.text,
                    "elapsed": elapsed
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "elapsed": time.time() - start_time
            }

    def run_advanced_tests(self):
        """Run tests that showcase 70b capabilities"""

        print("=" * 80)
        print("CroweLogic-Pharma Pro (70b) Advanced Test Suite")
        print("=" * 80)
        print(f"Pro Endpoint: {self.pro_endpoint}")
        if self.standard_endpoint:
            print(f"Standard Endpoint: {self.standard_endpoint}")
        print("")

        tests = [
            {
                "name": "Complex SAR Analysis",
                "prompt": """Analyze the structure-activity relationship of hericenone derivatives for NGF stimulation.
                Consider: 1) Key pharmacophore elements, 2) Effects of aromatic substitutions on potency,
                3) Impact of side chain modifications on BBB permeability, 4) Optimal LogP range for CNS penetration,
                5) Predicted metabolic liabilities and propose 3 optimized analogs with rationale."""
            },
            {
                "name": "Clinical Trial Design",
                "prompt": """Design a Phase II clinical trial for a novel hericenone-based drug targeting Alzheimer's disease.
                Include: 1) Patient inclusion/exclusion criteria with biomarker stratification, 2) Dosing regimen with PK/PD rationale,
                3) Primary and secondary endpoints, 4) Sample size calculation assuming 30% treatment effect,
                5) Adaptive design features, 6) Regulatory considerations for FDA Fast Track designation."""
            },
            {
                "name": "Multi-Target Polypharmacology",
                "prompt": """Evaluate the polypharmacology profile of ganoderic acid DM for cancer therapy.
                Analyze: 1) Known molecular targets (kinases, receptors, enzymes), 2) On-target vs off-target effects,
                3) Synergistic combinations with checkpoint inhibitors, 4) Resistance mechanisms and biomarkers,
                5) Therapeutic window optimization, 6) Clinical development strategy."""
            },
            {
                "name": "ADME-Tox Prediction",
                "prompt": """Predict the ADME-Tox profile for a novel psilocybin analog (4-HO-DET) as a rapid-acting antidepressant.
                Provide: 1) CYP metabolism predictions (isoforms, metabolites), 2) hERG liability assessment,
                3) BBB penetration (PSA, efflux considerations), 4) Half-life estimation, 5) Hepatotoxicity risk,
                6) Recommended preclinical toxicology studies."""
            }
        ]

        for i, test in enumerate(tests, 1):
            print(f"\n{'=' * 80}")
            print(f"TEST {i}: {test['name']}")
            print(f"{'=' * 80}")
            print(f"Prompt: {test['prompt'][:100]}...")
            print("")

            # Test Pro model
            print("🚀 Querying CroweLogic-Pharma Pro (70b)...")
            pro_result = self.query_model(
                self.pro_endpoint,
                "CroweLogic-Pharma-Pro:latest",
                test['prompt']
            )

            if pro_result['success']:
                print(f"✅ Response received in {pro_result['elapsed']:.1f}s")
                print(f"   Tokens: {pro_result['eval_count']} generated, {pro_result['prompt_eval_count']} prompt")
                print(f"\n📝 Response Preview:")
                print(f"   {pro_result['response'][:500]}...")

                # Calculate tokens per second
                if pro_result['elapsed'] > 0:
                    tps = pro_result['eval_count'] / pro_result['elapsed']
                    print(f"   Performance: {tps:.1f} tokens/second")
            else:
                print(f"❌ Error: {pro_result['error']}")

            # Optionally compare with standard model
            if self.standard_endpoint:
                print(f"\n📊 Comparing with Standard Model...")
                std_result = self.query_model(
                    self.standard_endpoint,
                    "CroweLogic-Pharma:latest",
                    test['prompt']
                )

                if std_result['success']:
                    print(f"   Standard: {std_result['elapsed']:.1f}s, {std_result['eval_count']} tokens")
                    speedup = std_result['elapsed'] / pro_result['elapsed'] if pro_result['success'] else 0
                    print(f"   Speed Comparison: 70b is {speedup:.2f}x the time of standard")

            # Pause between tests
            if i < len(tests):
                print(f"\n⏸️  Waiting 5 seconds before next test...")
                time.sleep(5)

        print(f"\n{'=' * 80}")
        print("✅ All tests completed!")
        print(f"{'=' * 80}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_70b_deployment.py <pro_endpoint> [standard_endpoint]")
        print("\nExample:")
        print("  python test_70b_deployment.py http://crowelogic-pharma-pro.eastus.azurecontainer.io:11434")
        print("\nWith comparison:")
        print("  python test_70b_deployment.py \\")
        print("    http://crowelogic-pharma-pro.eastus.azurecontainer.io:11434 \\")
        print("    http://crowelogic-pharma.eastus.azurecontainer.io:11434")
        sys.exit(1)

    pro_endpoint = sys.argv[1]
    standard_endpoint = sys.argv[2] if len(sys.argv) > 2 else None

    tester = Pharma70bTester(pro_endpoint, standard_endpoint)
    tester.run_advanced_tests()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script to fix the CroweLogic-Pharma model in the Azure container
"""
import subprocess
import sys

def run_container_command(command):
    """Execute a command in the Azure container"""
    full_cmd = [
        'az', 'container', 'exec',
        '--resource-group', 'crowelogic-pharma-rg',
        '--name', 'crowelogic-pharma-aci',
        '--exec-command', command
    ]
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0

def main():
    print("Step 1: Cleaning up old/broken models...")
    run_container_command("ollama rm CroweLogic-Pharma:latest")
    run_container_command("ollama rm gpt-oss:120b-cloud")

    print("\nStep 2: Listing available models...")
    run_container_command("ollama list")

    print("\nStep 3: Creating new CroweLogic-Pharma model with llama3.1:8b...")

    # Read the local Modelfile
    with open('/workspaces/crowelogic-pharma-model/models/CroweLogicPharmaModelfile', 'r') as f:
        modelfile_content = f.read()

    # Write Modelfile to container using printf to avoid quoting issues
    # Escape single quotes and backslashes for shell
    escaped_content = modelfile_content.replace("'", "'\"'\"'")

    # Write the file
    write_cmd = f"printf '%s' '{escaped_content}' > /tmp/CroweLogicPharmaModelfile"
    run_container_command(write_cmd)

    # Create the model from the temporary file
    run_container_command("ollama create CroweLogic-Pharma:latest -f /tmp/CroweLogicPharmaModelfile")

    print("\nStep 4: Verifying model creation...")
    run_container_command("ollama list")

    print("\n✅ Model configuration complete!")
    print("You can now test with:")
    print("  curl -X POST http://crowelogic-pharma.eastus.azurecontainer.io:11434/api/generate \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"model\": \"CroweLogic-Pharma:latest\", \"prompt\": \"Test query\", \"stream\": false}'")

if __name__ == '__main__':
    main()

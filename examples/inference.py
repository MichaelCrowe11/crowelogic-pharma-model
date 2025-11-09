#!/usr/bin/env python3
"""
Basic inference example for CroweLogic-Pharma model
Demonstrates how to load and query the fine-tuned Mistral-7B model
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

# Configuration
BASE_MODEL = "mistralai/Mistral-7B-v0.1"
ADAPTER_PATH = "../model"  # Path to LoRA adapters
DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

def load_model():
    """Load base model and LoRA adapters"""
    print(f"Loading model on device: {DEVICE}")
    print(f"Base model: {BASE_MODEL}")
    print(f"LoRA adapters: {ADAPTER_PATH}\n")

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Load base model
    base_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.float16 if DEVICE != "cpu" else torch.float32,
        device_map="auto",
        low_cpu_mem_usage=True,
    )

    # Load LoRA adapters
    model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)

    print("✓ Model loaded successfully\n")
    return model, tokenizer

def generate_response(model, tokenizer, question, max_tokens=512, temperature=0.7, top_p=0.9):
    """Generate response for a given question"""
    # Format prompt in Mistral instruction format
    prompt = f"<s>[INST] {question} [/INST]"

    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # Generate
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Decode and extract response
    full_response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = full_response.split("[/INST]")[-1].strip()

    return response

def main():
    """Main inference loop"""
    print("="*70)
    print("CroweLogic-Pharma Inference Demo")
    print("="*70)
    print()

    # Load model
    model, tokenizer = load_model()

    # Example queries
    example_queries = [
        "What is the mechanism of action of penicillin?",
        "What is Lipinski's Rule of Five?",
        "Explain the Crowe Logic multi-phase analysis pipeline.",
        "How do you implement type-safe API routes in Next.js?",
        "What are the pharmacokinetic properties of aspirin?",
    ]

    print("="*70)
    print("Example Queries")
    print("="*70)
    print()

    for i, question in enumerate(example_queries, 1):
        print(f"\n[Query {i}]")
        print(f"Q: {question}")
        print(f"\nA: ", end="", flush=True)

        response = generate_response(model, tokenizer, question)
        print(response)
        print("-"*70)

    # Interactive mode
    print("\n" + "="*70)
    print("Interactive Mode (type 'quit' to exit)")
    print("="*70)
    print()

    while True:
        try:
            question = input("\nYour question: ").strip()

            if question.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break

            if not question:
                continue

            response = generate_response(model, tokenizer, question)
            print(f"\nAnswer: {response}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")

if __name__ == "__main__":
    main()

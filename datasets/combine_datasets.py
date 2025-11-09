#!/usr/bin/env python3
"""
Combine all multi-source datasets with existing training data
"""
import json
import random
from pathlib import Path

def combine_datasets():
    """Combine all dataset files into master training/validation sets"""

    datasets_dir = Path(__file__).parent

    # Load existing master dataset
    print("Loading existing dataset...")
    existing = []
    master_file = datasets_dir / "crowelogic_pharma_combined.jsonl"
    if master_file.exists():
        with open(master_file, 'r') as f:
            existing = [json.loads(line) for line in f]
    print(f"  Loaded {len(existing)} existing examples")

    # Load all multi-source datasets
    print("\nLoading new multi-source examples...")
    new_examples = []

    multi_source_files = [
        "multi_source_1k.jsonl",
        "multi_source_10k.jsonl",
        "multi_source_50k.jsonl"
    ]

    for filename in multi_source_files:
        filepath = datasets_dir / filename
        if filepath.exists():
            with open(filepath, 'r') as f:
                examples = [json.loads(line) for line in f]
                new_examples.extend(examples)
                print(f"  {filename}: {len(examples)} examples")

    print(f"\n  Total new examples: {len(new_examples)}")

    # Check for duplicates (by instruction text)
    print("\nChecking for duplicates...")
    existing_instructions = {ex['instruction'] for ex in existing}
    unique_new = [ex for ex in new_examples if ex['instruction'] not in existing_instructions]

    duplicates = len(new_examples) - len(unique_new)
    print(f"  Found {duplicates} duplicates (skipping)")
    print(f"  Unique new examples: {len(unique_new)}")

    # Combine
    all_examples = existing + unique_new
    print(f"\n✓ Total combined: {len(all_examples)} examples")

    # Shuffle and split 90/10
    random.seed(42)
    random.shuffle(all_examples)

    split_idx = int(len(all_examples) * 0.9)
    train_set = all_examples[:split_idx]
    val_set = all_examples[split_idx:]

    print(f"\nSplit into:")
    print(f"  Training: {len(train_set)} examples")
    print(f"  Validation: {len(val_set)} examples")

    # Save updated datasets
    print("\nSaving updated datasets...")

    # Save combined
    with open(datasets_dir / "crowelogic_pharma_combined.jsonl", 'w') as f:
        for ex in all_examples:
            f.write(json.dumps(ex) + '\n')
    print(f"  ✓ Saved crowelogic_pharma_combined.jsonl ({len(all_examples)} examples)")

    # Save train
    with open(datasets_dir / "crowelogic_pharma_train.jsonl", 'w') as f:
        for ex in train_set:
            f.write(json.dumps(ex) + '\n')
    print(f"  ✓ Saved crowelogic_pharma_train.jsonl ({len(train_set)} examples)")

    # Save validation
    with open(datasets_dir / "crowelogic_pharma_val.jsonl", 'w') as f:
        for ex in val_set:
            f.write(json.dumps(ex) + '\n')
    print(f"  ✓ Saved crowelogic_pharma_val.jsonl ({len(val_set)} examples)")

    # Statistics
    print("\n" + "="*70)
    print("Dataset Update Complete!")
    print("="*70)
    print(f"\nPrevious total: {len(existing)} examples")
    print(f"New unique examples: {len(unique_new)} examples")
    print(f"Current total: {len(all_examples)} examples")
    print(f"\n✓ Training set: {len(train_set)} examples")
    print(f"✓ Validation set: {len(val_set)} examples")
    print("\n✓ Ready for model training!")

if __name__ == "__main__":
    combine_datasets()

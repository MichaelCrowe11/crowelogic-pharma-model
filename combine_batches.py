#!/usr/bin/env python3
"""
Combine Multiple Batch Files
Merges datasets generated on different PCs into a single dataset

Usage:
    # Combine all batches in generated_data/batches/
    python combine_batches.py --input-dir generated_data/batches --output combined_dataset.jsonl

    # Combine specific batches
    python combine_batches.py --input-dir generated_data/batches --batches 0 1 2 3 4

    # Create train/val/test splits
    python combine_batches.py --input-dir generated_data/batches --output combined.jsonl --split
"""

import json
import random
import argparse
from pathlib import Path
from typing import List, Dict
from collections import defaultdict
from tqdm import tqdm


def load_batch_files(input_dir: Path, batch_ids: List[int] = None) -> List[Dict]:
    """Load all batch JSONL files"""
    print(f"Loading batches from {input_dir}...")

    all_examples = []
    stats = defaultdict(int)

    # Find batch files
    if batch_ids:
        batch_files = [input_dir / f"batch_{bid}.jsonl" for bid in batch_ids]
    else:
        batch_files = sorted(input_dir.glob("batch_*.jsonl"))

    print(f"Found {len(batch_files)} batch files")

    # Load each batch
    for batch_file in tqdm(batch_files, desc="Loading batches"):
        if not batch_file.exists():
            print(f"  Warning: {batch_file} not found, skipping")
            continue

        batch_count = 0
        with open(batch_file, 'r') as f:
            for line in f:
                try:
                    example = json.loads(line.strip())
                    all_examples.append(example)
                    batch_count += 1

                    # Track stats
                    category = example.get('metadata', {}).get('category', 'unknown')
                    stats[f'category_{category}'] += 1

                except json.JSONDecodeError as e:
                    print(f"  Error parsing line in {batch_file}: {e}")
                    continue

        stats[f'batch_{batch_file.stem}'] = batch_count

    print(f"\n✓ Loaded {len(all_examples):,} total examples")
    return all_examples, dict(stats)


def remove_duplicates(examples: List[Dict]) -> List[Dict]:
    """Remove duplicate examples based on instruction+response"""
    print("\nRemoving duplicates...")

    seen = set()
    unique_examples = []

    for example in tqdm(examples, desc="Deduplicating"):
        # Create hash from instruction + response
        key = f"{example['instruction']}||{example['response']}"

        if key not in seen:
            seen.add(key)
            unique_examples.append(example)

    removed = len(examples) - len(unique_examples)
    print(f"✓ Removed {removed:,} duplicates ({removed/len(examples)*100:.1f}%)")
    print(f"✓ Unique examples: {len(unique_examples):,}")

    return unique_examples


def create_splits(examples: List[Dict], output_file: Path):
    """Create train/val/test splits"""
    print("\nCreating train/val/test splits (80/10/10)...")

    # Shuffle
    random.seed(42)
    random.shuffle(examples)

    # Split
    train_size = int(len(examples) * 0.8)
    val_size = int(len(examples) * 0.1)

    splits = {
        'train': examples[:train_size],
        'val': examples[train_size:train_size + val_size],
        'test': examples[train_size + val_size:]
    }

    # Save each split
    base_name = output_file.stem
    output_dir = output_file.parent

    for split_name, split_data in splits.items():
        split_file = output_dir / f"{base_name}_{split_name}.jsonl"

        with open(split_file, 'w') as f:
            for example in split_data:
                f.write(json.dumps(example) + '\n')

        size_mb = split_file.stat().st_size / 1024 / 1024
        print(f"  {split_name:5s}: {len(split_data):8,} examples → {split_file} ({size_mb:.1f} MB)")


def save_metadata(stats: Dict, output_file: Path, total_examples: int):
    """Save dataset metadata"""
    metadata_file = output_file.with_suffix('.metadata.json')

    metadata = {
        'total_examples': total_examples,
        'output_file': str(output_file),
        'stats': stats,
    }

    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✓ Metadata saved → {metadata_file}")


def analyze_dataset(examples: List[Dict]):
    """Print dataset analysis"""
    print("\n" + "="*70)
    print("DATASET ANALYSIS")
    print("="*70)

    # Category distribution
    categories = defaultdict(int)
    sources = defaultdict(int)
    difficulties = defaultdict(int)

    for example in examples:
        metadata = example.get('metadata', {})
        categories[metadata.get('category', 'unknown')] += 1
        sources[metadata.get('source_compound', 'unknown')] += 1
        difficulties[metadata.get('difficulty', 'unknown')] += 1

    print("\nCategory Distribution:")
    for category, count in sorted(categories.items(), key=lambda x: -x[1])[:10]:
        pct = count / len(examples) * 100
        print(f"  {category:30s}: {count:8,} ({pct:5.1f}%)")

    print("\nSource Distribution:")
    for source, count in sorted(sources.items(), key=lambda x: -x[1])[:10]:
        pct = count / len(examples) * 100
        print(f"  {source:30s}: {count:8,} ({pct:5.1f}%)")

    print("\nDifficulty Distribution:")
    for difficulty, count in sorted(difficulties.items()):
        pct = count / len(examples) * 100
        print(f"  {difficulty:30s}: {count:8,} ({pct:5.1f}%)")

    print("="*70)


def main():
    parser = argparse.ArgumentParser(description='Combine batch datasets from multiple PCs')
    parser.add_argument('--input-dir', type=str, default='generated_data/batches',
                       help='Input directory containing batch files')
    parser.add_argument('--output', type=str, default='combined_dataset.jsonl',
                       help='Output file path')
    parser.add_argument('--batches', type=int, nargs='+',
                       help='Specific batch IDs to combine (default: all)')
    parser.add_argument('--split', action='store_true',
                       help='Create train/val/test splits')
    parser.add_argument('--deduplicate', action='store_true', default=True,
                       help='Remove duplicate examples (default: True)')
    parser.add_argument('--analyze', action='store_true', default=True,
                       help='Print dataset analysis (default: True)')

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_file = Path(args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("BATCH COMBINER")
    print("="*70)
    print(f"Input:  {input_dir}")
    print(f"Output: {output_file}")
    if args.batches:
        print(f"Batches: {args.batches}")
    print("="*70 + "\n")

    # Load batches
    examples, stats = load_batch_files(input_dir, args.batches)

    if not examples:
        print("No examples found. Exiting.")
        return

    # Remove duplicates
    if args.deduplicate:
        examples = remove_duplicates(examples)

    # Analyze
    if args.analyze:
        analyze_dataset(examples)

    # Save combined dataset
    print(f"\nSaving combined dataset...")
    with open(output_file, 'w') as f:
        for example in tqdm(examples, desc="Writing"):
            f.write(json.dumps(example) + '\n')

    size_mb = output_file.stat().st_size / 1024 / 1024
    print(f"✓ Saved {len(examples):,} examples → {output_file} ({size_mb:.1f} MB)")

    # Save metadata
    save_metadata(stats, output_file, len(examples))

    # Create splits
    if args.split:
        create_splits(examples, output_file)

    # Final summary
    print("\n" + "="*70)
    print("COMBINING COMPLETE")
    print("="*70)
    print(f"✓ Total examples: {len(examples):,}")
    print(f"✓ Output file: {output_file}")
    print(f"✓ File size: {size_mb:.1f} MB")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()

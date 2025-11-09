#!/bin/bash
#
# Scale Data Generation to 10M Examples
# Uses proven generate_training_data.py script in batches
#
# Strategy: Generate in batches of 50K examples from 10K compounds each
# Total: 200 batches = 10M examples
#

set -e  # Exit on error

# Configuration
TARGET_TOTAL=10000000
BATCH_SIZE=50000
COMPOUNDS_PER_BATCH=10000
OUTPUT_DIR="./generated_data/massive_10m"

# Calculate number of batches
NUM_BATCHES=$((TARGET_TOTAL / BATCH_SIZE))

echo "================================"
echo "MASSIVE-SCALE DATA GENERATION"
echo "================================"
echo "Target: ${TARGET_TOTAL} examples"
echo "Batch size: ${BATCH_SIZE} examples"
echo "Compounds per batch: ${COMPOUNDS_PER_BATCH}"
echo "Total batches: ${NUM_BATCHES}"
echo "Output: ${OUTPUT_DIR}"
echo "================================"
echo

# Create output directory
mkdir -p "${OUTPUT_DIR}"
mkdir -p "${OUTPUT_DIR}/batches"

# Track progress
TOTAL_GENERATED=0
START_TIME=$(date +%s)

for batch_num in $(seq 1 $NUM_BATCHES); do
    echo
    echo "=========================================="
    echo "BATCH ${batch_num}/${NUM_BATCHES}"
    echo "=========================================="

    BATCH_OUTPUT="${OUTPUT_DIR}/batches/batch_${batch_num}.jsonl"

    # Skip if batch already exists
    if [ -f "$BATCH_OUTPUT" ]; then
        BATCH_COUNT=$(wc -l < "$BATCH_OUTPUT")
        echo "✓ Batch ${batch_num} already exists (${BATCH_COUNT} examples)"
        TOTAL_GENERATED=$((TOTAL_GENERATED + BATCH_COUNT))
        continue
    fi

    # Generate batch using proven script
    echo "Generating ${BATCH_SIZE} examples from ${COMPOUNDS_PER_BATCH} compounds..."

    python3 generate_training_data.py \
        --compounds ${COMPOUNDS_PER_BATCH} \
        --examples ${BATCH_SIZE} \
        --output "${BATCH_OUTPUT}" \
        || {
            echo "ERROR: Batch ${batch_num} failed"
            exit 1
        }

    # Count examples in batch
    if [ -f "$BATCH_OUTPUT" ]; then
        BATCH_COUNT=$(wc -l < "$BATCH_OUTPUT")
        TOTAL_GENERATED=$((TOTAL_GENERATED + BATCH_COUNT))
        echo "✓ Batch ${batch_num} complete: ${BATCH_COUNT} examples"
        echo "✓ Total generated so far: ${TOTAL_GENERATED} / ${TARGET_TOTAL}"
    else
        echo "ERROR: Batch output file not created"
        exit 1
    fi

    # Progress summary
    ELAPSED=$(($(date +%s) - START_TIME))
    RATE=$((TOTAL_GENERATED / (ELAPSED + 1)))
    REMAINING=$((TARGET_TOTAL - TOTAL_GENERATED))
    ETA=$((REMAINING / (RATE + 1)))

    echo
    echo "Progress: ${TOTAL_GENERATED} / ${TARGET_TOTAL} ($(( TOTAL_GENERATED * 100 / TARGET_TOTAL ))%)"
    echo "Rate: ${RATE} examples/second"
    echo "Elapsed: $((ELAPSED / 3600))h $(( (ELAPSED % 3600) / 60))m"
    echo "ETA: $((ETA / 3600))h $(( (ETA % 3600) / 60))m"

    # Save checkpoint metadata
    cat > "${OUTPUT_DIR}/progress.json" <<EOF
{
  "total_target": ${TARGET_TOTAL},
  "total_generated": ${TOTAL_GENERATED},
  "batches_complete": ${batch_num},
  "batches_total": ${NUM_BATCHES},
  "elapsed_seconds": ${ELAPSED},
  "rate_per_second": ${RATE}
}
EOF

    # Check if target reached
    if [ $TOTAL_GENERATED -ge $TARGET_TOTAL ]; then
        echo
        echo "✓ TARGET REACHED: ${TOTAL_GENERATED} examples"
        break
    fi
done

echo
echo "=========================================="
echo "COMBINING BATCHES"
echo "=========================================="

# Combine all batches into single file
COMBINED_FILE="${OUTPUT_DIR}/combined_10m.jsonl"
echo "Combining batches into ${COMBINED_FILE}..."

cat "${OUTPUT_DIR}"/batches/batch_*.jsonl > "$COMBINED_FILE"

FINAL_COUNT=$(wc -l < "$COMBINED_FILE")
echo "✓ Combined file created: ${FINAL_COUNT} examples"

# Create train/val/test splits
echo
echo "Creating train/val/test splits (80/10/10)..."

python3 << 'PYTHON_SCRIPT'
import json
import random
from pathlib import Path

# Load combined file
combined_file = Path("./generated_data/massive_10m/combined_10m.jsonl")
examples = []

print(f"Loading {combined_file}...")
with open(combined_file, 'r') as f:
    for line in f:
        examples.append(json.loads(line))

print(f"Loaded {len(examples)} examples")

# Shuffle
random.seed(42)
random.shuffle(examples)

# Split
train_size = int(len(examples) * 0.8)
val_size = int(len(examples) * 0.1)

train_set = examples[:train_size]
val_set = examples[train_size:train_size + val_size]
test_set = examples[train_size + val_size:]

# Save splits
output_dir = Path("./generated_data/massive_10m")

splits = [
    ('train', train_set),
    ('val', val_set),
    ('test', test_set)
]

for split_name, split_data in splits:
    split_file = output_dir / f"massive_10m_{split_name}.jsonl"
    with open(split_file, 'w') as f:
        for example in split_data:
            f.write(json.dumps(example) + '\n')
    print(f"✓ {split_name}: {len(split_data)} examples → {split_file}")

print("\n✓ Splits complete!")
PYTHON_SCRIPT

echo
echo "=========================================="
echo "GENERATION COMPLETE"
echo "=========================================="

TOTAL_TIME=$(($(date +%s) - START_TIME))

echo "✓ Total examples: ${FINAL_COUNT}"
echo "✓ Total time: $((TOTAL_TIME / 3600))h $(( (TOTAL_TIME % 3600) / 60))m"
echo "✓ Average rate: $((FINAL_COUNT / (TOTAL_TIME + 1))) examples/second"
echo "✓ Output directory: ${OUTPUT_DIR}"
echo
echo "Files created:"
echo "  - combined_10m.jsonl (all examples)"
echo "  - massive_10m_train.jsonl (80%)"
echo "  - massive_10m_val.jsonl (10%)"
echo "  - massive_10m_test.jsonl (10%)"
echo
echo "✓ Ready for 70B model training!"

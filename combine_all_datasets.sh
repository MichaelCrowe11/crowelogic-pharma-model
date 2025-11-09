#!/bin/bash

echo "═══════════════════════════════════════════════════════════════════"
echo "📦 COMBINE ALL DATASETS"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Create output directory
mkdir -p datasets/combined

# Combine all batch files
echo "Combining datasets..."
echo ""

# Start with existing master dataset
EXISTING="datasets/crowelogic_pharma_master_train.jsonl"
if [ -f "$EXISTING" ]; then
    EXISTING_COUNT=$(wc -l < "$EXISTING")
    echo "📊 Existing master dataset: $EXISTING_COUNT examples"
    cp "$EXISTING" datasets/combined/all_examples.jsonl
else
    echo "⚠️  No existing master dataset found, starting fresh"
    touch datasets/combined/all_examples.jsonl
fi

# Add Phase 1 batches
echo ""
echo "Adding Phase 1 batches..."
for file in datasets/batch_*.jsonl; do
    if [ -f "$file" ]; then
        COUNT=$(wc -l < "$file")
        echo "  + $file: $COUNT examples"
        cat "$file" >> datasets/combined/all_examples.jsonl
    fi
done

# Add Phase 2 batches
echo ""
echo "Adding Phase 2 batches..."
for file in datasets/phase_2_batch_*.jsonl; do
    if [ -f "$file" ]; then
        COUNT=$(wc -l < "$file")
        echo "  + $file: $COUNT examples"
        cat "$file" >> datasets/combined/all_examples.jsonl
    fi
done

# Add multi-source batches (if not already in master)
echo ""
echo "Adding multi-source batches..."
for file in datasets/multi_source_*.jsonl; do
    if [ -f "$file" ] && [ "$file" != "datasets/multi_source_50k.jsonl" ]; then
        COUNT=$(wc -l < "$file")
        echo "  + $file: $COUNT examples"
        cat "$file" >> datasets/combined/all_examples.jsonl
    fi
done

# Count total
echo ""
echo "───────────────────────────────────────────────────────────────────"
TOTAL=$(wc -l < datasets/combined/all_examples.jsonl)
SIZE=$(ls -lh datasets/combined/all_examples.jsonl | awk '{print $5}')
echo "✅ TOTAL EXAMPLES: $TOTAL"
echo "📁 File size: $SIZE"
echo "📂 Output: datasets/combined/all_examples.jsonl"
echo ""

# Shuffle and split into train/val
echo "───────────────────────────────────────────────────────────────────"
echo "Creating train/validation splits (90/10)..."
echo ""

# Shuffle
shuf datasets/combined/all_examples.jsonl > datasets/combined/all_shuffled.jsonl

# Calculate split
TRAIN_SIZE=$(echo "$TOTAL * 0.9 / 1" | bc)
VAL_SIZE=$(echo "$TOTAL - $TRAIN_SIZE" | bc)

# Split
head -n $TRAIN_SIZE datasets/combined/all_shuffled.jsonl > datasets/combined/final_train.jsonl
tail -n $VAL_SIZE datasets/combined/all_shuffled.jsonl > datasets/combined/final_val.jsonl

echo "✅ Training set: $TRAIN_SIZE examples"
echo "   → datasets/combined/final_train.jsonl"
echo ""
echo "✅ Validation set: $VAL_SIZE examples"
echo "   → datasets/combined/final_val.jsonl"
echo ""

# Cleanup
rm datasets/combined/all_shuffled.jsonl

echo "═══════════════════════════════════════════════════════════════════"
echo "✅ DATASET COMBINATION COMPLETE"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Final datasets:"
echo "  Training:   $TRAIN_SIZE examples (datasets/combined/final_train.jsonl)"
echo "  Validation: $VAL_SIZE examples (datasets/combined/final_val.jsonl)"
echo "  Combined:   $TOTAL examples (datasets/combined/all_examples.jsonl)"
echo ""

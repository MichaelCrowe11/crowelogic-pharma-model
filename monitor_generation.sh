#!/bin/bash

echo "═══════════════════════════════════════════════════════════════════"
echo "🔍 PHARMA MODEL GENERATION MONITOR"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Check running processes
RUNNING=$(ps aux | grep "generate_training_data.py" | grep -v grep | wc -l)
echo "📊 Active generation processes: $RUNNING"
echo ""

# Check batch statuses
if [ -f "logs/batch_1_5k.log" ]; then
    echo "───────────────────────────────────────────────────────────────────"
    echo "📦 BATCH 1 (1,000 compounds → 5,000 examples)"
    echo "───────────────────────────────────────────────────────────────────"

    # Get last progress line
    LAST_LINE=$(tail -100 logs/batch_1_5k.log | grep "ChEMBL:" | tail -1)
    if [ -n "$LAST_LINE" ]; then
        echo "   Status: $LAST_LINE"
    fi

    # Check if completed
    if grep -q "Generation Complete" logs/batch_1_5k.log; then
        EXAMPLES=$(grep "Generated:" logs/batch_1_5k.log | tail -1 | awk '{print $3}')
        echo "   ✅ COMPLETED: $EXAMPLES examples generated"

        if [ -f "datasets/batch_1_5k.jsonl" ]; then
            SIZE=$(ls -lh datasets/batch_1_5k.jsonl | awk '{print $5}')
            LINES=$(wc -l < datasets/batch_1_5k.jsonl)
            echo "   File: datasets/batch_1_5k.jsonl ($SIZE, $LINES examples)"
        fi
    else
        echo "   ⏳ In progress..."
    fi
    echo ""
fi

if [ -f "logs/batch_2_10k.log" ]; then
    echo "───────────────────────────────────────────────────────────────────"
    echo "📦 BATCH 2 (2,000 compounds → 10,000 examples)"
    echo "───────────────────────────────────────────────────────────────────"

    LAST_LINE=$(tail -100 logs/batch_2_10k.log | grep "ChEMBL:" | tail -1)
    if [ -n "$LAST_LINE" ]; then
        echo "   Status: $LAST_LINE"
    fi

    if grep -q "Generation Complete" logs/batch_2_10k.log; then
        EXAMPLES=$(grep "Generated:" logs/batch_2_10k.log | tail -1 | awk '{print $3}')
        echo "   ✅ COMPLETED: $EXAMPLES examples generated"

        if [ -f "datasets/batch_2_10k.jsonl" ]; then
            SIZE=$(ls -lh datasets/batch_2_10k.jsonl | awk '{print $5}')
            LINES=$(wc -l < datasets/batch_2_10k.jsonl)
            echo "   File: datasets/batch_2_10k.jsonl ($SIZE, $LINES examples)"
        fi
    else
        echo "   ⏳ In progress..."
    fi
    echo ""
fi

if [ -f "logs/batch_3_25k.log" ]; then
    echo "───────────────────────────────────────────────────────────────────"
    echo "📦 BATCH 3 (5,000 compounds → 25,000 examples)"
    echo "───────────────────────────────────────────────────────────────────"

    LAST_LINE=$(tail -100 logs/batch_3_25k.log | grep "ChEMBL:" | tail -1)
    if [ -n "$LAST_LINE" ]; then
        echo "   Status: $LAST_LINE"
    fi

    if grep -q "Generation Complete" logs/batch_3_25k.log; then
        EXAMPLES=$(grep "Generated:" logs/batch_3_25k.log | tail -1 | awk '{print $3}')
        echo "   ✅ COMPLETED: $EXAMPLES examples generated"

        if [ -f "datasets/batch_3_25k.jsonl" ]; then
            SIZE=$(ls -lh datasets/batch_3_25k.jsonl | awk '{print $5}')
            LINES=$(wc -l < datasets/batch_3_25k.jsonl)
            echo "   File: datasets/batch_3_25k.jsonl ($SIZE, $LINES examples)"
        fi
    else
        echo "   ⏳ In progress..."
    fi
    echo ""
fi

# Summary
echo "═══════════════════════════════════════════════════════════════════"
echo "📈 DATASET SUMMARY"
echo "═══════════════════════════════════════════════════════════════════"

# Existing dataset
if [ -f "datasets/crowelogic_pharma_master_train.jsonl" ]; then
    EXISTING=$(wc -l < datasets/crowelogic_pharma_master_train.jsonl)
    SIZE=$(ls -lh datasets/crowelogic_pharma_master_train.jsonl | awk '{print $5}')
    echo "Current master dataset: $EXISTING examples ($SIZE)"
fi

# Count completed batches
TOTAL_NEW=0
if [ -f "datasets/batch_1_5k.jsonl" ]; then
    BATCH1=$(wc -l < datasets/batch_1_5k.jsonl)
    TOTAL_NEW=$((TOTAL_NEW + BATCH1))
fi
if [ -f "datasets/batch_2_10k.jsonl" ]; then
    BATCH2=$(wc -l < datasets/batch_2_10k.jsonl)
    TOTAL_NEW=$((TOTAL_NEW + BATCH2))
fi
if [ -f "datasets/batch_3_25k.jsonl" ]; then
    BATCH3=$(wc -l < datasets/batch_3_25k.jsonl)
    TOTAL_NEW=$((TOTAL_NEW + BATCH3))
fi

if [ $TOTAL_NEW -gt 0 ]; then
    echo "New examples from batches: $TOTAL_NEW"

    if [ -f "datasets/crowelogic_pharma_master_train.jsonl" ]; then
        PROJECTED=$((EXISTING + TOTAL_NEW))
        echo ""
        echo "PROJECTED TOTAL: $PROJECTED examples"
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"

#!/bin/bash

echo "═══════════════════════════════════════════════════════════════════"
echo "🚀 PHASE 2: MASSIVE SCALE GENERATION (+100K EXAMPLES)"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Ensure Phase 1 is complete
echo "Checking Phase 1 status..."
RUNNING=$(ps aux | grep "generate_training_data.py" | grep -v grep | wc -l)
if [ $RUNNING -gt 0 ]; then
    echo "⚠️  WARNING: Phase 1 processes still running ($RUNNING active)"
    echo "   Wait for Phase 1 to complete before launching Phase 2"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

echo ""
echo "───────────────────────────────────────────────────────────────────"
echo "PHASE 2 CONFIGURATION"
echo "───────────────────────────────────────────────────────────────────"
echo ""
echo "Target: +100,000 new examples"
echo "Strategy: 2 massive parallel runs"
echo ""
echo "  Run 4: 10,000 compounds → 50,000 examples"
echo "  Run 5: 10,000 compounds → 50,000 examples"
echo ""
echo "Expected duration: 6-8 hours (ChEMBL API rate limits)"
echo "Expected output: 100K+ examples (combined)"
echo ""

read -p "Launch Phase 2? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "🚀 LAUNCHING PHASE 2 RUNS"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

# Run 4: 10K compounds → 50K examples
echo "📊 Run 4: 10,000 compounds → 50,000 examples"
nohup python3 generate_training_data.py --compounds 10000 --examples 50000 \
  --output datasets/phase_2_batch_4_50k.jsonl > logs/phase_2_batch_4_50k.log 2>&1 &
PID4=$!
echo "   PID: $PID4"
echo "   Log: logs/phase_2_batch_4_50k.log"
echo "   Output: datasets/phase_2_batch_4_50k.jsonl"
echo ""

# Run 5: 10K compounds → 50K examples
echo "📊 Run 5: 10,000 compounds → 50,000 examples"
nohup python3 generate_training_data.py --compounds 10000 --examples 50000 \
  --output datasets/phase_2_batch_5_50k.jsonl > logs/phase_2_batch_5_50k.log 2>&1 &
PID5=$!
echo "   PID: $PID5"
echo "   Log: logs/phase_2_batch_5_50k.log"
echo "   Output: datasets/phase_2_batch_5_50k.jsonl"
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo "✅ PHASE 2 LAUNCHED SUCCESSFULLY"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Active PIDs: $PID4, $PID5"
echo ""
echo "Monitor progress with:"
echo "  ./monitor_generation.sh"
echo ""
echo "Expected completion: 6-8 hours"
echo "Expected total dataset: ~226K+ examples (Phase 1 + Phase 2)"
echo ""

#!/bin/bash

echo "🚀 LAUNCHING MASSIVE PARALLEL GENERATION"
echo "========================================"
echo ""

# Run 1: 5K examples from 1000 compounds
echo "📊 Batch 1: 1000 compounds → 5K examples"
nohup python3 generate_training_data.py --compounds 1000 --examples 5000 \
  --output datasets/batch_1_5k.jsonl > logs/batch_1_5k.log 2>&1 &
echo "   PID: $!"

# Run 2: 10K examples from 2000 compounds  
echo "📊 Batch 2: 2000 compounds → 10K examples"
nohup python3 generate_training_data.py --compounds 2000 --examples 10000 \
  --output datasets/batch_2_10k.jsonl > logs/batch_2_10k.log 2>&1 &
echo "   PID: $!"

# Run 3: 25K examples from 5000 compounds
echo "📊 Batch 3: 5000 compounds → 25K examples"
nohup python3 generate_training_data.py --compounds 5000 --examples 25000 \
  --output datasets/batch_3_25k.jsonl > logs/batch_3_25k.log 2>&1 &
echo "   PID: $!"

echo ""
echo "✅ All batches launched!"
echo "Monitor progress: tail -f logs/batch_*.log"
echo ""
echo "Expected total: 40K+ new examples"
echo "Combined with existing 86K: ~126K TOTAL"

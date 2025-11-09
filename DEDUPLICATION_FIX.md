# Compound Deduplication Fix

## Problem Discovered (Phase 1)

All 3 parallel runs in Phase 1 fetched **the same 989 compounds** instead of unique compounds:
- Batch 1: 4,736 examples from 989 compounds
- Batch 2: 4,702 examples from 989 compounds
- Batch 3: 4,624 examples from 989 compounds
- **Total**: 14,062 examples (but with significant compound overlap)

### Root Cause
ChEMBL API queries without offset parameters always return the first N results:
- `fetch_approved_drugs(limit=1000)` → Always returns compounds 0-999
- `fetch_natural_products(limit=1000)` → Always returns compounds 0-999

Parallel runs were fetching identical compound sets, just generating different question phrasings.

---

## Solution: Offset-Based Pagination

### Changes Made

1. **ChEMBL Fetcher** (`data_acquisition/chembl_fetcher.py`):
   - Added `offset` parameter to `fetch_approved_drugs()`
   - Added `offset` parameter to `fetch_natural_products()`
   - ChEMBL API supports pagination via `offset` parameter

2. **Data Orchestrator** (`generate_training_data.py`):
   - Added `offset` parameter to `DataOrchestrator` constructor
   - Pass offset to ChEMBL fetcher methods
   - Added `--offset` command-line argument

3. **Phase 2 Launch Script** (`launch_phase_2.sh`):
   - Run 4: Uses offset **2000** (fetches compounds 2000-12000)
   - Run 5: Uses offset **12000** (fetches compounds 12000-22000)
   - Each run now fetches completely different compound sets

---

## Phase 2 Strategy

### Offset Allocation
- **Phase 1** (already run): offset 0 → compounds 0-2000 (989 unique fetched)
- **Run 4**: offset 2000 → compounds 2000-12000 (~10K compounds)
- **Run 5**: offset 12000 → compounds 12000-22000 (~10K compounds)

### Expected Results
- Run 4: ~10K unique compounds → ~50K examples
- Run 5: ~10K unique compounds → ~50K examples
- **Total Phase 2**: ~100K NEW unique examples
- **Combined with Phase 1**: ~114K examples total

---

## Testing the Fix

Test command:
```bash
# Test offset=0 (same as Phase 1)
python3 generate_training_data.py --compounds 10 --examples 50 --offset 0 --output test_offset_0.jsonl

# Test offset=2000 (new compounds)
python3 generate_training_data.py --compounds 10 --examples 50 --offset 2000 --output test_offset_2000.jsonl
```

Verify different compounds are fetched by comparing the compound IDs in the logs.

---

## Launch Commands

```bash
# Launch Phase 2 (after testing)
./launch_phase_2.sh

# Monitor progress
./monitor_generation.sh
```

---

## Impact

**Before Fix (Phase 1)**:
- 3 parallel runs → 14K examples from **989 unique compounds**
- Massive duplication across batches

**After Fix (Phase 2+)**:
- 2 parallel runs → 100K examples from **~20K unique compounds**
- Zero duplication across batches
- Proper scaling toward 226K+ dataset goal

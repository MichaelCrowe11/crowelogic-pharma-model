# Pharmaceutical Training Data Sources

## Overview
Multi-source data acquisition strategy for building 200K+ pharmaceutical training examples.

---

## ✅ Active Data Sources

### 1. ChEMBL (Primary Source)
- **URL**: https://www.ebi.ac.uk/chembl/
- **API**: Free, no authentication required
- **Database Size**: 2.4M bioactive compounds
- **Current Fetching**:
  - ✅ **Approved Drugs**: 1,000 per run
  - ✅ **Natural Products**: 1,000 per run (ULTRA-AGGRESSIVE SCALING)
- **Data Quality**: Excellent - includes IC50, EC50, Ki values, clinical trial phases, mechanisms of action
- **Status**: **PRODUCTION** - Primary source for drug compounds

### 2. PubChem (Secondary Source)
- **URL**: https://pubchem.ncbi.nlm.nih.gov/
- **API**: Free, no authentication required
- **Database Size**: 150M+ compounds
- **Current Fetching**:
  - ✅ **Common Drugs**: 200+ curated pharmaceutical compounds
  - Covers all therapeutic classes (cardiovascular, antibiotics, psychiatric, etc.)
- **Data Quality**: Very Good - comprehensive molecular properties, bioactivity data
- **Status**: **PRODUCTION** - Complementary drug source

---

## ⚠️ Blocked Data Sources

### 3. COCONUT Natural Products
- **URL**: https://coconut.naturalproducts.net/
- **API**: Requires Sanctum token authentication
- **Database Size**: 400K+ natural products
- **Blocker**: ❌ **Authentication Required**
  - API endpoints discovered: `/api/molecules`, `/api/molecules/search`
  - Requires API token/credentials we don't have
- **Workaround**: ChEMBL natural products provide similar coverage (now fetching 1000/run)
- **Status**: **BLOCKED** - Cannot integrate without credentials

### 4. DrugBank
- **URL**: https://go.drugbank.com/
- **API**: Requires API key (commercial/academic license)
- **Database Size**: 14K+ drugs with clinical data
- **Blocker**: ⚠️ **Likely requires authentication**
  - Not yet tested, but DrugBank typically requires API keys
- **Status**: **NOT IMPLEMENTED** - Research needed

---

## 📊 Current Dataset Statistics

### Training Data (as of generation)
- **Existing Dataset**: 86,336 training examples, 9,575 validation examples
- **In Progress** (3 parallel runs):
  - Batch 1: 1,000 compounds → 5,000 examples
  - Batch 2: 2,000 compounds → 10,000 examples
  - Batch 3: 5,000 compounds → 25,000 examples
  - **Total Expected**: +40,000 examples
- **Projected Total**: ~126K examples after current runs complete

### Source Distribution
- **ChEMBL**: 74.6% (drugs + natural products)
- **PubChem**: 25.4% (common pharmaceutical drugs)

---

## 🚀 Scaling Strategy

### Phase 1: ULTRA-AGGRESSIVE Scaling (Current)
**Target**: 200K+ examples from free sources
- ✅ ChEMBL drugs: 500 → **1,000 per run** (DONE)
- ✅ ChEMBL natural products: 300 → **1,000 per run** (DONE)
- ✅ PubChem drugs: 50 → **200+ per run** (DONE)
- 🔄 Running 3 parallel generation batches (40K+ examples in progress)

### Phase 2: Additional Free Sources (Next Steps)
- Add **PubChem compound categories**:
  - Metabolites (human, microbial)
  - Vitamins & supplements
  - Toxins & environmental compounds
- Explore **ChemSpider** (free for academic use)
- Test **ZINC** database (free drug-like compounds)

### Phase 3: Premium Sources (Future)
- Acquire **DrugBank** academic license (if needed)
- Explore **COCONUT** API access (if authentication becomes available)
- Consider **Reaxys** or **SciFinder** (institutional access)

---

## 🔧 Data Quality & Diversity

### Template Coverage
Each compound generates 5-20 training examples using templates:
- Molecular properties (formula, weight, logP, TPSA)
- Drug-likeness analysis (Lipinski's Rule of Five)
- Chemical structure (SMILES, InChI)
- Pharmacological properties (bioactivity, mechanisms)
- Comparative analysis (similar compounds, structure-activity relationships)

### Compound Diversity
- **Approved drugs**: FDA/EMA approved therapeutics (high clinical relevance)
- **Natural products**: Plant/fungal/bacterial metabolites (structural diversity)
- **Drug candidates**: Clinical trial compounds (future therapeutics)
- **Metabolites**: Biological transformation products (ADME relevance)

---

## 📈 Performance & Caching

### API Performance
- **ChEMBL**: ~1-2s per compound (rate limiting)
- **PubChem**: ~1-2s per compound (rate limiting)
- **Cache Hit Rate**: ~30% (MD5-based caching of compound data)

### Optimization
- ✅ Parallel generation runs (3 simultaneous processes)
- ✅ Aggressive caching (reduces redundant API calls)
- ✅ Batch processing (500 examples per write operation)
- ✅ Error handling (continues on failed compound fetches)

---

## 🎯 Roadmap to 200K+ Examples

**Current Status**: 86K examples → **Projected**: 126K after current runs

**Path to 200K+**:
1. ✅ Complete current 40K generation (126K total)
2. Launch **4 additional massive runs**:
   - Run 4: 10,000 compounds → 50K examples
   - Run 5: 10,000 compounds → 50K examples
   - **Total**: +100K examples
3. **Final Total**: 226K+ examples

**Timeline**: 2-3 days for full 200K+ dataset generation (API rate limits)

---

## 📝 Notes

- All data sources are used for **educational/research purposes**
- ChEMBL and PubChem data are **freely available** with proper attribution
- COCONUT integration requires API access - **workaround in place** via ChEMBL natural products
- Generated training data follows **instruction-response format** for LLM fine-tuning

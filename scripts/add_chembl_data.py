#!/usr/bin/env python3
"""
Add ChEMBL Drug Target Knowledge to CroweLogic-Pharma
Processes 17,803 ChEMBL targets and creates training examples
"""

import json
import os
from pathlib import Path

class ChEMBLIntegrator:
    def __init__(self, chembl_file="../../Downloads/chembl_targets_all.jsonl"):
        self.chembl_file = chembl_file
        self.training_examples = []
        self.therapeutic_areas = {
            'oncology': ['cancer', 'tumor', 'carcinoma', 'leukemia', 'lymphoma'],
            'neurology': ['alzheimer', 'parkinson', 'neurodegenerative', 'cognitive', 'neural'],
            'immunology': ['immune', 'inflammation', 'autoimmune', 'cytokine'],
            'cardiovascular': ['heart', 'cardiac', 'vascular', 'hypertension'],
            'metabolic': ['diabetes', 'metabolic', 'obesity', 'lipid'],
            'infectious': ['antibacterial', 'antiviral', 'antimicrobial', 'pathogen']
        }

    def process_target(self, target_data):
        """Convert ChEMBL target to training example"""
        try:
            target_id = target_data.get('target_chembl_id', '')
            pref_name = target_data.get('pref_name', '')
            target_type = target_data.get('target_type', '')
            organism = target_data.get('organism', '')

            # Extract key information
            components = target_data.get('target_components', [])
            if not components:
                return None

            component = components[0]
            accession = component.get('accession', '')
            description = component.get('component_description', '')

            # Extract gene symbols
            synonyms = component.get('target_component_synonyms', [])
            gene_symbols = [s['component_synonym'] for s in synonyms if s.get('syn_type') == 'GENE_SYMBOL']

            # Extract GO terms
            xrefs = component.get('target_component_xrefs', [])
            go_functions = [x['xref_name'] for x in xrefs if x.get('xref_src_db') == 'GoFunction' and x.get('xref_name')]
            go_processes = [x['xref_name'] for x in xrefs if x.get('xref_src_db') == 'GoProcess' and x.get('xref_name')]

            # Extract PDB structures
            pdb_ids = [x['xref_id'] for x in xrefs if x.get('xref_src_db') == 'PDB']

            # Create training example
            if not pref_name:
                return None

            prompt = f"What is the drug target {pref_name} (ChEMBL ID: {target_id})?"

            response_parts = [f"{pref_name} is a {target_type.lower()} target in {organism}."]

            if gene_symbols:
                response_parts.append(f"\n\n**Gene Symbol**: {', '.join(gene_symbols[:3])}")

            if description and description != pref_name:
                response_parts.append(f"\n**Description**: {description}")

            if accession:
                response_parts.append(f"\n**UniProt**: {accession}")

            if go_functions:
                response_parts.append(f"\n\n**Molecular Functions**:")
                for func in go_functions[:5]:
                    response_parts.append(f"\n- {func}")

            if go_processes:
                response_parts.append(f"\n\n**Biological Processes**:")
                for proc in go_processes[:5]:
                    response_parts.append(f"\n- {proc}")

            if pdb_ids:
                response_parts.append(f"\n\n**Available Structures**: {len(pdb_ids)} PDB entries ({', '.join(pdb_ids[:5])}{'...' if len(pdb_ids) > 5 else ''})")

            response_parts.append(f"\n\n**ChEMBL Link**: https://www.ebi.ac.uk/chembl/target_report_card/{target_id}/")
            response_parts.append(f"\n**Therapeutic Relevance**: This target is catalogued in ChEMBL, indicating validated or potential drug development applications.")

            response = ''.join(response_parts)

            return {
                "prompt": prompt,
                "response": response,
                "source": "chembl",
                "category": "drug_targets",
                "target_id": target_id,
                "target_type": target_type,
                "organism": organism
            }

        except Exception as e:
            print(f"Error processing target: {e}")
            return None

    def sample_targets(self, n_samples=200):
        """Sample diverse targets for training"""
        print(f"Reading ChEMBL targets from {self.chembl_file}...")

        target_types = {}
        total_count = 0

        with open(self.chembl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    total_count += 1
                    target_data = json.loads(line)
                    target_type = target_data.get('target_type', 'UNKNOWN')

                    if target_type not in target_types:
                        target_types[target_type] = []

                    if len(target_types[target_type]) < n_samples // len(target_types):
                        example = self.process_target(target_data)
                        if example:
                            target_types[target_type].append(example)

                    if total_count % 1000 == 0:
                        print(f"  Processed {total_count} targets...")

        print(f"\nTotal targets in database: {total_count}")
        print(f"\nTargets by type:")
        for ttype, examples in target_types.items():
            print(f"  {ttype}: {len(examples)} sampled")
            self.training_examples.extend(examples)

        return self.training_examples

    def classify_therapeutic_area(self, target_data):
        """Classify target into therapeutic areas based on description and GO terms"""
        text = f"{target_data.get('pref_name', '')} {target_data.get('organism', '')}"

        # Add GO terms to text
        components = target_data.get('target_components', [])
        if components:
            xrefs = components[0].get('target_component_xrefs', [])
            go_terms = [x['xref_name'] for x in xrefs if x.get('xref_name')]
            text += ' ' + ' '.join(go_terms)

        text = text.lower()
        areas = []

        for area, keywords in self.therapeutic_areas.items():
            if any(keyword in text for keyword in keywords):
                areas.append(area)

        return areas if areas else ['general']

    def create_bioactivity_examples(self):
        """Create examples about bioactivity data interpretation"""
        examples = [
            {
                "prompt": "How do you interpret IC50, EC50, Ki, and Kd values in drug discovery?",
                "response": """Bioactivity metrics in drug discovery:

**IC50 (Half-Maximal Inhibitory Concentration):**
- Definition: Concentration needed to inhibit 50% of target activity
- Units: Typically nM (nanomolar) or μM (micromolar)
- Lower IC50 = more potent inhibitor
- Example: Imatinib IC50 = 0.6 nM for BCR-ABL
- Use: Primary screening metric, dose-response curves
- Limitation: Assay-dependent (varies with substrate concentration)

**EC50 (Half-Maximal Effective Concentration):**
- Definition: Concentration producing 50% of maximal response
- Used for agonists (activators) rather than inhibitors
- Example: EC50 = 10 nM for receptor activation
- Cell-based assays often report EC50
- Reflects both binding and functional efficacy

**Ki (Inhibition Constant):**
- Definition: Equilibrium dissociation constant for inhibitor binding
- Calculated from IC50 using Cheng-Prusoff equation: Ki = IC50/(1 + [S]/Km)
- True thermodynamic measure of binding affinity
- Independent of assay conditions (unlike IC50)
- Example: Ki = 0.8 nM indicates tight binding
- Lower Ki = stronger binding

**Kd (Dissociation Constant):**
- Definition: Equilibrium constant for P + L ⇌ PL dissociation
- Direct binding measurement (no enzyme activity required)
- Methods: SPR (Surface Plasmon Resonance), ITC, fluorescence
- Kd = [P][L]/[PL] at equilibrium
- Lower Kd = tighter binding
- Example: Antibody-antigen Kd = 1 pM to 100 nM

**Comparison Table:**

| Metric | Type | Typical Range | Method | Interpretation |
|--------|------|---------------|--------|----------------|
| IC50 | Functional | 1 nM - 100 μM | Enzyme/cell assay | Potency (assay-dependent) |
| EC50 | Functional | 1 nM - 100 μM | Cell-based assay | Efficacy |
| Ki | Binding | 0.1 nM - 10 μM | Calculated or direct | True affinity (inhibitors) |
| Kd | Binding | 1 pM - 10 μM | Biophysical | True affinity (all binders) |

**Potency Classifications:**
- Very high potency: < 1 nM
- High potency: 1-100 nM
- Moderate potency: 100 nM - 1 μM
- Low potency: 1-10 μM
- Weak/inactive: > 10 μM

**ChEMBL Database Context:**
- Contains 20M+ bioactivity measurements
- Standardized to pChEMBL scale: -log10(IC50 or Ki in M)
- pChEMBL ≥ 6 (≤ 1 μM) considered active
- Enables cross-assay comparison
- Quality flags indicate measurement confidence

**Practical Considerations:**

1. **Target Product Profile (TPP):**
   - Lead optimization goal: IC50 < 10 nM
   - Selectivity: >100-fold vs off-targets
   - Cell potency: EC50 < 100 nM

2. **Structure-Activity Relationship (SAR):**
   - Track IC50 changes with structural modifications
   - Identify key pharmacophore elements
   - Optimize potency while maintaining drug-like properties

3. **In Vivo Translation:**
   - In vitro IC50 doesn't always predict in vivo efficacy
   - Consider: ADME, protein binding, tissue penetration
   - Free drug concentration at target site is key

**Example from ChEMBL:**
CHEMBL1201583 (Erlotinib) vs EGFR:
- IC50 = 2 nM (cellular assay)
- Ki = 0.5 nM (biochemical assay)
- Kd = 1.2 nM (SPR)
- Clinical dose: 150 mg/day (achieves effective plasma levels)

Understanding these metrics enables rational drug design and appropriate interpretation of ChEMBL bioactivity data.""",
                "source": "chembl_bioactivity",
                "category": "pharmacology",
                "dataset": "chembl_methodology"
            },
            {
                "prompt": "How do you use ChEMBL data to perform structure-activity relationship (SAR) analysis?",
                "response": """ChEMBL-based Structure-Activity Relationship (SAR) analysis:

**Step 1: Target Selection and Data Extraction**

**Query ChEMBL:**
```python
# Example using ChEMBL web services API
import requests

# Get bioactivity data for EGFR (ChEMBL203)
target_chembl_id = "CHEMBL203"
url = f"https://www.ebi.ac.uk/chembl/api/data/activity.json"
params = {
    'target_chembl_id': target_chembl_id,
    'pchembl_value__isnull': False,  # Only with standardized values
    'limit': 1000
}
response = requests.get(url, params=params)
activities = response.json()['activities']
```

**Data Filtering:**
- Select single assay type (e.g., IC50 binding assays)
- Filter by confidence score (≥ 8)
- Same assay conditions when possible
- Human vs other species
- Result: Consistent dataset for comparison

**Step 2: Structural Analysis**

**Identify Core Scaffold:**
- Extract SMILES for all compounds
- Perform maximum common substructure (MCS) analysis
- Define core pharmacophore

**Example EGFR Inhibitors:**
Core scaffold: 4-anilinoquinazoline
- Erlotinib: Quinazoline + 3-ethynyl aniline
- Gefitinib: Quinazoline + 3-chloro-4-fluoroaniline
- Lapatinib: Quinazoline + furyl-fluorobenzyl

**Step 3: SAR Analysis**

**Substituent Effects:**

**Position R1 (Quinazoline C-6):**
| Compound | R1 Substituent | IC50 (nM) | ΔICLOGP50 |
|----------|----------------|-----------|-------|
| 1 | -OCH3 | 500 | 0 (reference) |
| 2 | -OC2H5 | 250 | +0.3 (2x better) |
| 3 | -OCH2CH=CH2 | 100 | +0.7 (5x better) |
| 4 | -O-(cyclopropyl) | 50 | +1.0 (10x better) |

**Conclusion:** Larger lipophilic groups at R1 increase potency (hydrophobic pocket interaction)

**Position R2 (Aniline C-3):**
| Compound | R2 Substituent | IC50 (nM) | Selectivity |
|----------|----------------|-----------|-------------|
| 5 | -H | 150 | Low (hits EGFR + HER2) |
| 6 | -Cl | 20 | Moderate |
| 7 | -Br | 15 | High (EGFR selective) |
| 8 | -C≡CH | 2 | Very high |

**Conclusion:** Halogen/alkyne at R3 increases potency and selectivity (fills hydrophobic cleft)

**Step 4: Quantitative SAR (QSAR)**

**Hansch Analysis:**
log(1/IC50) = a·π + b·σ + c·Es + d

Where:
- π = lipophilicity (logP contribution)
- σ = electronic effect (Hammett constant)
- Es = steric parameter
- a,b,c,d = coefficients from regression

**Build Model:**
```python
from rdkit import Chem
from rdkit.Chem import Descriptors
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Features: Molecular descriptors
features = []
activities = []

for compound in chembl_data:
    mol = Chem.MolFromSmiles(compound['smiles'])
    desc = [
        Descriptors.MolLogP(mol),
        Descriptors.MolWt(mol),
        Descriptors.NumHDonors(mol),
        Descriptors.NumHAcceptors(mol),
        Descriptors.TPSA(mol)
    ]
    features.append(desc)
    activities.append(compound['pchembl_value'])  # -log(IC50)

# Train model
X = np.array(features)
y = np.array(activities)
model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

# Predict new compound activity
new_mol = Chem.MolFromSmiles('CC1=C(C=C(C=C1)NC(=O)C2=CC=CC=C2C3=CC=NC=C3)NC4=NC=CC(=N4)N5CCN(CC5)C')
new_desc = [Descriptors.MolLogP(new_mol), ...]
predicted_pchembl = model.predict([new_desc])
predicted_ic50 = 10 ** (-predicted_pchembl[0]) * 1e9  # Convert to nM
```

**Step 5: 3D SAR (Pharmacophore)**

**Align Active Compounds:**
- Superimpose high-potency compounds (IC50 < 10 nM)
- Identify common 3D features:
  - H-bond donors/acceptors
  - Hydrophobic centers
  - Aromatic rings
  - Charged groups

**EGFR Pharmacophore:**
- H-bond acceptor (quinazoline N-1): Binds Met793 backbone NH
- H-bond donor (quinazoline N-3): Binds Thr790 (gatekeeper)
- Hydrophobic center (aniline ring): Fills hydrophobic pocket
- Solvent-exposed region: Tolerates diverse substituents

**Step 6: Activity Cliff Analysis**

**Identify Activity Cliffs:**
- Compounds with high structural similarity but large activity differences
- Tanimoto similarity > 0.85, but ΔpIC50 > 1

**Example:**
- Compound A: -OCH3 substituent, IC50 = 500 nM
- Compound B: -OCH2C≡CH substituent, IC50 = 5 nM (100-fold difference!)
- Tiny change, huge impact: Reveals critical interaction

**Step 7: Lead Optimization Strategy**

**Based on SAR:**
1. **Potency:** Add ethynyl group at R2 (Erlotinib-like)
2. **Selectivity:** Modify R1 to avoid HER2 binding
3. **ADME:** Keep MW < 500, LogP < 5, add polar groups for solubility
4. **Synthesis:** Ensure modifications are chemically feasible

**Design Next Round:**
- Hybrid structures combining best features
- Small modifications to test cliff edges
- Address liabilities (e.g., reduce LogP if too high)

**Step 8: Validation**

**Prospective Testing:**
- Synthesize predicted high-potency compounds
- Measure IC50 experimentally
- Compare to predicted values
- Refine model with new data

**ChEMBL Advantages for SAR:**
- Large datasets (100s-1000s compounds per target)
- Standardized bioactivity (pChEMBL)
- Structural diversity
- Multiple targets for selectivity analysis
- Historical data to avoid failed strategies

**Typical SAR Workflow:**
1. Extract 200-500 compounds for target from ChEMBL
2. Filter for consistent assay type
3. Identify 20-50 structurally similar compounds
4. Perform SAR analysis (substituent scanning)
5. Build QSAR model (80% train, 20% test)
6. Design 10-20 new compounds
7. Predict activities
8. Synthesize top 5 candidates
9. Test experimentally
10. Iterate

**Success Metrics:**
- Model R² > 0.7 (good predictive power)
- 70%+ of designs meet potency goals
- Identify 3-5 fold improvements
- Reduce synthesis/testing cycles by 50%

ChEMBL's extensive bioactivity data enables data-driven SAR, accelerating lead optimization in drug discovery.""",
                "source": "chembl_sar_analysis",
                "category": "medicinal_chemistry",
                "dataset": "chembl_methodology"
            }
        ]

        self.training_examples.extend(examples)
        print(f"  Created {len(examples)} bioactivity analysis examples")
        return examples

    def create_compound_matching_examples(self):
        """Create examples for matching mushroom compounds to drug targets"""
        examples = [
            {
                "prompt": "How would you use ChEMBL to identify drug targets for hericenone A from Lion's Mane mushroom?",
                "response": """To identify potential drug targets for hericenone A using ChEMBL:

**1. Structure-Based Target Fishing:**
- Input hericenone A SMILES or structure
- Perform similarity search against ChEMBL compound library
- Identify structurally similar compounds with known targets
- Hypothesis: Similar structures may have similar targets

**2. Target Prioritization:**
Look for targets relevant to hericenone A's known effects:
- **Neurotrophin pathways**: NGF receptors (TrkA, p75NTR)
- **Neuroprotection**: Acetylcholinesterase (ChEMBL220)
- **Neuroinflammation**: COX-2 (ChEMBL230), NF-κB pathway
- **Oxidative stress**: Nrf2 activators, antioxidant enzymes

**3. ChEMBL Query Strategy:**
```
# Search for compounds with similar scaffolds
# Filter for targets in CNS/neurological pathways
# Prioritize targets with:
#   - PDB structures available (for docking)
#   - Bioactivity data (IC50, EC50)
#   - Disease association (Alzheimer's, neurodegeneration)
```

**4. Validation Approach:**
- Molecular docking to predicted targets
- In vitro binding assays
- Cell-based functional assays
- Compare to existing data on hericenone mechanisms

**5. Key ChEMBL Targets to Investigate:**
- ChEMBL220: Acetylcholinesterase (cognitive function)
- ChEMBL1827: PDE5 (neuroprotection, cerebral blood flow)
- ChEMBL4792: BACE1 (amyloid-beta production)
- ChEMBL4816: GSK3β (tau phosphorylation, neuroplasticity)

This systematic approach leverages ChEMBL's 17K+ targets to predict and validate mechanisms for natural product therapeutics.""",
                "source": "chembl_integration",
                "category": "target_prediction"
            },
            {
                "prompt": "Design a ChEMBL-based workflow for screening ganoderic acids against cancer targets.",
                "response": """ChEMBL-guided screening workflow for ganoderic acids in oncology:

**Phase 1: Target Identification**

Query ChEMBL for validated cancer targets:
- **Growth signaling**: EGFR (ChEMBL203), HER2 (ChEMBL1824)
- **Apoptosis**: BCL-2 family, caspases
- **Angiogenesis**: VEGFR (ChEMBL279), PDGFR
- **Cell cycle**: CDKs (ChEMBL308, ChEMBL4641)
- **Metastasis**: MMPs, integrins

**Phase 2: Structure-Activity Relationships**

Compare ganoderic acid structures to ChEMBL compounds:
1. Identify triterpenoid scaffolds in ChEMBL
2. Analyze bioactivity data for similar compounds
3. Map structure features to target selectivity
4. Predict ganoderic acid variants with best activity

**Phase 3: Virtual Screening**

For prioritized targets with PDB structures:
1. Download structures from ChEMBL links
2. Molecular docking of ganoderic acids A-F
3. Score binding affinity predictions
4. Rank target-compound pairs

**Phase 4: ChEMBL Bioactivity Analysis**

Extract reference data:
- IC50 values for similar compounds
- Selectivity profiles (on-target vs off-target)
- ADME properties of triterpenoids
- Clinical stage of comparable drugs

**Phase 5: Experimental Validation**

Prioritize top targets:
- **Target 1**: EGFR (abundant PDB data, validated in cancer)
- **Target 2**: BCL-2 (apoptosis induction observed)
- **Target 3**: NF-κB pathway (anti-inflammatory mechanism)

**Expected Outcomes:**
- 5-10 high-priority targets for ganoderic acids
- Structure-activity hypotheses
- Optimized analogs for synthesis
- Clinical development pathway

**ChEMBL Advantage:**
- 17K+ targets with bioactivity data
- Structural information for docking
- Comparable compounds for SAR
- Clinical context for target validation

This systematic approach accelerates natural product drug discovery by leveraging decades of pharmaceutical research data.""",
                "source": "chembl_integration",
                "category": "virtual_screening"
            }
        ]

        self.training_examples.extend(examples)
        return examples

    def save_training_data(self, output_file="chembl_training_data.jsonl"):
        """Save ChEMBL training examples"""
        output_path = Path("../training_data") / output_file

        print(f"\nSaving {len(self.training_examples)} ChEMBL training examples...")
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in self.training_examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')

        print(f"Saved to: {output_path}")

        # Also update the complete training file
        complete_path = Path("../training_data/crowelogic_pharma_complete_training.jsonl")
        if complete_path.exists():
            print("Appending to complete training file...")
            with open(complete_path, 'a', encoding='utf-8') as f:
                for example in self.training_examples:
                    f.write(json.dumps(example, ensure_ascii=False) + '\n')

        return output_path

def main():
    print("=== ChEMBL Integration for CroweLogic-Pharma ===\n")

    integrator = ChEMBLIntegrator()

    # Sample diverse targets from ChEMBL
    print("Step 1: Sampling drug targets from ChEMBL database...")
    integrator.sample_targets(n_samples=200)

    # Create bioactivity interpretation examples
    print("\nStep 2: Creating bioactivity interpretation examples...")
    integrator.create_bioactivity_examples()

    # Create mushroom-drug target matching examples
    print("\nStep 3: Creating compound-target matching examples...")
    integrator.create_compound_matching_examples()

    # Save training data
    print("\nStep 4: Saving training data...")
    output_file = integrator.save_training_data()

    print(f"\n=== Summary ===")
    print(f"Total training examples created: {len(integrator.training_examples)}")
    print(f"Output file: {output_file}")
    print("\nNext steps:")
    print("1. Review training data quality")
    print("2. Run consolidation: python scripts/consolidate_training_data.py")
    print("3. Rebuild model: ollama create CroweLogic-Pharma:120b-v3 -f models/CroweLogicPharmaModelfile")
    print("4. Test ChEMBL query capabilities")

if __name__ == "__main__":
    main()

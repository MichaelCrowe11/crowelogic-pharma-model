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

    # Create mushroom-drug target matching examples
    print("\nStep 2: Creating compound-target matching examples...")
    integrator.create_compound_matching_examples()

    # Save training data
    print("\nStep 3: Saving training data...")
    output_file = integrator.save_training_data()

    print(f"\n=== Summary ===")
    print(f"Total training examples created: {len(integrator.training_examples)}")
    print(f"Output file: {output_file}")
    print("\nNext steps:")
    print("1. Review training data quality")
    print("2. Rebuild model: ollama create CroweLogic-Pharma:120b-v3 -f models/CroweLogicPharmaModelfile")
    print("3. Test ChEMBL query capabilities")

if __name__ == "__main__":
    main()

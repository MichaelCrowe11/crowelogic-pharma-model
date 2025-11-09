#!/usr/bin/env python3
"""
Mass-Scale Example Generator
Generate millions of high-quality training examples from compound data

Target: 10M examples for multi-model training
Architecture: Distributed, parallel, template-based with LLM augmentation
"""

import json
import logging
import multiprocessing as mp
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Set
from pathlib import Path
from collections import defaultdict
import random
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Example:
    """Training example structure"""
    instruction: str
    response: str
    category: str
    source_compound: str
    difficulty: str  # easy, medium, hard, expert
    tags: List[str]


@dataclass
class GenerationConfig:
    """Configuration for mass-scale generation"""
    target_examples: int = 10_000_000
    examples_per_compound_min: int = 5
    examples_per_compound_max: int = 50
    quality_threshold: float = 0.8
    diversity_threshold: float = 0.7
    output_dir: Path = Path("./datasets")
    batch_size: int = 1000
    num_workers: int = mp.cpu_count()


class TemplateLibrary:
    """
    Massive template library for diverse example generation

    Categories:
    - Molecular Properties (35%)
    - Biological Activity (25%)
    - Natural Products (15%)
    - Clinical & Therapeutic (15%)
    - Crowe Logic Integration (10%)
    """

    def __init__(self):
        self.templates = self._build_template_library()

    def _build_template_library(self) -> Dict[str, List[Dict]]:
        """Build comprehensive template library"""

        templates = {
            # MOLECULAR PROPERTIES (Target: 3.5M examples)
            'basic_properties': self._molecular_property_templates(),
            'comparative_analysis': self._comparative_templates(),
            'drug_likeness': self._drug_likeness_templates(),
            'adme_properties': self._adme_templates(),
            'structure_analysis': self._structure_templates(),

            # BIOLOGICAL ACTIVITY (Target: 2.5M examples)
            'mechanism': self._mechanism_templates(),
            'target_interaction': self._target_templates(),
            'bioassay': self._bioassay_templates(),
            'sar': self._sar_templates(),

            # NATURAL PRODUCTS (Target: 1.5M examples)
            'traditional_use': self._traditional_use_templates(),
            'biosynthesis': self._biosynthesis_templates(),
            'ethnopharmacology': self._ethnopharm_templates(),

            # CLINICAL (Target: 1.5M examples)
            'indications': self._indication_templates(),
            'interactions': self._interaction_templates(),
            'adverse_effects': self._adverse_effect_templates(),

            # CROWE LOGIC (Target: 1M examples)
            'architecture': self._architecture_templates(),
            'ml_pipeline': self._ml_templates(),
        }

        return templates

    def _molecular_property_templates(self) -> List[Dict]:
        """Molecular property question templates"""
        return [
            {
                'template': 'What is the molecular formula of {name}?',
                'response': 'The molecular formula of {name} is {molecular_formula}.',
                'difficulty': 'easy',
                'requires': ['molecular_formula'],
            },
            {
                'template': 'What is the molecular weight of {name}?',
                'response': 'The molecular weight of {name} is {molecular_weight:.2f} g/mol.',
                'difficulty': 'easy',
                'requires': ['molecular_weight'],
            },
            {
                'template': 'Provide the SMILES notation for {name}.',
                'response': 'The canonical SMILES notation for {name} is: {smiles}',
                'difficulty': 'medium',
                'requires': ['smiles'],
            },
            {
                'template': 'What is the logP value of {name} and what does it indicate?',
                'response': 'The logP (partition coefficient) of {name} is {logp}. {logp_interpretation} This value is important for predicting membrane permeability and oral bioavailability.',
                'difficulty': 'medium',
                'requires': ['logp'],
            },
            {
                'template': 'What is the topological polar surface area (TPSA) of {name}?',
                'response': 'The TPSA of {name} is {tpsa} Ų. {tpsa_interpretation} TPSA is a key predictor of drug bioavailability and blood-brain barrier penetration.',
                'difficulty': 'medium',
                'requires': ['tpsa'],
            },
            {
                'template': 'How many hydrogen bond donors and acceptors does {name} have?',
                'response': '{name} has {h_donors} hydrogen bond donor(s) and {h_acceptors} hydrogen bond acceptor(s). {hb_interpretation}',
                'difficulty': 'easy',
                'requires': ['h_donors', 'h_acceptors'],
            },
            {
                'template': 'Does {name} satisfy Lipinski\'s Rule of Five?',
                'response': 'Analyzing {name}: MW={molecular_weight:.1f} (should be <500), logP={logp} (should be <5), H-donors={h_donors} (should be ≤5), H-acceptors={h_acceptors} (should be ≤10). {lipinski_result}',
                'difficulty': 'hard',
                'requires': ['molecular_weight', 'logp', 'h_donors', 'h_acceptors'],
            },
            {
                'template': 'Describe the key physicochemical properties of {name} relevant to drug development.',
                'response': '{name} ({molecular_formula}, MW: {molecular_weight:.2f} g/mol) exhibits the following drug-relevant properties: logP of {logp} ({logp_interpretation}), TPSA of {tpsa} Ų ({tpsa_interpretation}), {h_donors} H-bond donors and {h_acceptors} acceptors, and {rotatable_bonds} rotatable bonds. {drug_dev_implications}',
                'difficulty': 'expert',
                'requires': ['molecular_formula', 'molecular_weight', 'logp', 'tpsa', 'h_donors', 'h_acceptors', 'rotatable_bonds'],
            },
        ]

    def _comparative_templates(self) -> List[Dict]:
        """Comparative analysis templates"""
        return [
            {
                'template': 'Compare the lipophilicity of {name} with typical drug compounds.',
                'response': '{name} has a logP of {logp}. {logp_interpretation} Optimal oral drugs typically have logP values between 0 and 3, balancing solubility and membrane permeability.',
                'difficulty': 'medium',
                'requires': ['logp'],
            },
            {
                'template': 'Is {name} likely to cross the blood-brain barrier?',
                'response': 'Based on {name}\'s TPSA of {tpsa} Ų and logP of {logp}, {bbb_prediction}. Compounds with TPSA < 90 Ų and appropriate lipophilicity typically show better CNS penetration.',
                'difficulty': 'hard',
                'requires': ['tpsa', 'logp'],
            },
        ]

    def _drug_likeness_templates(self) -> List[Dict]:
        """Drug-likeness templates"""
        return [
            {
                'template': 'Assess the oral bioavailability potential of {name}.',
                'response': 'Based on Lipinski\'s Rule of Five analysis: {lipinski_result} Additionally, the TPSA of {tpsa} Ų and {rotatable_bonds} rotatable bonds {bioavailability_prediction}',
                'difficulty': 'hard',
                'requires': ['molecular_weight', 'logp', 'h_donors', 'h_acceptors', 'tpsa', 'rotatable_bonds'],
            },
        ]

    def _adme_templates(self) -> List[Dict]:
        """ADME property templates"""
        return [
            {
                'template': 'Predict the absorption characteristics of {name}.',
                'response': 'Absorption prediction for {name}: {absorption_prediction} based on MW={molecular_weight:.1f}, logP={logp}, TPSA={tpsa} Ų.',
                'difficulty': 'expert',
                'requires': ['molecular_weight', 'logp', 'tpsa'],
            },
        ]

    def _structure_templates(self) -> List[Dict]:
        """Structural analysis templates"""
        return [
            {
                'template': 'What are the key structural features of {name}?',
                'response': '{name} ({molecular_formula}) contains {structural_features}. Its SMILES structure ({smiles}) reveals {structure_analysis}',
                'difficulty': 'hard',
                'requires': ['molecular_formula', 'smiles'],
            },
        ]

    def _mechanism_templates(self) -> List[Dict]:
        """Mechanism of action templates"""
        return [
            {
                'template': 'Explain the general mechanism of action for compounds similar to {name}.',
                'response': 'Based on the structural class of {name} ({compound_class}), {general_mechanism}',
                'difficulty': 'expert',
                'requires': ['compound_class'],
            },
        ]

    def _target_templates(self) -> List[Dict]:
        """Target interaction templates"""
        return []

    def _bioassay_templates(self) -> List[Dict]:
        """Bioassay templates"""
        return []

    def _sar_templates(self) -> List[Dict]:
        """Structure-activity relationship templates"""
        return []

    def _traditional_use_templates(self) -> List[Dict]:
        """Traditional use templates for natural products"""
        return [
            {
                'template': 'What are the traditional medicinal uses of {name}?',
                'response': '{name}, found in {source_organism}, has been traditionally used for {traditional_uses}. {ethnopharm_context}',
                'difficulty': 'medium',
                'requires': ['source_organism', 'traditional_uses'],
                'applies_to': ['natural_product'],
            },
        ]

    def _biosynthesis_templates(self) -> List[Dict]:
        """Biosynthesis templates"""
        return []

    def _ethnopharm_templates(self) -> List[Dict]:
        """Ethnopharmacology templates"""
        return []

    def _indication_templates(self) -> List[Dict]:
        """Clinical indication templates"""
        return []

    def _interaction_templates(self) -> List[Dict]:
        """Drug interaction templates"""
        return []

    def _adverse_effect_templates(self) -> List[Dict]:
        """Adverse effect templates"""
        return []

    def _architecture_templates(self) -> List[Dict]:
        """Crowe Logic architecture templates"""
        return []

    def _ml_templates(self) -> List[Dict]:
        """ML pipeline templates"""
        return []

    def _has_field(self, compound_data: Dict, field: str) -> bool:
        """Check if a field is available in compound data (handles nested properties)"""
        # Check top level
        if field in compound_data:
            return True

        # Check properties dict (for fields like molecular_formula, molecular_weight, etc.)
        props = compound_data.get('properties', {})
        field_mappings = {
            'molecular_formula': 'molecular_formula',
            'molecular_weight': 'molecular_weight',
            'smiles': 'canonical_smiles',
            'logp': 'logp',
            'tpsa': 'tpsa',
            'h_donors': 'h_bond_donors',
            'h_acceptors': 'h_bond_acceptors',
            'rotatable_bonds': 'rotatable_bonds',
        }

        if field in field_mappings and props.get(field_mappings[field]) is not None:
            return True

        # Check metadata
        metadata = compound_data.get('metadata', {})
        if field in metadata:
            return True

        return False

    def get_templates_for_compound(self, compound_data: Dict) -> List[Dict]:
        """Select appropriate templates based on compound properties"""
        available_templates = []

        for category, templates in self.templates.items():
            for template in templates:
                # Check if required fields are available
                if 'requires' in template:
                    if all(self._has_field(compound_data, field) for field in template['requires']):
                        available_templates.append({**template, 'category': category})

                # Check if template applies to compound type
                elif 'applies_to' in template:
                    compound_type = compound_data.get('type', '')
                    if compound_type in template['applies_to']:
                        available_templates.append({**template, 'category': category})

        return available_templates


class MassScaleGenerator:
    """
    Generate millions of training examples at scale

    Features:
    - Parallel processing
    - Quality validation
    - Diversity enforcement
    - Progress tracking
    - Incremental saving
    """

    def __init__(self, config: Optional[GenerationConfig] = None):
        self.config = config or GenerationConfig()
        self.template_library = TemplateLibrary()
        self.generated_count = 0
        self.stats = defaultdict(int)

    def generate_from_compounds(
        self,
        compounds: List[Dict],
        output_path: Path
    ) -> int:
        """
        Generate examples from compound data

        Args:
            compounds: List of compound data dictionaries
            output_path: Where to save generated examples

        Returns:
            Number of examples generated
        """
        logger.info(f"Generating up to {self.config.target_examples:,} examples from {len(compounds):,} compounds")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        examples = []
        with tqdm(total=self.config.target_examples, desc="Generating examples") as pbar:
            for compound in compounds:
                if self.generated_count >= self.config.target_examples:
                    break

                # Generate examples for this compound
                compound_examples = self._generate_for_compound(compound)
                examples.extend(compound_examples)
                self.generated_count += len(compound_examples)
                pbar.update(len(compound_examples))

                # Save in batches
                if len(examples) >= self.config.batch_size:
                    self._save_batch(examples, output_path)
                    examples = []

        # Save remaining
        if examples:
            self._save_batch(examples, output_path)

        logger.info(f"✓ Generated {self.generated_count:,} examples")
        return self.generated_count

    def _generate_for_compound(self, compound: Dict) -> List[Example]:
        """Generate multiple examples for a single compound"""
        examples = []

        # Get applicable templates
        templates = self.template_library.get_templates_for_compound(compound)

        # Determine how many examples to generate
        # Ensure max is always >= min
        max_examples = min(self.config.examples_per_compound_max, len(templates))
        min_examples = min(self.config.examples_per_compound_min, max_examples)
        num_examples = random.randint(min_examples, max_examples)

        # Select diverse templates
        selected = random.sample(templates, min(num_examples, len(templates)))

        for template_data in selected:
            try:
                example = self._create_example(compound, template_data)
                if example and self._validate_example(example):
                    examples.append(example)
            except Exception as e:
                logger.debug(f"Failed to create example: {e}")
                continue

        return examples

    def _create_example(self, compound: Dict, template: Dict) -> Optional[Example]:
        """Create a single example from compound data and template"""
        try:
            # Extract compound data
            props = compound.get('properties', {})
            metadata = compound.get('metadata', {})

            # Prepare formatting dictionary
            format_dict = {
                'name': compound.get('name', 'Unknown'),
                'molecular_formula': props.get('molecular_formula', ''),
                'molecular_weight': props.get('molecular_weight', 0),
                'smiles': props.get('canonical_smiles', ''),
                'logp': props.get('logp', 0),
                'tpsa': props.get('tpsa', 0),
                'h_donors': props.get('h_bond_donors', 0),
                'h_acceptors': props.get('h_bond_acceptors', 0),
                'rotatable_bonds': props.get('rotatable_bonds', 0),
                # Add interpretations
                **self._generate_interpretations(props),
            }

            # Format instruction and response
            instruction = template['template'].format(**format_dict)
            response = template['response'].format(**format_dict)

            return Example(
                instruction=instruction,
                response=response,
                category=template.get('category', 'unknown'),
                source_compound=compound.get('id', 'unknown'),
                difficulty=template.get('difficulty', 'medium'),
                tags=template.get('tags', []),
            )

        except KeyError as e:
            logger.debug(f"Missing required field: {e}")
            return None

    def _generate_interpretations(self, props: Dict) -> Dict[str, str]:
        """Generate interpretive text for properties"""
        interp = {}

        # logP interpretation
        logp = props.get('logp', 0)
        if logp < 0:
            interp['logp_interpretation'] = "This indicates high hydrophilicity."
        elif logp < 3:
            interp['logp_interpretation'] = "This is within the optimal range for oral drugs."
        elif logp < 5:
            interp['logp_interpretation'] = "This indicates moderate lipophilicity."
        else:
            interp['logp_interpretation'] = "This indicates high lipophilicity, which may affect solubility."

        # TPSA interpretation
        tpsa = props.get('tpsa', 0)
        if tpsa < 60:
            interp['tpsa_interpretation'] = "This low value suggests good membrane permeability."
        elif tpsa < 140:
            interp['tpsa_interpretation'] = "This moderate value is typical for orally bioavailable drugs."
        else:
            interp['tpsa_interpretation'] = "This high value may limit oral bioavailability."

        # Lipinski analysis
        mw = props.get('molecular_weight', 0)
        violations = sum([
            mw > 500,
            logp > 5,
            props.get('h_bond_donors', 0) > 5,
            props.get('h_bond_acceptors', 0) > 10,
        ])

        if violations == 0:
            interp['lipinski_result'] = "This compound satisfies Lipinski's Rule of Five with no violations, suggesting good oral bioavailability potential."
        elif violations == 1:
            interp['lipinski_result'] = "This compound has 1 Lipinski violation but may still have acceptable oral bioavailability."
        else:
            interp['lipinski_result'] = f"This compound violates Lipinski's Rule of Five ({violations} violations), which may indicate poor oral bioavailability."

        return interp

    def _validate_example(self, example: Example) -> bool:
        """Validate example quality"""
        # Basic checks
        if len(example.instruction) < 10 or len(example.response) < 20:
            return False

        # Check for placeholder text
        if '{' in example.instruction or '{' in example.response:
            return False

        return True

    def _save_batch(self, examples: List[Example], output_path: Path):
        """Save batch of examples to file"""
        mode = 'a' if output_path.exists() else 'w'
        with open(output_path, mode) as f:
            for example in examples:
                # Convert to dict for JSON serialization
                example_dict = {
                    'instruction': example.instruction,
                    'response': example.response,
                }
                f.write(json.dumps(example_dict) + '\n')

        logger.debug(f"Saved batch of {len(examples)} examples")


def main():
    """Demo mass-scale generator"""
    print("="*70)
    print("Mass-Scale Example Generator")
    print("="*70)

    # Demo with sample compounds
    sample_compounds = [
        {
            'id': 'demo_1',
            'name': 'Aspirin',
            'properties': {
                'molecular_formula': 'C9H8O4',
                'molecular_weight': 180.16,
                'canonical_smiles': 'CC(=O)OC1=CC=CC=C1C(=O)O',
                'logp': 1.2,
                'tpsa': 63.6,
                'h_bond_donors': 1,
                'h_bond_acceptors': 4,
                'rotatable_bonds': 3,
            }
        }
    ]

    config = GenerationConfig(target_examples=100, batch_size=50)
    generator = MassScaleGenerator(config)

    output_path = Path("./test_examples.jsonl")
    count = generator.generate_from_compounds(sample_compounds, output_path)

    print(f"\n✓ Generated {count} examples")
    print(f"✓ Saved to {output_path}")


if __name__ == "__main__":
    main()

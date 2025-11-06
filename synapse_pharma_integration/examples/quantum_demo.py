#!/usr/bin/env python3
"""
Quantum Chemistry Demo
Demonstrates quantum mechanical analysis of mushroom bioactive compounds
"""

import sys
sys.path.insert(0, '../..')

from synapse_pharma_integration.quantum_chemistry import QuantumChemistryEngine


def main():
    engine = QuantumChemistryEngine()

    print("\n" + "="*80)
    print("QUANTUM CHEMISTRY ANALYSIS - MUSHROOM BIOACTIVE COMPOUNDS")
    print("Powered by Synapse-Lang + CroweLogic-Pharma")
    print("="*80)

    # Analyze Hericenone (Lion's Mane)
    print("\n1. HERICENONE A - NGF-Stimulating Compound from Lion's Mane")
    print("-"*80)
    hericenone = engine.analyze_hericenone_structure()

    print(f"\n📊 Quantum Properties:")
    print(f"   • HOMO-LUMO Gap: {hericenone['homo_lumo_gap_ev']:.3f} eV")
    print(f"   • UV Absorption λmax: {hericenone['uv_lambda_max']:.1f} nm")
    print(f"   • Dipole Moment: {hericenone['dipole_moment']:.2f} Debye")
    print(f"   • Reactivity: {hericenone['reactivity']}")
    print(f"   • Aromaticity: {hericenone['aromaticity']}")

    print(f"\n🔬 Electronic Transitions (UV-Vis):")
    for i, trans in enumerate(hericenone['electronic_transitions'][:3], 1):
        print(f"   {i}. {trans['transition']}: {trans['wavelength']:.1f} nm ({trans['energy']:.2f} eV)")

    # Analyze Ganoderic Acid (Reishi)
    print("\n\n2. GANODERIC ACID - Anti-inflammatory Compound from Reishi")
    print("-"*80)
    ganoderic = engine.analyze_ganoderic_acid_structure()

    print(f"\n📊 Quantum Properties:")
    print(f"   • HOMO-LUMO Gap: {ganoderic['homo_lumo_gap_ev']:.3f} eV")
    print(f"   • UV Absorption λmax: {ganoderic['uv_lambda_max']:.1f} nm")
    print(f"   • Target Affinity: {ganoderic['target_affinity']}")
    print(f"   • Bioactivity: {ganoderic['bioactivity']}")

    print(f"\n🔬 Electronic Transitions (UV-Vis):")
    for i, trans in enumerate(ganoderic['electronic_transitions'][:3], 1):
        print(f"   {i}. {trans['transition']}: {trans['wavelength']:.1f} nm ({trans['energy']:.2f} eV)")

    # Comparison
    print("\n\n3. COMPARATIVE ANALYSIS")
    print("-"*80)
    print(f"\n{'Property':<25} {'Hericenone A':<20} {'Ganoderic Acid':<20}")
    print("-"*65)
    print(f"{'HOMO-LUMO Gap (eV)':<25} {hericenone['homo_lumo_gap_ev']:< 20.3f} {ganoderic['homo_lumo_gap_ev']:<20.3f}")
    print(f"{'UV λmax (nm)':<25} {hericenone['uv_lambda_max']:<20.1f} {ganoderic['uv_lambda_max']:<20.1f}")
    print(f"{'Reactivity':<25} {hericenone['reactivity']:<20} {'-':<20}")
    print(f"{'Primary Target':<25} {'TrkA (NGF)':<20} {'NF-κB':<20}")

    print("\n\n" + "="*80)
    print("✓ Quantum chemistry analysis complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

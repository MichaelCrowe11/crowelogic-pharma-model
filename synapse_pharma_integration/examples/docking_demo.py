#!/usr/bin/env python3
"""
Molecular Docking Demo
Demonstrates protein-ligand docking simulations for drug discovery
"""

import sys
sys.path.insert(0, '../..')

from synapse_pharma_integration.molecular_simulator import MolecularSimulator


def main():
    simulator = MolecularSimulator()

    print("\n" + "="*80)
    print("MOLECULAR DOCKING SIMULATION - DRUG DISCOVERY")
    print("Powered by Synapse-Lang + CroweLogic-Pharma")
    print("="*80)

    # Hericenone docking
    print("\n1. HERICENONE A → TrkA (NGF Receptor)")
    print("-"*80)
    hericenone_results = simulator.simulate_hericenone_docking()

    print(f"\n🎯 Docking Results:")
    print(f"   • Docking Score: {hericenone_results['docking_score']:.2f} kcal/mol")
    print(f"   • Predicted Kd: {hericenone_results['predicted_Kd_nM']:.1f} nM")
    print(f"   • Predicted Ki: {hericenone_results['predicted_Ki_nM']:.1f} nM")
    print(f"   • Predicted IC50: {hericenone_results['predicted_IC50_nM']:.1f} nM")
    print(f"   • pKi: {hericenone_results['pKi']:.2f}")

    print(f"\n💊 ADME Properties:")
    adme = hericenone_results['adme_properties']
    print(f"   • Drug-likeness: {adme['drug_likeness']}")
    print(f"   • Lipinski Violations: {adme['lipinski_violations']}/4")
    print(f"   • Oral Bioavailability: {'✓ Yes' if adme['oral_bioavailability'] else '✗ No'}")
    print(f"   • BBB Penetration: {'✓ Yes' if adme['bbb_penetration'] else '✗ No'}")
    print(f"   • P-gp Substrate: {'Yes' if adme['pgp_substrate'] else 'No'}")
    print(f"   • TPSA: {adme['tpsa']:.1f} Ų")

    print(f"\n🔬 Mechanism:")
    print(f"   • {hericenone_results['mechanism']}")
    print(f"   • Therapeutic: {hericenone_results['therapeutic_potential']}")

    # Ganoderic Acid docking
    print("\n\n2. GANODERIC ACID A → NF-κB p65")
    print("-"*80)
    ganoderic_results = simulator.simulate_ganoderic_acid_docking()

    print(f"\n🎯 Docking Results:")
    print(f"   • Docking Score: {ganoderic_results['docking_score']:.2f} kcal/mol")
    print(f"   • Predicted Kd: {ganoderic_results['predicted_Kd_nM']:.1f} nM")
    print(f"   • Predicted Ki: {ganoderic_results['predicted_Ki_nM']:.1f} nM")
    print(f"   • Predicted IC50: {ganoderic_results['predicted_IC50_nM']:.1f} nM")
    print(f"   • pKi: {ganoderic_results['pKi']:.2f}")

    print(f"\n💊 ADME Properties:")
    adme = ganoderic_results['adme_properties']
    print(f"   • Drug-likeness: {adme['drug_likeness']}")
    print(f"   • Lipinski Violations: {adme['lipinski_violations']}/4")
    print(f"   • Oral Bioavailability: {'✓ Yes' if adme['oral_bioavailability'] else '✗ No'}")
    print(f"   • BBB Penetration: {'✓ Yes' if adme['bbb_penetration'] else '✗ No'}")
    print(f"   • TPSA: {adme['tpsa']:.1f} Ų")

    print(f"\n🔬 Mechanism:")
    print(f"   • {ganoderic_results['mechanism']}")
    print(f"   • Therapeutic: {ganoderic_results['therapeutic_potential']}")

    # Comparison
    print("\n\n3. HEAD-TO-HEAD COMPARISON")
    print("-"*80)
    comparison = simulator.compare_compounds([hericenone_results, ganoderic_results])

    print(f"\n🏆 Best Binder: {comparison['best_binder']}")
    print(f"   Score: {comparison['best_docking_score']:.2f} kcal/mol")

    print(f"\n📊 Ranking:")
    for rank_data in comparison['ranking']:
        print(f"   {rank_data['rank']}. {rank_data['compound']}")
        print(f"      Target: {rank_data['target']}")
        print(f"      Score: {rank_data['docking_score']:.2f} kcal/mol")
        print(f"      Ki: {rank_data['predicted_Ki_nM']:.1f} nM")
        print(f"      Drug-likeness: {rank_data['drug_likeness']}\n")

    print("\n" + "="*80)
    print("✓ Molecular docking simulation complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

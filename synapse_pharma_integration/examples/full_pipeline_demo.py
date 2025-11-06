#!/usr/bin/env python3
"""
Complete Drug Discovery Pipeline Demo
End-to-end analysis: Quantum → Docking → AI Recommendation
"""

import sys
sys.path.insert(0, '../..')

from synapse_pharma_integration.drug_discovery_ai import DrugDiscoveryAI


def main():
    ai = DrugDiscoveryAI()

    print("\n" + "="*90)
    print(" " * 15 + "SYNAPSE-PHARMA INTEGRATED DRUG DISCOVERY AI")
    print(" " * 10 + "Quantum Computing + AI-Driven Pharmaceutical Research")
    print("="*90)

    # Hericenone Analysis
    print("\n" + "="*90)
    print("COMPOUND 1: HERICENONE A (Hericium erinaceus - Lion's Mane)")
    print("="*90)

    hericenone_analysis = ai.full_analysis('hericenone_A')

    print("\n🔬 [STEP 1: QUANTUM CHEMISTRY ANALYSIS]")
    print("-"*90)
    qp = hericenone_analysis['quantum_properties']
    print(f"   HOMO-LUMO Gap:        {qp['homo_lumo_gap_ev']:.3f} eV")
    print(f"   UV λmax:              {qp['uv_lambda_max']:.1f} nm")
    print(f"   Dipole Moment:        {qp['dipole_moment']:.2f} Debye")
    print(f"   Reactivity:           {qp['reactivity']}")
    print(f"   Aromaticity:          {qp['aromaticity']}")

    print("\n🎯 [STEP 2: MOLECULAR DOCKING]")
    print("-"*90)
    dr = hericenone_analysis['docking_results']
    print(f"   Target Protein:       {dr['target']}")
    print(f"   Docking Score:        {dr['docking_score']:.2f} kcal/mol")
    print(f"   Predicted Kd:         {dr['predicted_Kd_nM']:.1f} nM")
    print(f"   Predicted Ki:         {dr['predicted_Ki_nM']:.1f} nM")
    print(f"   Predicted IC50:       {dr['predicted_IC50_nM']:.1f} nM")
    print(f"   pKi:                  {dr['pKi']:.2f}")

    print("\n💊 [STEP 3: ADME-TOX PREDICTION]")
    print("-"*90)
    adme = dr['adme_properties']
    print(f"   Drug-likeness:        {adme['drug_likeness']}")
    print(f"   Lipinski Violations:  {adme['lipinski_violations']}/4")
    print(f"   Oral Bioavailability: {'✓ YES' if adme['oral_bioavailability'] else '✗ NO'}")
    print(f"   BBB Penetration:      {'✓ YES' if adme['bbb_penetration'] else '✗ NO'}")
    print(f"   Absorption:           {adme['absorption']}")
    print(f"   TPSA:                 {adme['tpsa']:.1f} Ų")

    print("\n🤖 [STEP 4: AI RECOMMENDATION]")
    print("-"*90)
    rec = hericenone_analysis['therapeutic_recommendation']
    print(f"   Development Potential: {rec['development_potential']}")
    print(f"   Predicted Potency:     {rec['predicted_potency']}")
    print(f"   Mechanism:             {rec['mechanism']}")
    print(f"   Clinical Applications: {rec['clinical_applications']}")

    print(f"\n   Recommended Next Steps:")
    for i, step in enumerate(rec['next_steps'], 1):
        print(f"      {i}. {step}")

    # Ganoderic Acid Analysis
    print("\n\n" + "="*90)
    print("COMPOUND 2: GANODERIC ACID A (Ganoderma lucidum - Reishi)")
    print("="*90)

    ganoderic_analysis = ai.full_analysis('ganoderic_acid_A')

    print("\n🔬 [STEP 1: QUANTUM CHEMISTRY ANALYSIS]")
    print("-"*90)
    qp = ganoderic_analysis['quantum_properties']
    print(f"   HOMO-LUMO Gap:        {qp['homo_lumo_gap_ev']:.3f} eV")
    print(f"   UV λmax:              {qp['uv_lambda_max']:.1f} nm")
    print(f"   Target Affinity:      {qp['target_affinity']}")
    print(f"   Bioactivity:          {qp['bioactivity']}")

    print("\n🎯 [STEP 2: MOLECULAR DOCKING]")
    print("-"*90)
    dr = ganoderic_analysis['docking_results']
    print(f"   Target Protein:       {dr['target']}")
    print(f"   Docking Score:        {dr['docking_score']:.2f} kcal/mol")
    print(f"   Predicted Kd:         {dr['predicted_Kd_nM']:.1f} nM")
    print(f"   Predicted Ki:         {dr['predicted_Ki_nM']:.1f} nM")
    print(f"   Predicted IC50:       {dr['predicted_IC50_nM']:.1f} nM")
    print(f"   pKi:                  {dr['pKi']:.2f}")

    print("\n💊 [STEP 3: ADME-TOX PREDICTION]")
    print("-"*90)
    adme = dr['adme_properties']
    print(f"   Drug-likeness:        {adme['drug_likeness']}")
    print(f"   Lipinski Violations:  {adme['lipinski_violations']}/4")
    print(f"   Oral Bioavailability: {'✓ YES' if adme['oral_bioavailability'] else '✗ NO'}")
    print(f"   Absorption:           {adme['absorption']}")
    print(f"   TPSA:                 {adme['tpsa']:.1f} Ų")

    print("\n🤖 [STEP 4: AI RECOMMENDATION]")
    print("-"*90)
    rec = ganoderic_analysis['therapeutic_recommendation']
    print(f"   Development Potential: {rec['development_potential']}")
    print(f"   Predicted Potency:     {rec['predicted_potency']}")
    print(f"   Mechanism:             {rec['mechanism']}")
    print(f"   Clinical Applications: {rec['clinical_applications']}")

    print(f"\n   Recommended Next Steps:")
    for i, step in enumerate(rec['next_steps'], 1):
        print(f"      {i}. {step}")

    # Final Summary
    print("\n\n" + "="*90)
    print("COMPARATIVE SUMMARY")
    print("="*90)

    h_rec = hericenone_analysis['therapeutic_recommendation']
    g_rec = ganoderic_analysis['therapeutic_recommendation']

    print(f"\n{'Metric':<30} {'Hericenone A':<30} {'Ganoderic Acid A':<30}")
    print("-"*90)
    print(f"{'Target':<30} {'TrkA (NGF Receptor)':<30} {'NF-κB p65':<30}")
    print(f"{'Predicted Ki (nM)':<30} {h_rec['predicted_Ki_nM']:<30.1f} {g_rec['predicted_Ki_nM']:<30.1f}")
    print(f"{'Potency':<30} {h_rec['predicted_potency']:<30} {g_rec['predicted_potency']:<30}")
    print(f"{'Development Potential':<30} {h_rec['development_potential']:<30} {g_rec['development_potential']:<30}")

    print("\n\n" + "="*90)
    print("✓ INTEGRATED DRUG DISCOVERY ANALYSIS COMPLETE")
    print("  Powered by Synapse-Lang Quantum Computing + CroweLogic-Pharma AI")
    print("="*90 + "\n")


if __name__ == "__main__":
    main()

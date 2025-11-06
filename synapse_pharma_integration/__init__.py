"""
Synapse-Pharma Integration Module
Combines Synapse-Lang quantum computing with CroweLogic-Pharma drug discovery
"""

__version__ = "1.0.0"
__author__ = "Michael Benjamin Crowe"

from .quantum_chemistry import QuantumChemistryEngine
from .molecular_simulator import MolecularSimulator
from .drug_discovery_ai import DrugDiscoveryAI

__all__ = [
    'QuantumChemistryEngine',
    'MolecularSimulator',
    'DrugDiscoveryAI'
]

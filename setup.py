#!/usr/bin/env python3
"""
Setup script for CroweLogic-Pharma CLI
Production-ready pharmaceutical AI research platform
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
if readme_file.exists():
    long_description = readme_file.read_text(encoding='utf-8')
else:
    long_description = "CroweLogic-Pharma: AI-Powered Pharmaceutical Research Platform"

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    requirements = [
        'click>=8.3.0',
        'rich>=14.2.0',
        'typer>=0.20.0',
        'requests>=2.32.3',
        'numpy>=1.26.4',
        'scipy>=1.13.1',
        'pandas>=2.2.2',
        'synapse-lang>=2.3.3',
        'numba>=0.62.0',
        'rdkit>=2025.9.1',
        'datasets>=2.14.0',
        'chembl-webresource-client>=0.10.8',
        'ollama>=0.4.7',
        'azure-mgmt-containerinstance>=10.1.0',
        'azure-mgmt-containerregistry>=10.3.0',
        'azure-mgmt-resource>=23.1.1',
        'azure-identity>=1.18.0',
    ]

setup(
    name='crowelogic-pharma',
    version='3.0.0',
    author='Michael Benjamin Crowe',
    author_email='michael@crowelogic.com',
    description='AI-Powered Pharmaceutical Research Platform with Quantum Computing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/michaelcrowe11/crowelogic-pharma-model',
    project_urls={
        'Documentation': 'https://github.com/michaelcrowe11/crowelogic-pharma-model',
        'Source': 'https://github.com/michaelcrowe11/crowelogic-pharma-model',
        'Tracker': 'https://github.com/michaelcrowe11/crowelogic-pharma-model/issues',
    },

    # Package configuration
    packages=find_packages(exclude=['tests', 'tests.*', 'examples', 'examples.*']),
    py_modules=['crowelogic_pharma_cli'],

    # Dependencies
    install_requires=requirements,
    python_requires='>=3.10',

    # Optional dependencies
    extras_require={
        'dev': [
            'pytest>=8.3.4',
            'pytest-cov>=6.0.0',
            'black>=24.10.0',
            'flake8>=7.1.1',
            'mypy>=1.13.0',
        ],
        'gpu': [
            'cupy-cuda12x>=13.3.0',
        ],
        'docs': [
            'sphinx>=8.1.3',
            'sphinx-rtd-theme>=3.0.2',
        ],
    },

    # CLI entry points
    entry_points={
        'console_scripts': [
            'crowelogic=crowelogic_pharma_cli:cli',
            'crowelogic-pharma=crowelogic_pharma_cli:cli',
        ],
    },

    # Package metadata
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],

    keywords='pharmaceutical ai drug-discovery quantum-computing machine-learning chemistry bioinformatics mushrooms mycology',

    # Include package data
    include_package_data=True,
    package_data={
        '': [
            '*.md',
            '*.txt',
            '*.yaml',
            '*.yml',
            '*.json',
            '*.jsonl',
        ],
    },

    # Zip safety
    zip_safe=False,
)

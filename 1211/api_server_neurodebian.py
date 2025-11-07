#!/usr/bin/env python3
"""
CroweLogic-Pharma API Server with NeuroDebian Integration
Combines pharmaceutical research with neuroscience analysis tools
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import requests
import uvicorn
import logging

# Initialize FastAPI
app = FastAPI(
    title="CroweLogic-Pharma NeuroDebian API",
    description="Pharmaceutical AI with integrated neuroscience research tools",
    version="2.0-neurodebian"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ollama configuration
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "CroweLogic-Pharma:120b-v2"

# Request models
class NeuropharmacologyQuery(BaseModel):
    compound: str = Field(..., description="Mushroom compound (e.g., hericenone_a)")
    analysis_type: str = Field("neuroprotection", description="Type: neuroprotection, neuroplasticity, cognition")
    include_imaging: bool = Field(False, description="Include neuroimaging analysis recommendations")

class ClinicalTrialNeuroimaging(BaseModel):
    compound: str
    indication: str
    imaging_modalities: Optional[List[str]] = Field(None, description="MRI, fMRI, PET, EEG")

# Helper function
def query_ollama(prompt: str, temperature: float = 0.05) -> dict:
    """Query Ollama model"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature}
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Ollama request failed: {e}")
        raise HTTPException(status_code=503, detail=f"Model service unavailable: {str(e)}")

# Standard endpoints (from original)
@app.get("/")
async def root():
    return {
        "name": "CroweLogic-Pharma NeuroDebian API",
        "version": "2.0-neurodebian",
        "description": "Pharmaceutical AI with neuroscience integration",
        "features": {
            "pharmaceutical_research": True,
            "neuroscience_tools": True,
            "neuroimaging_analysis": True,
            "clinical_trial_design": True
        },
        "neurodebian_version": "bookworm (Debian 12)",
        "available_tools": [
            "FSL (optional install)",
            "AFNI (optional install)",
            "MNE-Python",
            "NiBabel",
            "Nilearn"
        ]
    }

@app.get("/health")
async def health_check():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        response.raise_for_status()
        return {
            "status": "healthy",
            "model": MODEL_NAME,
            "neurodebian": "active",
            "neuroscience_tools": "available"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

# NEW: Neuropharmacology endpoint
@app.post("/api/neuropharmacology")
async def neuropharmacology_analysis(request: NeuropharmacologyQuery):
    """
    Specialized endpoint for neuroprotective compound analysis
    Integrates with NeuroDebian neuroscience tools
    """

    prompt = f"""Analyze the neuropharmacology of {request.compound} for {request.analysis_type}.

Provide:
1. Neurological mechanism of action
2. Target brain regions and neurotransmitter systems
3. Expected neuroimaging biomarkers
4. Clinical assessment recommendations
"""

    if request.include_imaging:
        prompt += """
5. Recommended neuroimaging protocols:
   - MRI sequences for structural changes
   - fMRI paradigms for functional connectivity
   - PET tracers for molecular imaging
   - EEG/MEG for electrophysiological assessment
"""

    try:
        result = query_ollama(prompt)

        response = {
            "compound": request.compound,
            "analysis": result.get("response", ""),
            "neuroimaging_tools": {
                "available": request.include_imaging,
                "fsl_installed": False,  # Check actual installation
                "afni_installed": False,
                "python_tools": ["nibabel", "nilearn", "mne"]
            }
        }

        return response
    except Exception as e:
        logger.error(f"Neuropharmacology analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# NEW: Clinical trial neuroimaging endpoint
@app.post("/api/clinical-trial-neuroimaging")
async def clinical_trial_neuroimaging(request: ClinicalTrialNeuroimaging):
    """
    Design neuroimaging protocols for clinical trials of mushroom compounds
    """

    modalities = request.imaging_modalities or ["MRI", "fMRI", "PET"]

    prompt = f"""Design a comprehensive neuroimaging protocol for a clinical trial evaluating {request.compound} in {request.indication}.

Include protocols for: {', '.join(modalities)}

Provide:
1. Imaging timepoints (baseline, follow-up schedule)
2. MRI sequences and parameters
3. fMRI task paradigms
4. PET tracer selection
5. Image processing pipeline recommendations
6. Statistical analysis plan for imaging biomarkers
7. NeuroDebian tools that can be used for analysis

Focus on biomarkers relevant to {request.indication} pathophysiology."""

    try:
        result = query_ollama(prompt, temperature=0.05)

        return {
            "compound": request.compound,
            "indication": request.indication,
            "imaging_protocol": result.get("response", ""),
            "recommended_tools": {
                "preprocessing": "FSL FEAT, AFNI 3dDeconvolve",
                "connectivity": "Nilearn, FSL MELODIC",
                "structural": "FSL FIRST, ANTs",
                "visualization": "FSLeyes, AFNI viewer"
            }
        }
    except Exception as e:
        logger.error(f"Neuroimaging protocol design failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# NEW: Neuroimaging data analysis endpoint
@app.post("/api/analyze-neuroimaging")
async def analyze_neuroimaging_data(
    data_path: str,
    analysis_type: str = "connectivity"
):
    """
    Analyze neuroimaging data using NeuroDebian tools

    Note: This is a placeholder - actual implementation would integrate
    with FSL, AFNI, or Python neuroimaging libraries
    """

    return {
        "status": "placeholder",
        "message": "Neuroimaging analysis endpoint - integration with FSL/AFNI coming soon",
        "suggested_workflow": {
            "preprocessing": "fsl_anat for structural, feat for fMRI",
            "analysis": f"{analysis_type} analysis using appropriate tool",
            "visualization": "Generate reports with FSLeyes/AFNI"
        },
        "data_path": data_path
    }

if __name__ == "__main__":
    logger.info("Starting CroweLogic-Pharma NeuroDebian API Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

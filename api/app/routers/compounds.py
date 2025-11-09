#!/usr/bin/env python3
"""
Compound lookup endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
import sys
import os
import time
import logging

# Add parent directory to path to import data_acquisition modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

from data_acquisition.chembl_fetcher import ChEMBLFetcher
from data_acquisition.pubchem_fetcher import PubChemFetcher

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize fetchers
chembl = ChEMBLFetcher()
pubchem = PubChemFetcher()


@router.get("/compounds/lookup")
async def lookup_compound(
    identifier: str = Query(..., description="ChEMBL ID, PubChem CID, or compound name"),
    source: str = Query("auto", description="Data source: chembl, pubchem, or auto")
):
    """
    Lookup compound by identifier

    Supports:
    - ChEMBL IDs (e.g., CHEMBL25)
    - PubChem CIDs (e.g., 2244)
    - Compound names (e.g., aspirin)
    """
    start_time = time.time()

    try:
        result = None

        # Auto-detect source
        if source == "auto":
            # Try ChEMBL ID format first
            if identifier.upper().startswith("CHEMBL"):
                source = "chembl"
            # Try PubChem CID (numeric)
            elif identifier.isdigit():
                source = "pubchem"
            # Default to name search in ChEMBL
            else:
                source = "chembl_name"

        # Fetch from ChEMBL
        if source == "chembl":
            logger.info(f"Fetching {identifier} from ChEMBL")
            result = chembl.fetch_compound(identifier)

        # Fetch from PubChem by CID
        elif source == "pubchem":
            logger.info(f"Fetching CID {identifier} from PubChem")
            cid = int(identifier)
            result = pubchem.fetch_compound(cid)

        # Search ChEMBL by name
        elif source == "chembl_name":
            logger.info(f"Searching ChEMBL for '{identifier}'")
            chembl_ids = chembl.search_by_name(identifier, limit=1)
            if chembl_ids:
                result = chembl.fetch_compound(chembl_ids[0])
            else:
                # Try PubChem name search as fallback
                logger.info(f"Trying PubChem for '{identifier}'")
                cids = pubchem.search_by_name(identifier, limit=1)
                if cids:
                    result = pubchem.fetch_compound(cids[0])

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Compound '{identifier}' not found"
            )

        processing_time = round((time.time() - start_time) * 1000, 2)

        return {
            "success": True,
            "identifier": identifier,
            "source": result.get('source', source),
            "compound": result,
            "processing_time_ms": processing_time
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error looking up compound: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error looking up compound: {str(e)}"
        )


@router.get("/compounds/chembl/{chembl_id}")
async def get_chembl_compound(chembl_id: str):
    """
    Get compound details from ChEMBL by ID

    Example: /compounds/chembl/CHEMBL25
    """
    start_time = time.time()

    try:
        result = chembl.fetch_compound(chembl_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"ChEMBL compound {chembl_id} not found"
            )

        processing_time = round((time.time() - start_time) * 1000, 2)

        return {
            "success": True,
            "chembl_id": chembl_id,
            "compound": result,
            "processing_time_ms": processing_time
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching ChEMBL compound: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching ChEMBL compound: {str(e)}"
        )


@router.get("/compounds/pubchem/{cid}")
async def get_pubchem_compound(cid: int):
    """
    Get compound details from PubChem by CID

    Example: /compounds/pubchem/2244 (aspirin)
    """
    start_time = time.time()

    try:
        result = pubchem.fetch_compound(cid)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"PubChem CID {cid} not found"
            )

        processing_time = round((time.time() - start_time) * 1000, 2)

        return {
            "success": True,
            "pubchem_cid": cid,
            "compound": result,
            "processing_time_ms": processing_time
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching PubChem compound: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching PubChem compound: {str(e)}"
        )


@router.get("/compounds/search")
async def search_compounds(
    query: str = Query(..., description="Search query (compound name)"),
    source: str = Query("chembl", description="Data source: chembl or pubchem"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results")
):
    """
    Search for compounds by name

    Returns list of matching compound IDs
    """
    start_time = time.time()

    try:
        results = []

        if source == "chembl":
            chembl_ids = chembl.search_by_name(query, limit=limit)
            results = [{"chembl_id": cid, "source": "chembl"} for cid in chembl_ids]

        elif source == "pubchem":
            cids = pubchem.search_by_name(query, limit=limit)
            results = [{"pubchem_cid": cid, "source": "pubchem"} for cid in cids]

        processing_time = round((time.time() - start_time) * 1000, 2)

        return {
            "success": True,
            "query": query,
            "source": source,
            "results": results,
            "count": len(results),
            "processing_time_ms": processing_time
        }

    except Exception as e:
        logger.error(f"Error searching compounds: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error searching compounds: {str(e)}"
        )


@router.get("/compounds/approved")
async def get_approved_drugs(
    limit: int = Query(10, ge=1, le=100, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Pagination offset")
):
    """
    Get list of FDA/EMA approved drugs from ChEMBL

    Phase 4 drugs only
    """
    start_time = time.time()

    try:
        chembl_ids = chembl.fetch_approved_drugs(limit=limit, offset=offset)

        processing_time = round((time.time() - start_time) * 1000, 2)

        return {
            "success": True,
            "results": [{"chembl_id": cid} for cid in chembl_ids],
            "count": len(chembl_ids),
            "limit": limit,
            "offset": offset,
            "processing_time_ms": processing_time
        }

    except Exception as e:
        logger.error(f"Error fetching approved drugs: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching approved drugs: {str(e)}"
        )

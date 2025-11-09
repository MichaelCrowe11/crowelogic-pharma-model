#!/usr/bin/env python3
"""
CrowePharma Intelligence API
AI-Powered Drug Intelligence Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
import time

from .routers import compounds

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Store startup time
START_TIME = time.time()

# Initialize FastAPI app
app = FastAPI(
    title="CrowePharma Intelligence API",
    description="AI-Powered Drug Intelligence Platform for pharmaceutical discovery and molecular analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(compounds.router, prefix="/api/v1", tags=["Compounds"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "CrowePharma Intelligence API",
        "tagline": "AI-Powered Drug Intelligence",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "compounds": "/api/v1/compounds",
            "search": "/api/v1/search",
            "predictions": "/api/v1/predictions"
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - START_TIME
    return {
        "status": "healthy",
        "uptime_seconds": round(uptime, 2),
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.on_event("startup")
async def startup_event():
    """Initialize resources on startup"""
    logger.info("🚀 CrowePharma Intelligence API starting up...")
    logger.info("AI-Powered Drug Intelligence Platform")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("👋 CrowePharma API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True
    )

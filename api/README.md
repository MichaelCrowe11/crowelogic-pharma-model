# CrowePharma Intelligence API

**AI-Powered Drug Intelligence Platform**

## Overview

CrowePharma is a production-ready pharmaceutical intelligence API that provides:

- **Compound Lookup**: Fetch detailed information about drugs and chemicals from ChEMBL and PubChem
- **Property Predictions**: Calculate molecular properties and ADME characteristics
- **Similarity Search**: Find structurally similar compounds
- **Drug Discovery**: AI-powered insights for pharmaceutical research

## Features

### Current (v1.0.0)
- ✅ FastAPI-based REST API
- ✅ Health monitoring endpoints
- ✅ Auto-generated interactive documentation (Swagger/ReDoc)
- ✅ CORS support for web applications
- ✅ Docker containerization
- ✅ Fly.io deployment ready

### Coming Soon
- 🚧 Compound lookup by ChEMBL ID, PubChem CID, or name
- 🚧 SMILES validation and property calculations
- 🚧 Molecular similarity search (RDKit integration)
- 🚧 AI model inference for property prediction
- 🚧 Rate limiting and API key authentication
- 🚧 PostgreSQL database integration
- 🚧 Web dashboard UI

## Quick Start

### Local Development

1. **Install dependencies:**
```bash
cd api
pip install -r requirements.txt
```

2. **Run the API:**
```bash
python3 -m uvicorn app.main:app --reload --port 8080
```

3. **Visit the docs:**
- API: http://localhost:8080
- Interactive docs: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

### Docker

```bash
cd api
docker build -t crowepharma-api .
docker run -p 8080:8080 crowepharma-api
```

### Fly.io Deployment

```bash
cd api
flyctl launch --name crowepharma-api
flyctl deploy
```

## API Endpoints

### Core Endpoints

```
GET  /                    # API information
GET  /health              # Health check
GET  /docs                # Interactive API documentation
```

### Coming Soon

```
POST /api/v1/compounds/lookup        # Lookup compound by ID or name
POST /api/v1/predictions/properties  # Predict molecular properties
POST /api/v1/search/similarity       # Find similar compounds
GET  /api/v1/search/drugs            # Search approved drugs
```

## Example Usage

### Health Check

```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "uptime_seconds": 123.45,
  "version": "1.0.0",
  "timestamp": "2025-11-09T17:11:31.966461"
}
```

### API Information

```bash
curl http://localhost:8080/
```

Response:
```json
{
  "name": "CrowePharma Intelligence API",
  "tagline": "AI-Powered Drug Intelligence",
  "version": "1.0.0",
  "status": "operational",
  "endpoints": {
    "health": "/health",
    "compounds": "/api/v1/compounds",
    "search": "/api/v1/search",
    "predictions": "/api/v1/predictions"
  }
}
```

## Architecture

```
api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── routers/             # API route handlers (coming soon)
│   ├── services/            # Business logic (coming soon)
│   ├── models/              # Database models (coming soon)
│   └── utils/               # Helper functions (coming soon)
├── tests/                   # Test suite (coming soon)
├── Dockerfile               # Container definition
├── fly.toml                 # Fly.io configuration
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Technology Stack

- **Framework**: FastAPI 0.109
- **Server**: Uvicorn (ASGI)
- **Chemistry**: RDKit, ChEMBL Web Resource Client
- **Data**: Pandas, NumPy
- **Database**: PostgreSQL (via SQLAlchemy)
- **Deployment**: Docker, Fly.io
- **Authentication**: JWT (python-jose)

## Development Roadmap

### Week 1: Core API (Current)
- [x] Project structure
- [x] FastAPI application
- [x] Docker containerization
- [x] Fly.io configuration
- [ ] Compound lookup endpoints
- [ ] ChEMBL integration

### Week 2: Chemistry Features
- [ ] SMILES validation (RDKit)
- [ ] Property calculations
- [ ] Similarity search
- [ ] PubChem integration

### Week 3: AI Model
- [ ] Train Mistral-7B on pharma data
- [ ] Model inference API
- [ ] Property prediction endpoint
- [ ] Model performance monitoring

### Week 4: Production Polish
- [ ] API authentication
- [ ] Rate limiting
- [ ] Caching layer
- [ ] Production deployment
- [ ] Web dashboard

## Contributing

This is a production platform under active development. More details coming soon.

## License

Proprietary - CrowePharma

## Contact

**CrowePharma** - AI-Powered Drug Intelligence
Website: crowepharma.com (coming soon)

---

**Status**: 🚀 Active Development
**Version**: 1.0.0
**Last Updated**: November 2025

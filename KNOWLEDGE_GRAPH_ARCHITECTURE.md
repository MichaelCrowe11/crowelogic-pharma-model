# Mycopharmacology Knowledge Graph Storage Architecture

## Storage Location & Infrastructure Design

---

## Primary Storage Locations

### 1. **Azure PostgreSQL Flexible Server** (Production)
**Location**: East US (Primary), West US 2 (Backup)

```
📍 Primary: East US Azure Data Center
   └─ Azure Database for PostgreSQL Flexible Server
      ├─ Database: mycopharmacology_kg
      ├─ Size: 500GB initial (auto-scale to 16TB)
      ├─ Compute: GP_Gen5_8 (8 vCores, 32GB RAM)
      ├─ Backup: Geo-redundant (7-35 day retention)
      └─ High Availability: Zone-redundant
```

**Connection String**:
```
Host: crowelogic-pharma-pg.postgres.database.azure.com
Port: 5432
Database: mycopharmacology_kg
SSL: Required
```

**Cost**: ~$800/month
**Features**:
- Automatic backups every 5 minutes
- Point-in-time restore (up to 35 days)
- Read replicas for scaling queries
- Azure AD authentication
- Private Link support

---

### 2. **Neo4j Graph Database** (Azure VM or AKS)
**Location**: East US

```
📍 Azure Kubernetes Service (AKS)
   └─ Neo4j Community/Enterprise Edition
      ├─ Graph data for complex relationship queries
      ├─ Size: 1TB SSD
      ├─ Compute: Standard_D8s_v3 (8 vCPUs, 32GB)
      └─ Backup: Azure Blob Storage (daily)
```

**Why Neo4j**:
- Optimized for multi-hop graph traversal
- Cypher query language for complex patterns
- Visual exploration tools
- Better performance for "find all paths" queries

**Connection String**:
```
bolt://crowelogic-pharma-neo4j.eastus.cloudapp.azure.com:7687
```

**Cost**: ~$500/month
**Use Case**: Complex graph queries, visualization, path finding

---

### 3. **Azure Blob Storage** (Data Lake)
**Location**: East US (Hot tier) + Cool tier for archives

```
📍 Azure Blob Storage
   └─ Storage Account: crowelogicpharmadata
      ├─ Container: raw-data/ (cultivation CSVs, videos)
      ├─ Container: processed-data/ (cleaned, normalized)
      ├─ Container: chembl-mirror/ (ChEMBL database dumps)
      ├─ Container: pubmed-cache/ (PubMed XML/JSON)
      ├─ Container: backups/ (database backups)
      └─ Container: knowledge-graph-exports/ (JSON/RDF exports)
```

**Cost**: ~$200/month
**Redundancy**: LRS (Locally Redundant) for hot, GRS (Geo-Redundant) for backups

---

### 4. **Azure Cognitive Search** (Full-Text Search)
**Location**: East US

```
📍 Azure Cognitive Search Service
   └─ Index: mushroom_literature
      ├─ 50,000+ PubMed/PMC articles indexed
      ├─ Full-text search with relevance scoring
      ├─ AI-enriched with key phrase extraction
      └─ Size: Standard S1 (15GB, 50M documents)
```

**Cost**: ~$250/month
**Use Case**: Literature search, compound mentions, target identification

---

## Data Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                            │
│  (FastAPI, CroweLogic-Pharma Model, Dashboards)                │
└────────────┬──────────────────────────────────┬─────────────────┘
             │                                  │
             │                                  │
   ┌─────────▼─────────┐              ┌────────▼─────────┐
   │  QUERY ROUTER     │              │   AI LAYER       │
   │  (GraphQL/REST)   │              │  (Ollama Model)  │
   └─────────┬─────────┘              └──────────────────┘
             │
   ┌─────────┴──────────────────────────────────────┐
   │                                                 │
┌──▼──────────────┐  ┌───────────────┐  ┌──────────▼────────┐
│  PostgreSQL     │  │    Neo4j      │  │  Cognitive Search │
│  (Relational)   │  │   (Graph)     │  │  (Full-Text)      │
└────────┬────────┘  └───────┬───────┘  └────────┬──────────┘
         │                   │                     │
         │         ┌─────────┴─────────┐          │
         │         │                   │          │
      ┌──▼─────────▼────┐    ┌────────▼──────────▼─┐
      │  Azure Blob      │    │  Azure Data Lake   │
      │  (Raw Data)      │    │  (Processed Data)  │
      └──────────────────┘    └────────────────────┘
```

---

## Detailed Storage Breakdown

### PostgreSQL Schema (Structured Data)

**Database**: `mycopharmacology_kg`

**Schemas**:
```sql
-- Core mycology data
CREATE SCHEMA cultivation;    -- Cultivation runs, parameters, yields
CREATE SCHEMA compounds;       -- Mushroom compounds, properties
CREATE SCHEMA bioactivity;     -- Measured compound concentrations

-- Pharmaceutical data
CREATE SCHEMA chembl;          -- ChEMBL bioactivity data
CREATE SCHEMA uniprot;         -- Protein/target information
CREATE SCHEMA clinical;        -- Clinical trials data

-- Literature & knowledge
CREATE SCHEMA pubmed;          -- PubMed articles, abstracts
CREATE SCHEMA traditional;     -- Traditional use knowledge
CREATE SCHEMA ontologies;      -- Disease ontologies, GO terms

-- Derived/analytics
CREATE SCHEMA analytics;       -- Pre-computed views, correlations
CREATE SCHEMA ml_features;     -- Features for ML models
CREATE SCHEMA recommendations; -- Optimization recommendations
```

**Size Estimates**:
- cultivation schema: ~50GB (100K+ runs)
- compounds schema: ~10GB (10K+ compounds)
- chembl schema: ~150GB (mirror of ChEMBL v33)
- pubmed schema: ~200GB (50K+ full-text articles)
- **Total**: ~500GB initial, growing to 2-3TB

---

### Neo4j Graph Schema (Relationship Data)

**Graph Structure**:

```
(Mushroom Species) -[PRODUCES]-> (Compound)
(Compound) -[BINDS_TO]-> (Protein Target)
(Protein Target) -[IMPLICATED_IN]-> (Disease)
(Compound) -[SYNTHESIZED_IN]-> (Cultivation Run)
(Cultivation Run) -[HAS_PARAMETER]-> (Environmental Condition)
(Compound) -[MENTIONED_IN]-> (Publication)
(Publication) -[DESCRIBES]-> (Clinical Trial)
(Compound) -[SIMILAR_TO]-> (Compound)
```

**Node Types**:
- Species: ~500 nodes
- Compounds: ~10,000 nodes
- Targets: ~20,000 nodes
- Diseases: ~5,000 nodes
- Publications: ~50,000 nodes
- Cultivation Runs: ~100,000 nodes

**Relationships**: ~5 million edges

**Size**: ~100GB graph data

---

### Blob Storage Structure

```
crowelogicpharmadata/
├── raw-data/
│   ├── cultivation-videos/        (500GB - Southwest Mushrooms library)
│   ├── cultivation-logs/           (10GB - CSV/Excel files)
│   ├── laboratory-assays/          (50GB - HPLC, LC-MS data)
│   └── images/                     (100GB - microscopy, fruiting bodies)
│
├── processed-data/
│   ├── extracted-transcripts/      (5GB - Video transcriptions)
│   ├── normalized-cultivation/     (2GB - Cleaned CSV)
│   ├── compound-structures/        (1GB - MOL, SDF files)
│   └── bioactivity-data/           (10GB - Standardized assay results)
│
├── external-data/
│   ├── chembl-v33/                 (50GB - ChEMBL database dump)
│   ├── uniprot-human/              (20GB - Human proteome)
│   ├── pubmed-mycology/            (100GB - Downloaded articles)
│   └── clinicaltrials-gov/         (5GB - Trial metadata)
│
├── knowledge-graph-exports/
│   ├── monthly-snapshots/          (10GB each - JSONL, RDF)
│   ├── training-data/              (5GB - ML training examples)
│   └── public-datasets/            (20GB - Shareable subsets)
│
└── backups/
    ├── postgresql/                 (500GB - Daily backups)
    ├── neo4j/                      (100GB - Weekly backups)
    └── disaster-recovery/          (1TB - Full system state)
```

**Total Blob Storage**: ~2.5TB

---

## Geographic Distribution & Data Sovereignty

### Primary Regions
```
🌍 Production: East US (Virginia)
   ├─ PostgreSQL Primary
   ├─ Neo4j Primary
   ├─ Blob Storage Hot Tier
   └─ Cognitive Search

🌍 Backup: West US 2 (Washington)
   ├─ PostgreSQL Read Replica
   ├─ Blob Storage Geo-Replication
   └─ Disaster Recovery Site

🌍 Europe (Future): North Europe (Ireland)
   └─ GDPR-compliant data residency
```

### Data Residency Compliance
- **US Data**: Stored in US Azure regions
- **EU Data** (future): Separate Azure region for GDPR compliance
- **API Access**: Global via Azure Front Door
- **Model Inference**: Regional deployment (low latency)

---

## Access Patterns & API

### Public API Endpoints
```
https://api.crowelogic-pharma.com/kg/v1/
├── /query             (GraphQL endpoint)
├── /compounds         (Compound lookup)
├── /targets           (Target information)
├── /cultivation       (Cultivation protocols)
├── /literature        (Publication search)
└── /recommendations   (AI-powered suggestions)
```

### Authentication
- **Public Tier**: Rate-limited (100 queries/day), API key
- **Academic Tier**: OAuth2, 10K queries/month
- **Enterprise Tier**: Private Link, unlimited queries

---

## Local Development Setup

For researchers who want to run queries locally:

```bash
# Docker Compose setup
version: '3.8'
services:
  postgres:
    image: postgres:15
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: mycopharmacology_kg_dev

  neo4j:
    image: neo4j:5.13
    volumes:
      - ./data/neo4j:/data
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt

  api:
    image: crowelogic-pharma-api:latest
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - neo4j
```

**Local Data Sync**:
```bash
# Download knowledge graph snapshot (monthly)
az storage blob download \
  --account-name crowelogicpharmadata \
  --container-name knowledge-graph-exports \
  --name 2025-11-snapshot.sql.gz \
  --file ./local-kg.sql.gz

# Restore to local PostgreSQL
gunzip -c local-kg.sql.gz | psql -U postgres -d mycopharmacology_kg_dev
```

---

## Backup & Disaster Recovery

### Backup Strategy

**PostgreSQL**:
- **Continuous**: Transaction log backup every 5 minutes
- **Daily**: Full backup at 2 AM UTC
- **Weekly**: Full backup retained for 5 weeks
- **Monthly**: Archive backup retained for 12 months

**Neo4j**:
- **Daily**: Incremental backup
- **Weekly**: Full backup
- **Stored**: Azure Blob Storage (Cool tier)

**Recovery Time Objective (RTO)**: < 1 hour
**Recovery Point Objective (RPO)**: < 5 minutes

### Disaster Recovery Plan

**Scenario 1: Database Corruption**
- Point-in-time restore from transaction logs
- RTO: 15 minutes

**Scenario 2: Regional Outage (East US)**
- Failover to West US 2 read replica
- Promote to primary
- RTO: 30 minutes

**Scenario 3: Complete Data Loss**
- Restore from geo-redundant backups
- Rebuild knowledge graph from raw data
- RTO: 4-6 hours

---

## Cost Summary

### Monthly Costs

| Service | Configuration | Monthly Cost |
|---------|---------------|--------------|
| PostgreSQL Flexible Server | GP_Gen5_8, 500GB | $800 |
| Neo4j (AKS) | Standard_D8s_v3 | $500 |
| Blob Storage | 2.5TB, LRS+GRS | $200 |
| Cognitive Search | Standard S1 | $250 |
| Data Transfer | Egress, backups | $150 |
| **Total** | | **$1,900/month** |

**Annual**: ~$23,000

### Cost Optimization Options
- **Dev/Test**: Smaller instances ($500/month)
- **Reserved Instances**: 30% discount with 1-year commit
- **Spot Instances**: For batch processing (70% savings)
- **Archive Tier**: Old backups to Archive storage (90% cheaper)

---

## Scaling Plan

### Phase 1: MVP (Current)
- PostgreSQL: GP_Gen5_8
- Neo4j: Single instance
- Blob: 2.5TB
- **Cost**: $1,900/month
- **Users**: 100 concurrent

### Phase 2: Growth (6 months)
- PostgreSQL: GP_Gen5_16 + Read Replica
- Neo4j: HA Cluster (3 nodes)
- Blob: 10TB
- CDN for API caching
- **Cost**: $5,000/month
- **Users**: 1,000 concurrent

### Phase 3: Enterprise (12 months)
- PostgreSQL: Hyperscale (auto-scale)
- Neo4j: Enterprise Cluster (5 nodes)
- Blob: 50TB + Archive tier
- Global CDN + Azure Front Door
- Multiple regions (US, EU, Asia)
- **Cost**: $15,000/month
- **Users**: 10,000 concurrent

---

## Data Governance & Security

### Access Control
- **Row-Level Security**: Filter data by customer/subscription
- **Column Masking**: Hide sensitive cultivation details
- **Audit Logging**: All queries logged for compliance
- **Encryption**: At-rest (Azure Storage) and in-transit (TLS 1.3)

### Compliance
- **HIPAA** (future): For clinical trial data
- **GDPR**: EU data residency option
- **SOC 2 Type II**: Audit in progress
- **ISO 27001**: Target for Year 2

---

## Migration Path

### From Local to Azure (Current Task)

**Week 1-2**: Infrastructure Setup ✅ (In Progress)
```bash
# Currently deploying to Azure
- [x] Resource Group created
- [x] Container Registry created
- [⏳] Container Instance deploying
- [ ] PostgreSQL provisioning (next)
- [ ] Neo4j setup
- [ ] Blob storage configuration
```

**Week 3-4**: Data Migration
```bash
# Migrate existing data
1. Export local data (mushroom_knowledge_database.json, etc.)
2. Create PostgreSQL schema
3. Load cultivation data
4. Sync ChEMBL data
5. Index PubMed articles
```

**Week 5-6**: Knowledge Graph Build
```bash
# Build initial graph
python scripts/build_biomedical_knowledge_graph.py
python scripts/add_chembl_data.py
python scripts/consolidate_training_data.py
```

**Week 7-8**: Testing & Validation
```bash
# Validate deployment
- Query performance testing
- Data integrity checks
- API endpoint testing
- Model inference validation
```

---

## Monitoring & Observability

### Azure Monitor Configuration
```yaml
Metrics:
  - Database CPU usage
  - Query response times
  - Storage utilization
  - API request rates
  - Model inference latency

Alerts:
  - CPU > 80% for 10 minutes
  - Query time > 5 seconds
  - Storage > 90% capacity
  - API errors > 1% of requests
  - Model inference failure

Dashboards:
  - Knowledge graph statistics
  - Query patterns
  - User activity
  - Cost tracking
```

---

## Summary: Where Your Knowledge Graph Lives

**Primary Location**:
```
📍 Azure East US Data Center
   ├─ PostgreSQL: mycopharmacology_kg database
   ├─ Neo4j: Graph relationships
   ├─ Blob Storage: Raw data & backups
   └─ Cognitive Search: Literature index
```

**Access**:
```
🌐 API: https://api.crowelogic-pharma.com
🔐 Direct DB: crowelogic-pharma-pg.postgres.database.azure.com
📊 Dashboard: https://dashboard.crowelogic-pharma.com
```

**Redundancy**:
```
📍 Azure West US 2 (Backup)
📍 Azure Blob GRS (3 copies in each region = 6 total)
📍 Local Dev: Docker Compose setup available
```

**Current Status**:
- ⏳ Azure Container Instance deploying
- 🔜 Next: PostgreSQL & Neo4j setup (this week)
- 🔜 Knowledge graph build (next week)

---

**The knowledge graph will be production-ready in Azure within 2-3 weeks, with complete backup/disaster recovery and global API access!**

# DataNarrate - System Architecture

## Architecture Overview

DataNarrate follows a layered architecture pattern with clear separation of concerns. The system is designed for scalability, maintainability, and security.

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend Layer                      │
│  (React / Next.js)                                          │
│  - Query Interface                                          │
│  - Visualizations (Chart.js / D3.js)                        │
│  - User Management                                          │
│  - History & Saved Queries                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTPS / WebSocket
┌──────────────────────▼──────────────────────────────────────┐
│                         Backend Layer                       │
│  (FastAPI)                                                  │
│  - API Gateway                                              │
│  - Request Validation                                       │
│  - Authentication / Authorization                          │
│  - Rate Limiting                                            │
│  - Query Orchestration                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼────────┐ ┌──▼───────────┐ ┌▼───────────────────┐
│   AI Layer     │ │  Cache Layer │ │  Database Layer    │
│  (LangChain)   │ │  (Redis)     │ │  (PostgreSQL)      │
│  - NL to SQL   │ │  - Schema    │ │  - Users           │
│  - Validation  │ │  - Results   │ │  - Query History   │
│  - Insights    │ │  - Sessions  │ │  - Saved Queries   │
│  - Chart Gen   │ └──────────────┘ │  - Connections     │
└────────────────┘                  │  - Audit Logs      │
        │                           └────────────────────┘
        │
┌───────▼───────────────────────────────────────────────────┐
│              External Data Sources                        │
│  - PostgreSQL                                             │
│  - MySQL                                                  │
│  - SQL Server                                             │
│  - Snowflake                                              │
│  - BigQuery                                               │
└───────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Frontend Layer

**Technology Stack:** React, Next.js, TypeScript, Tailwind CSS, Chart.js

**Responsibilities:**
- User interface and interaction
- Natural language query input form
- Results display (tables, charts)
- Insights visualization
- Query history management
- Saved queries management
- Database connection configuration
- User authentication and profile management
- Export functionality (CSV, Excel, PNG, PDF)
- Real-time updates via WebSocket for long-running queries

### 2. Backend Layer

**Technology Stack:** FastAPI, Python, Pydantic, Uvicorn

**Responsibilities:**
- RESTful API endpoints
- Request validation and sanitization
- Authentication and authorization (JWT)
- Rate limiting and throttling
- Query orchestration and workflow management
- Database connection pooling
- Result formatting and transformation
- Error handling and logging
- WebSocket connections for real-time updates
- File export generation

### 3. AI Layer

**Technology Stack:** LangChain, OpenAI / Anthropic / Azure OpenAI, SQLAlchemy

**Responsibilities:**
- Natural Language to SQL conversion
- SQL validation and security checks
- Schema-aware query generation
- Query optimization suggestions
- Business insights generation from results
- Chart type recommendation
- Anomaly detection in data
- Trend analysis
- Query refinement suggestions

### 4. Cache Layer

**Technology Stack:** Redis

**Responsibilities:**
- Database schema caching (TTL: 1 hour)
- Frequent query results caching
- User session management
- Rate limiting counters
- API response caching
- Reducing database load
- Improving response times

### 5. Database Layer

**Technology Stack:** PostgreSQL

**Responsibilities:**
- Storing user data and profiles
- Managing query history
- Storing saved queries and tags
- Managing database connection configurations (encrypted)
- Audit logging
- Application metadata storage
- Transaction management
- Data persistence and durability

### 6. Deployment Layer

**Technology Stack:** Docker, Docker Compose, Kubernetes (optional), Nginx

**Responsibilities:**
- Containerization of all services
- Orchestration and scaling
- Load balancing
- SSL/TLS termination
- Service discovery
- Health monitoring
- Log aggregation
- Backup and restore

## Data Flow

1. User enters natural language query in frontend
2. Frontend sends request to Backend API
3. Backend validates request and authenticates user
4. Backend retrieves database schema (from Cache or Database Layer)
5. Backend sends query + schema to AI Layer
6. AI Layer generates and validates SQL
7. Backend executes SQL against external data source
8. Results are sent back to AI Layer for insights and chart recommendations
9. Backend stores query in history, caches results
10. Frontend displays results, charts, and insights

## Technology Decisions

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Backend Framework | FastAPI | High performance, async support, automatic docs, type hints |
| Frontend Framework | React + Next.js | SSR/SSG, rich ecosystem, TypeScript support |
| AI Framework | LangChain | Flexible, supports multiple LLMs, built-in utilities |
| Cache | Redis | In-memory, high performance, persistence options |
| Application DB | PostgreSQL | ACID compliance, robust features, extensibility |
| Containerization | Docker | Consistency, portability, easy scaling |

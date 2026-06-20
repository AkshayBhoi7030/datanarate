# DataNarrate - Folder Structure

## Project Root

```
DataNarrate/
├── backend/
├── frontend/
├── database/
├── docker/
├── docs/
├── .gitignore
├── README.md
└── LICENSE
```

---

## Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── dependencies.py         # Dependency injection
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── health.py       # /health endpoint
│   │   │   ├── schema.py       # /schema endpoint
│   │   │   ├── query.py        # /query endpoint
│   │   │   ├── history.py      # /history endpoint
│   │   │   ├── saved_queries.py # /saved-queries endpoint
│   │   │   └── export.py       # /export endpoint
│   │   └── deps.py             # API dependencies
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py         # Authentication, password hashing
│   │   ├── auth.py             # JWT token handling
│   │   ├── config.py           # Settings management
│   │   └── logging.py          # Logging configuration
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   ├── connection.py       # Database connection model
│   │   ├── query_history.py    # Query history model
│   │   ├── saved_query.py      # Saved query model
│   │   └── audit_log.py        # Audit log model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas
│   │   ├── connection.py       # Connection Pydantic schemas
│   │   ├── query.py            # Query Pydantic schemas
│   │   └── common.py           # Common schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── db_service.py       # Database operations
│   │   ├── connection_service.py # Connection management
│   │   ├── query_service.py    # Query orchestration
│   │   ├── export_service.py   # Export generation
│   │   └── audit_service.py    # Audit logging
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── llm_client.py       # LLM client wrapper
│   │   ├── sql_generator.py    # NL to SQL conversion
│   │   ├── sql_validator.py    # SQL validation
│   │   ├── insights_generator.py # Business insights
│   │   └── chart_recommender.py # Chart type recommendations
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py          # Database session
│   │   └── base.py             # SQLAlchemy base
│   │
│   └── utils/
│       ├── __init__.py
│       ├── encryption.py       # Encryption utilities
│       ├── validators.py       # Input validators
│       └── helpers.py          # Helper functions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   ├── test_api/               # API tests
│   ├── test_services/          # Service tests
│   └── test_ai/                # AI module tests
│
├── alembic/
│   ├── versions/               # Database migrations
│   ├── env.py
│   └── script.py.mako
│
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── alembic.ini
└── README.md
```

### Backend Folder Responsibilities

| Folder | Purpose |
|--------|---------|
| `app/api/` | API route definitions |
| `app/core/` | Core utilities (security, auth, config) |
| `app/models/` | SQLAlchemy ORM models |
| `app/schemas/` | Pydantic request/response schemas |
| `app/services/` | Business logic layer |
| `app/ai/` | AI/LLM integration modules |
| `app/db/` | Database setup and session management |
| `app/utils/` | Helper utilities and functions |
| `tests/` | Unit and integration tests |
| `alembic/` | Database migration files |

---

## Frontend Structure

```
frontend/
├── public/
│   ├── favicon.ico
│   └── index.html
│
├── src/
│   ├── main.tsx                # Application entry point
│   ├── App.tsx                 # Root component
│   ├── vite-env.d.ts
│   │
│   ├── components/
│   │   ├── common/             # Reusable components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── Loader.tsx
│   │   ├── query/
│   │   │   ├── QueryInput.tsx
│   │   │   ├── QueryResults.tsx
│   │   │   └── SQLViewer.tsx
│   │   ├── charts/
│   │   │   ├── BarChart.tsx
│   │   │   ├── LineChart.tsx
│   │   │   ├── PieChart.tsx
│   │   │   └── ChartContainer.tsx
│   │   ├── connections/
│   │   │   ├── ConnectionList.tsx
│   │   │   └── ConnectionForm.tsx
│   │   ├── history/
│   │   │   └── HistoryList.tsx
│   │   └── saved/
│   │       └── SavedQueries.tsx
│   │
│   ├── pages/
│   │   ├── Home.tsx
│   │   ├── Login.tsx
│   │   ├── Dashboard.tsx
│   │   ├── QueryPage.tsx
│   │   ├── HistoryPage.tsx
│   │   └── SettingsPage.tsx
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useQuery.ts
│   │   ├── useConnections.ts
│   │   └── useHistory.ts
│   │
│   ├── services/
│   │   ├── api.ts              # API client setup
│   │   ├── auth.ts             # Auth API calls
│   │   ├── query.ts            # Query API calls
│   │   ├── connections.ts      # Connection API calls
│   │   └── export.ts           # Export API calls
│   │
│   ├── store/
│   │   ├── index.ts            # Zustand store
│   │   ├── slices/
│   │   │   ├── authSlice.ts
│   │   │   ├── querySlice.ts
│   │   │   └── connectionSlice.ts
│   │
│   ├── types/
│   │   ├── index.ts
│   │   ├── user.ts
│   │   ├── connection.ts
│   │   └── query.ts
│   │
│   ├── utils/
│   │   ├── constants.ts
│   │   ├── formatters.ts
│   │   └── validators.ts
│   │
│   ├── styles/
│   │   ├── globals.css
│   │   └── themes.ts
│   │
│   └── assets/
│       ├── images/
│       └── icons/
│
├── tests/
│   ├── unit/
│   └── e2e/
│
├── .env.example
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── README.md
```

### Frontend Folder Responsibilities

| Folder | Purpose |
|--------|---------|
| `components/` | React components (common, query, charts, etc.) |
| `pages/` | Page-level components |
| `hooks/` | Custom React hooks |
| `services/` | API service calls |
| `store/` | State management (Zustand) |
| `types/` | TypeScript type definitions |
| `utils/` | Utility functions and constants |
| `styles/` | Global styles and themes |
| `assets/` | Static assets (images, icons) |
| `tests/` | Unit and E2E tests |

---

## Database Structure

```
database/
├── migrations/
│   ├── 001_create_users_table.sql
│   ├── 002_create_connections_table.sql
│   ├── 003_create_query_history_table.sql
│   ├── 004_create_saved_queries_table.sql
│   └── 005_create_audit_logs_table.sql
│
├── sample_data/
│   ├── e_commerce_schema.sql
│   └── e_commerce_data.sql
│
└── scripts/
    ├── init_db.sh
    └── backup.sh
```

### Database Folder Responsibilities

| Folder | Purpose |
|--------|---------|
| `migrations/` | SQL migration scripts |
| `sample_data/` | Sample dataset schema and data |
| `scripts/` | Database administration scripts |

---

## Docker Structure

```
docker/
├── backend/
│   └── Dockerfile
├── frontend/
│   └── Dockerfile
├── postgres/
│   └── init.sql
├── redis/
│   └── redis.conf
├── .env.example
├── docker-compose.yml
└── docker-compose.prod.yml
```

### Docker Folder Responsibilities

| Folder | Purpose |
|--------|---------|
| `backend/` | Backend Dockerfile |
| `frontend/` | Frontend Dockerfile |
| `postgres/` | PostgreSQL initialization |
| `redis/` | Redis configuration |
| `docker-compose.yml` | Local development orchestration |
| `docker-compose.prod.yml` | Production orchestration |

---

## Docs Structure

```
docs/
├── 01_PRD.md
├── 02_System_Architecture.md
├── 03_Database_Design.md
├── 04_Sample_Business_Dataset.md
├── 05_ER_Diagram.md
├── 06_API_Design.md
├── 07_Folder_Structure.md
├── 08_Security_Plan.md
├── 09_Development_Roadmap.md
└── 10_Acceptance_Criteria.md
```

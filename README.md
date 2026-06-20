<div align="center">
  <img src="https://coresg-normal.trae.ai/api/ide/v1/text-to-image?prompt=modern%20AI%20analytics%20dashboard%20logo%20with%20data%20visualization%20elements%20and%20dark%20theme&image_size=square" alt="DataNarrate Logo" width="140" height="140">
  <h1>DataNarrate</h1>
  <p><strong>AI-Powered Natural Language Analytics Platform</strong></p>
  <p><i>Turn questions into insights with AI-powered SQL, automated visualizations, and intelligent reports</i></p>

  <p>
    <a href="#-features">Features</a> •
    <a href="#-architecture">Architecture</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-deployment">Deployment</a> •
    <a href="#-tech-stack">Tech Stack</a>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.12-blue?style=flat-square" alt="Python 3.12">
    <img src="https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square" alt="FastAPI">
    <img src="https://img.shields.io/badge/React-18-blue?style=flat-square" alt="React">
    <img src="https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square" alt="PostgreSQL">
    <img src="https://img.shields.io/badge/Redis-7-red?style=flat-square" alt="Redis">
    <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License">
    <img src="https://img.shields.io/badge/Status-Production-green?style=flat-square" alt="Status">
  </p>
</div>

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [AI Features](#-ai-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Environment Variables](#-environment-variables)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Folder Structure](#-folder-structure)
- [Deployment Guide](#-deployment-guide)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**DataNarrate** is a production-grade SaaS platform that transforms natural language questions into actionable insights. Built with modern technologies and enterprise-grade security, it empowers non-technical users to query databases, generate visualizations, and get AI-powered insights without writing a single line of SQL.

### Business Value
- **Reduce Dependency on Data Teams**: Empower business users to self-serve analytics
- **Faster Decision Making**: Get insights in seconds instead of hours
- **Reduce Costs**: Lower analytics operations cost by 60%
- **Improve Accessibility**: Democratize data access across the organization

---

## ✨ Features

### Core Features
- 🤖 **Natural Language to SQL**: Ask questions in plain English → get production-ready SQL
- 📊 **Automatic Visualizations**: Charts, graphs, and tables generated automatically
- 💾 **Query History & Saved Queries**: Track and reuse your analytics
- 📄 **Export & Reporting**: Download as CSV, Excel, or generate PDF reports
- ⚡ **High Performance**: Redis caching, optimized queries, fast inference
- 🔒 **Enterprise Security**: SQL validation, secure data handling, RBAC ready
- 📈 **Usage Analytics**: Track queries, performance, and user behavior
- 📱 **Responsive UI**: Beautiful interface that works on all devices

### Advanced Features
- 🎨 **Smart Chart Engine**: Auto-detects best visualization type (line, bar, pie, scatter)
- 📊 **KPI Dashboard**: Real-time key performance indicators
- 🔍 **Schema Explorer**: Browse database tables and columns
- ⚙️ **User Preferences**: Customize your experience

---

## 🤖 AI Features

DataNarrate uses cutting-edge AI to deliver intelligent analytics:

### 1. AI SQL Generation
- Uses OpenRouter (primary) + Ollama (fallback)
- Schema-aware query generation
- Automatic SQL validation
- Fallback to rule-based generation for common queries

### 2. AI Insight Generation
- Executive summaries of query results
- Key insights and trends
- Top/low performer analysis
- Recommendations for further analysis
- Context-aware business explanations

### 3. Smart Visualizations
- Column type detection (numeric, categorical, date)
- Chart type recommendation
- Automatic sorting and filtering
- Responsive, interactive charts

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Frontend (React + Vite)                        │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐              │
│  │   Dashboard   │  │ Query Console │  │ Saved Queries │              │
│  └───────────────┘  └───────────────┘  └───────────────┘              │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │ HTTPS / REST API
┌─────────────────────────────────▼───────────────────────────────────────┐
│                      FastAPI Backend (Python 3.12)                      │
│  ┌─────────────┐ ┌───────────────┐ ┌─────────────┐ ┌─────────────────┐ │
│  │   API Layer │ │  AI Agents    │ │  Services   │ │  Data Validator │ │
│  └─────────────┘ └───────────────┘ └─────────────┘ └─────────────────┘ │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
┌────────▼──────────┐  ┌──────────▼──────────┐  ┌────────▼─────────┐
│   PostgreSQL 16   │  │      Redis 7        │  │  OpenRouter /   │
│   (Primary DB)    │  │     (Cache)         │  │    Ollama (LLM) │
└───────────────────┘  └─────────────────────┘  └──────────────────┘
```

### Key Components
1. **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
2. **Backend**: FastAPI + SQLAlchemy + Pydantic
3. **AI Layer**: OpenRouter (GPT-4/3.5) + Ollama (Phi-3 fallback)
4. **Database**: PostgreSQL 16 for primary storage
5. **Cache**: Redis 7 for high-performance caching

---

## 🛠️ Tech Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| React | 18.x | UI Framework |
| TypeScript | 5.x | Type Safety |
| Vite | 5.x | Build Tool & Dev Server |
| Tailwind CSS | 3.x | Styling |
| Chart.js | 4.x | Data Visualization |
| Axios | 1.x | HTTP Client |

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.12 | Runtime |
| FastAPI | 0.115 | Web Framework |
| SQLAlchemy | 2.x | ORM |
| Pydantic | 2.x | Data Validation |
| PostgreSQL | 16 | Database |
| Redis | 7 | Cache |
| httpx | 0.x | HTTP Client |

### AI/ML
| Service | Purpose |
|---------|---------|
| OpenRouter | Primary LLM API (GPT-4, Claude) |
| Ollama | Local LLM fallback (Phi-3, Llama) |

### DevOps & Deployment
| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Docker Compose | Local Stack Orchestration |
| Vercel | Frontend Hosting |
| Railway/Render | Backend Hosting |
| Neon | Managed PostgreSQL |
| Upstash | Managed Redis |

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (recommended)
- or
- Python 3.12+, Node.js 20+, PostgreSQL 16, Redis 7

### Option 1: Docker Compose (Easiest)
```bash
# 1. Clone the repository
git clone https://github.com/your-username/datanarrate.git
cd datanarrate

# 2. Set up environment
cp .env.example .env
# Edit .env with your configuration

# 3. Start all services
docker-compose up -d --build

# 4. Open the app
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup
```bash
# Backend Setup
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m app.main

# Frontend Setup (new terminal)
cd frontend
npm install
npm run dev
```

---

## 🔐 Environment Variables

### Backend Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Yes | `sqlite:///./datanarrate.db` | PostgreSQL database URL |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Redis connection URL |
| `SECRET_KEY` | Yes | Random | JWT secret key |
| `ENVIRONMENT` | No | `development` | Environment (production/development) |
| `OPENROUTER_API_KEY` | Yes* | - | OpenRouter API key |
| `OLLAMA_URL` | No | `http://localhost:11434` | Ollama service URL |
| `LOG_LEVEL` | No | `INFO` | Log level (DEBUG/INFO/WARNING/ERROR) |
| `CORS_ORIGINS` | No | `http://localhost:3000` | Allowed CORS origins |

### Frontend Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_BASE_URL` | No | `/api/v1` | Backend API base URL |

---

## 💻 Usage

### Getting Started
1. **Ask a Question**: Type your question in natural language (e.g., "Show sales by category in Q4")
2. **View Results**: See auto-generated SQL, query results, and visualization
3. **Get Insights**: Read AI-powered analysis of your data
4. **Save & Export**: Save your query for later or export results

### Example Questions
- "Show total revenue by month"
- "Who are our top 10 customers by total spend?"
- "Compare sales across product categories this year"
- "How many orders were placed last week?"

---

## 📡 API Endpoints

### Query Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/query` | Send natural language query |

### History Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/history` | Get query history |
| `POST` | `/api/v1/history` | Add to history |
| `DELETE` | `/api/v1/history/:id` | Delete history item |

### Saved Queries Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/saved-queries` | Get saved queries |
| `POST` | `/api/v1/saved-queries` | Save a query |
| `PUT` | `/api/v1/saved-queries/:id` | Update saved query |
| `DELETE` | `/api/v1/saved-queries/:id` | Delete saved query |
| `PATCH` | `/api/v1/saved-queries/:id/favorite` | Toggle favorite |

### Export Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/exports/csv` | Export to CSV |
| `POST` | `/api/v1/exports/excel` | Export to Excel |
| `POST` | `/api/v1/exports/pdf` | Export to PDF |

### Dashboard Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/dashboard/stats` | Get KPI stats |

### Schema Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/schema` | Get database schema |

### Health Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/status` | Application status |

---

## 📁 Folder Structure

```
datanarrate/
├── backend/                    # FastAPI Backend
│   ├── app/                    # Application code
│   │   ├── agents/             # AI agents (SQL generator)
│   │   ├── api/                # API routes
│   │   ├── core/               # Core config & settings
│   │   ├── db/                 # Database setup
│   │   ├── executors/          # SQL execution
│   │   ├── explainers/         # Insight generation
│   │   ├── llm/                # LLM services (OpenRouter, Ollama)
│   │   ├── middleware/         # Middleware
│   │   ├── models/             # SQLAlchemy models
│   │   ├── prompts/            # LLM prompts
│   │   ├── rag/                # RAG for schema
│   │   ├── repositories/       # Data repositories
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic
│   │   └── validators/         # SQL validators
│   ├── scripts/                # Utility scripts
│   ├── tests/                  # Tests
│   └── requirements.txt        # Python dependencies
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API services
│   │   ├── types/              # TypeScript types
│   │   └── utils/              # Utilities
│   └── package.json            # Node.js dependencies
├── docker/                     # Docker configuration
│   ├── backend/
│   ├── frontend/
│   └── redis/
├── docs/                       # Documentation
├── .github/                    # GitHub workflows
├── docker-compose.yml          # Dev Docker stack
├── docker-compose.prod.yml     # Prod Docker stack
├── README.md                   # This file
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guidelines
└── CHANGELOG.md                # Project changelog
```

---

## 🚀 Deployment Guide

### Option 1: Vercel + Railway (Recommended)

#### Step 1: Deploy Frontend to Vercel
1. Push your code to GitHub
2. Log in to Vercel, import your repo
3. Set environment variables: `VITE_API_BASE_URL=https://your-backend.railway.app/api/v1`
4. Deploy!

#### Step 2: Deploy Backend to Railway
1. Connect GitHub repo to Railway
2. Add PostgreSQL and Redis plugins
3. Set environment variables (DATABASE_URL, REDIS_URL, etc.)
4. Deploy from main branch

#### Step 3: Database Setup (Neon)
1. Sign up at [neon.tech](https://neon.tech)
2. Create project → get connection string
3. Update `DATABASE_URL` in Railway

---

### Option 2: Render
1. Create Web Service for backend
2. Add PostgreSQL and Redis
3. Set environment variables
4. Deploy!

---

### Option 3: Self-Hosted (Docker Compose)
```bash
# Copy production env
cp .env.production.example .env.production

# Start production stack
docker-compose -f docker-compose.prod.yml up -d --build
```

---

## 🔮 Future Enhancements

### Short Term (0-3 months)
- [ ] Multi-tenant SaaS architecture
- [ ] User authentication & authorization
- [ ] Role-based access control (RBAC)
- [ ] Scheduled reports & alerts
- [ ] Advanced chart customization

### Medium Term (3-6 months)
- [ ] Multiple database connections
- [ ] Data import & upload
- [ ] Collaborative features
- [ ] Advanced AI with RAG
- [ ] Custom visualization templates

### Long Term (6+ months)
- [ ] Embeddable widgets for websites
- [ ] API for integration
- [ ] Mobile applications
- [ ] Advanced analytics & ML models
- [ ] Marketplace for dashboard templates

---

## 🤝 Contributing

Contributions are welcome and appreciated! Please see our [Contributing Guide](CONTRIBUTING.md) for more details.

### Ways to Contribute
- Report bugs & issues
- Fix bugs & submit PRs
- Improve documentation
- Suggest new features
- Share feedback

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 📞 Support

If you have questions, feedback, or need help:
- Open an [Issue](../../issues)
- Check [Documentation](docs/)

---

## 🙏 Acknowledgements

- OpenRouter for AI API
- Vercel, Railway, Neon for hosting
- All open-source contributors

---

<div align="center">
  <strong>DataNarrate - Turn Questions into Insights</strong>
  <br>
  <br>
  <i>Built with ❤️ for data lovers</i>
</div>

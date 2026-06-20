# DataNarrate - Verification Checklist

## Step 1: Initialize Git Repository
```bash
git init
git add .
git commit -m "chore: initial project setup"
```

## Step 2: Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env if needed
```

## Step 3: Start Docker Services
```bash
docker-compose up -d
```

## Step 4: Verify Docker Containers
```bash
docker ps
# Should see:
# - datanarrate-postgres (healthy)
# - datanarrate-redis (healthy)
```

## Step 5: Verify PostgreSQL Connection
```bash
docker exec -it datanarrate-postgres psql -U postgres -d datanarrate
# Should connect to the database
```

## Step 6: Verify Redis Connection
```bash
docker exec -it datanarrate-redis redis-cli ping
# Should return PONG
```

## Step 7: Set Up Backend Virtual Environment
```bash
cd backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
```

## Step 8: Set Up Frontend Dependencies
```bash
cd frontend
npm install
```

## Step 9: Verify Volumes
```bash
docker volume ls
# Should see:
# - datanarrate_postgres_data
# - datanarrate_redis_data
```

## Step 10: Initialize Git (if not done already)
```bash
git init
git add .
git commit -m "chore: initial commit"
```

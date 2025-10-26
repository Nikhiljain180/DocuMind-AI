# DocuMind AI - Docker Setup Guide

## When to Set Up Docker

### For Local Development Without Docker
You can develop without Docker, but you'll need PostgreSQL and Qdrant running locally.

### For Testing (Recommended After Checkpoint 2)
**Start Docker now** to test database connections and prepare for Checkpoint 3.

---

## Quick Start

### 1. Start Infrastructure Services

```bash
# From project root
docker-compose up postgres qdrant redis
```

This starts:
- **PostgreSQL** on port 5432 (database for users and documents)
- **Qdrant** on ports 6333/6334 (vector database for embeddings)
- **Redis** on port 6379 (for future async tasks)

### 2. Verify Services Are Running

```bash
# Check PostgreSQL
docker exec -it documind-postgres psql -U rag_user -d rag_db -c "SELECT version();"

# Check Qdrant (open in browser)
open http://localhost:6333/dashboard

# Check Redis
docker exec -it documind-redis redis-cli ping
# Should return: PONG
```

### 3. Run Database Migration (After Checkpoint 2)

```bash
cd server

# Install dependencies first
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migration
alembic upgrade head
```

### 4. Start the Backend Server

```bash
# Still in server directory with venv activated
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs to see the API documentation.

---

## Docker Setup Checklist

### Checkpoint 1 ✅
- [x] Docker Compose configured
- [x] Services defined (postgres, qdrant, redis)
- [x] Volumes for persistent data
- [x] Health checks enabled

### Checkpoint 2 ✅  
- [x] Database models created
- [x] Alembic configured
- [ ] **TODO: Run migration when Docker is started**
- [ ] Test database connection

### Checkpoint 3 (Authentication)
- Will need to test signup/signin endpoints
- Requires Docker services running

### Checkpoint 4 (Document Upload)
- Requires Docker for file storage
- Need to test upload functionality

---

## Current Status

**You can set up Docker NOW to test the backend!**

### What You Can Test Now (After Checkpoint 2):
1. Database connection
2. Creating tables with Alembic
3. Qdrant client connection
4. Server startup
5. Health check endpoints

### What You'll Test in Checkpoint 3:
1. User registration endpoint
2. User login endpoint
3. JWT token generation
4. Protected routes

---

## Development Workflow

### Option 1: Full Docker (All Services in Containers)
```bash
# Start everything
docker-compose up

# Backend: http://localhost:8000
# Frontend: http://localhost:5173 (will be ready in Checkpoint 7)
# Qdrant UI: http://localhost:6333/dashboard
```

### Option 2: Docker Only for Databases (Recommended for Development)
```bash
# Start only databases
docker-compose up postgres qdrant redis

# Run backend locally
cd server
uvicorn app.main:app --reload
```

**This is recommended** because:
- Faster code reloading
- Easier debugging
- Better IDE integration
- Can see logs in terminal

---

## Quick Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# Start specific service
docker-compose up postgres

# Restart a service
docker-compose restart postgres
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5432
lsof -i :5432

# Kill the process
kill -9 <PID>
```

### Database Connection Error
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check logs
docker-compose logs postgres
```

### Migration Errors
```bash
# Reset database
docker-compose down -v
docker-compose up postgres -d
cd server
alembic upgrade head
```

---

## Next Steps

1. **Now**: Start Docker services
2. **Now**: Run database migration
3. **Now**: Test server startup
4. **Checkpoint 3**: Implement authentication
5. **Checkpoint 3**: Test auth endpoints

---

**When you're ready to test, run:**
```bash
docker-compose up postgres qdrant redis
cd server
alembic upgrade head
uvicorn app.main:app --reload
```

Then visit: http://localhost:8000/docs


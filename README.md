# DocuMind AI 🧠📄

A full-stack AI-powered document Q&A system. Upload your documents and chat with them using AI - like ChatGPT, but for your own files!

## ✨ What It Does

- **Upload documents** (PDF, DOCX, TXT, MD, CSV, JSON) and ask questions about them
- **Smart AI responses** based on your document content
- **Secure authentication** with your own account
- **Chat history** that remembers your conversations
- **Fast document processing** with background tasks

## 🚀 Quick Setup (5 minutes)

### Prerequisites
- **Node.js 18+** ([Download](https://nodejs.org/))
- **Python 3.12** ([Download](https://www.python.org/downloads/))
- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop))
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

### Step 1: Clone & Setup Environment

```bash
# Clone the repository
git clone https://github.com/your-username/DocuMind-AI.git
cd DocuMind-AI

# Setup backend environment
cd server
cp env.example .env
# Edit .env and add your OpenAI API key

# Setup frontend environment
cd ../client
cp env.example .env
cd ..
```

### Step 2: Start Database Services

```bash
# Start PostgreSQL, Qdrant, and Redis
docker-compose up -d
```

Wait 10 seconds for services to start.

### Step 3: Setup Backend

**Terminal 1 - Backend Server:**
```bash
cd server

# Install UV (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv --python 3.12
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Setup database
alembic upgrade head

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Background Worker:**
```bash
cd server
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Start Celery worker for async tasks
celery -A app.celery_app worker --loglevel=info
```

Backend runs at: **http://localhost:8000**

### Step 4: Setup Frontend

**Terminal 3 - Frontend:**
```bash
cd client

# Install pnpm (fast package manager)
npm install -g pnpm

# Use Node.js 20 (if using nvm)
nvm use 20

# Install dependencies
pnpm install

# Start frontend
pnpm dev
```

Frontend runs at: **http://localhost:5173**

### Step 5: Use the App! 🎉

1. Open **http://localhost:5173**
2. **Sign up** for an account
3. **Upload** documents
4. **Chat** and ask questions!

## 🔄 Restart Everything

Stop all servers with **Ctrl+C** in each terminal, then:

**Restart databases:**
```bash
docker-compose restart
```

**Restart backend (Terminal 1):**
```bash
cd server
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Restart worker (Terminal 2):**
```bash
cd server
source .venv/bin/activate
celery -A app.celery_app worker --loglevel=info
```

**Restart frontend (Terminal 3):**
```bash
cd client
pnpm dev
```

## 📚 Key Features

### 🔐 Authentication
- Secure signup/login with JWT tokens
- Password encryption
- Protected routes

### 📤 Document Management
- Drag-and-drop upload
- Multiple file formats: PDF, DOCX, TXT, MD, CSV, JSON
- Up to 10MB per file
- View and delete documents

### 💬 Smart Chat
- ChatGPT-like interface
- Context-aware AI responses
- Chat history saved automatically
- Multi-line input (Shift + Enter)

### 🤖 AI Technology
- OpenAI GPT-4o-mini for responses
- Vector search with Qdrant
- Smart document chunking
- Async processing with Redis + Celery

## 🏗️ Tech Stack

**Frontend:** React 18, TypeScript, Vite, Tailwind CSS, Redux Toolkit  
**Backend:** FastAPI, Python 3.12, SQLAlchemy, LangChain  
**Databases:** PostgreSQL (user data), Qdrant (vector search), Redis (tasks)  
**AI:** OpenAI API (GPT-4o-mini, embeddings)

## 📍 Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Qdrant Dashboard | http://localhost:6333/dashboard |
| PostgreSQL | localhost:5432 |

## 🔧 Development Commands

**Backend:**
```bash
# Create database migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

**Frontend:**
```bash
# Build for production
pnpm build

# Preview production build
pnpm preview

# Type check
pnpm tsc
```

**Docker:**
```bash
# Stop all services
docker-compose down

# Fresh start (removes data)
docker-compose down -v

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart postgres
```

## 🎯 Usage Tips

### Upload Documents
1. Go to **Documents** page
2. Drag files or click to browse
3. Wait for "✅ Completed" status
4. Check the green checkmark

### Ask Questions
1. Go to **Chat** page
2. Type your question
3. Press **Enter** to send
4. Use **Shift + Enter** for new lines

### Example Questions
- "What is this document about?"
- "Summarize the main points"
- "What does it say about [topic]?"
- "Compare these documents"
- "Find all mentions of [keyword]"

## 🐛 Common Issues

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Database Connection Error
```bash
# Restart databases
docker-compose down -v
docker-compose up -d
sleep 10
cd server
alembic upgrade head
```

### Python Package Issues
```bash
cd server
source .venv/bin/activate
uv pip install --upgrade -r requirements.txt
```

### Node.js Version Issues
```bash
# Install Node 20
nvm install 20
nvm use 20

# Reinstall packages
cd client
rm -rf node_modules
pnpm install
```

### Missing OpenAI API Key
Edit `server/.env` and add:
```env
OPENAI_API_KEY=sk-your-api-key-here
```

## 📖 Documentation

- [Architecture Guide](./ARCHITECTURE.md) - System design and decisions
- [Project Plan](./PROJECT_PLAN.md) - Detailed setup and structure
- [Contributing Guide](./CONTRIBUTING.md) - How to contribute
- [Backend README](./server/README.md) - Backend docs
- [Frontend README](./client/README.md) - Frontend docs

## 🚀 Production Deployment

For production deployment using Aiven (PostgreSQL + Redis):

1. **Create Services** on [Aiven](https://aiven.io)
   - PostgreSQL service
   - Redis service

2. **Update Environment Variables:**
```env
# server/.env
POSTGRES_HOST=your-aiven-postgres-host
POSTGRES_PORT=your-aiven-postgres-port
POSTGRES_DB=defaultdb
POSTGRES_USER=avnadmin
POSTGRES_PASSWORD=your-password

REDIS_HOST=your-aiven-redis-host
REDIS_PORT=your-redis-port
REDIS_PASSWORD=your-redis-password
```

3. **Run Migrations:**
```bash
cd server
source .venv/bin/activate
alembic upgrade head
```

4. **Test Deployment:**
```bash
./scripts/test_deployment.sh
```

## 📝 License

MIT License - see [LICENSE](./LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/your-username/DocuMind-AI/issues)
- **Discussions:** [GitHub Discussions](https://github.com/your-username/DocuMind-AI/discussions)

---

**Built with ❤️ using React, FastAPI, and OpenAI**

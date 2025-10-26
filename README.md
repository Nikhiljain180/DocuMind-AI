# DocuMind AI 🧠📄

> **Status**: ✅ **PRODUCTION READY** - All Features Complete (Checkpoints 1-13) | **Next**: Deployment

A powerful full-stack Retrieval-Augmented Generation (RAG) application built with React, TypeScript, FastAPI, and vector databases. Upload your documents and get intelligent AI-powered answers based on your content - like ChatGPT, but for your own documents!

## ✨ Features

### 🔐 User Authentication
- Secure signup and signin with JWT tokens
- Password hashing with bcrypt
- Protected routes and API endpoints
- Persistent authentication state
- Clean logout functionality

### 📤 Document Management
- **Drag-and-drop** file upload with visual feedback
- Support for multiple file formats: **PDF**, **DOCX**, **TXT**, **MD**, **CSV**
- File size limit: up to 10MB per document
- Real-time upload progress indicator
- Document listing with metadata (filename, size, upload date)
- Easy document deletion

### 💬 Intelligent Chat Interface
- ChatGPT-like conversational UI
- Context-aware responses based on uploaded documents
- **Chat history persistence** - messages saved across page refreshes
- **Clear history button** - easily start fresh conversations
- Multi-line input support (Shift + Enter for new line)
- Auto-scrolling chat view
- Document status indicator
- Helpful tips and guidance

### 🔍 Advanced RAG System
- **Vector search** with Qdrant for semantic similarity
- **Chunking strategy** for efficient document processing
- **OpenAI embeddings** (text-embedding-3-small) for semantic search
- **GPT-4o-mini** for intelligent response generation
- Top-3 relevant chunks for context
- Accurate answers based on document content

## 🏗️ Architecture

```
Frontend (React + TypeScript)  →  Backend (FastAPI)  →  PostgreSQL (Auth)
                                              ↓
                                         Qdrant (Vector DB)
                                              ↓
                                         OpenAI (LLM + Embeddings)
```

## 📁 Project Structure

```
DocuMind-AI/
├── client/          # React frontend (isolated)
├── server/          # FastAPI backend (isolated)
├── docker-compose.yml
└── data/            # Uploaded documents
```

Both `client/` and `server/` are independent and can be used in separate projects.

## 🛠️ Tech Stack

### Frontend
- **React 18** with TypeScript
- **Vite** - Lightning-fast build tool
- **Tailwind CSS** - Utility-first styling
- **Redux Toolkit** - State management
- **React Router** - Client-side routing
- **React Dropzone** - Drag-and-drop file uploads
- **Axios** - HTTP client with interceptors
- **React Hot Toast** - Beautiful notifications
- **Zustand** (optional) - Lightweight state management
- **pnpm** - Fast package manager

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.12** - Latest stable version
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migrations
- **LangChain** - Document processing & RAG orchestration
- **OpenAI API** - Embeddings & chat completions
- **Qdrant Client** - Vector database operations
- **PostgreSQL** - User data & document metadata
- **Passlib + bcrypt** - Password hashing
- **python-jose** - JWT token handling
- **UV** - Fast Python package manager

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **PostgreSQL 15** - Relational database
- **Qdrant** - Vector database for embeddings
- **Redis** - Caching and async tasks (optional)

## 📦 Installation

### Prerequisites
- **Node.js 18+** (use nvm to manage versions: `nvm use 20`)
- **pnpm** - Fast package manager (`npm install -g pnpm`)
- **Python 3.12** (use uv or pyenv for version management)
- **UV** - Fast Python package manager ([Install UV](https://github.com/astral-sh/uv))
- **Docker & Docker Compose** - For infrastructure services
- **OpenAI API Key** - Get one from [OpenAI Platform](https://platform.openai.com/)

### 🚀 Quick Start (5 minutes)

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/DocuMind-AI.git
cd DocuMind-AI
```

#### 2. Set Up Environment Variables

**Backend (Required):**
```bash
cd server
cp env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
cd ..
```

**Frontend (Already configured):**
```bash
cd client
cp env.example .env
# Default: VITE_API_URL=http://localhost:8000
cd ..
```

#### 3. Start Infrastructure Services
```bash
docker-compose up postgres qdrant redis -d
```

Wait ~10 seconds for services to initialize.

#### 4. Set Up Backend
```bash
cd server

# Create virtual environment with Python 3.12
uv venv --python 3.12

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: **http://localhost:8000**

#### 5. Set Up Frontend (New Terminal)
```bash
cd client

# Ensure you're using Node.js 18+ (or 20+)
nvm use 20  # If using nvm

# Install dependencies
pnpm install

# Start the dev server
pnpm dev
```

Frontend will run at: **http://localhost:5173**

#### 6. 🎉 Start Using the App!
1. Open **http://localhost:5173** in your browser
2. **Sign up** for a new account
3. **Upload** some documents (PDF, DOCX, TXT, MD, CSV)
4. Go to **Chat** and start asking questions about your documents!

### 📍 Access Points
- **Frontend UI**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **PostgreSQL**: localhost:5432 (user: `rag_user`, db: `rag_db`)

## 🔧 Development

### Development Workflow

The recommended development setup runs infrastructure in Docker while running backend and frontend locally for faster iteration and hot-reloading.

**1. Start Infrastructure (in background):**
```bash
docker-compose up postgres qdrant redis -d
```

**2. Start Backend (Terminal 1):**
```bash
cd server
source .venv/bin/activate  # Activate your venv
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**3. Start Frontend (Terminal 2):**
```bash
cd client
pnpm dev
```

### Useful Commands

**Backend:**
```bash
# Create a new migration
cd server
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check database connection
python -c "from app.database import engine; print('Connected!' if engine else 'Failed')"
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

# Stop and remove volumes (fresh start)
docker-compose down -v

# View logs
docker-compose logs -f

# Restart a specific service
docker-compose restart postgres
```

## 🔑 Environment Variables

### Server (.env)
Key variables you need to configure:

```env
OPENAI_API_KEY=sk-your-key-here  # REQUIRED
POSTGRES_HOST=postgres
QDRANT_HOST=qdrant
JWT_SECRET_KEY=generate-strong-secret
```

See `server/.env.example` for all options.

### Client (.env)
```env
VITE_API_URL=http://localhost:8000
```

## 📚 Documentation

- [Project Plan](./PROJECT_PLAN.md) - Detailed architecture and setup guide
- [Architecture Guide](./ARCHITECTURE.md) - System architecture and design decisions
- [Development Checkpoints](./CHECKPOINT.md) - Step-by-step development milestones
- [Setup Guide](./SETUP_GUIDE.md) - GitHub upload and setup instructions
- [Frontend README](./client/README.md) - Frontend-specific documentation
- [Backend README](./server/README.md) - Backend-specific documentation

## 🎯 Usage Guide

### Step-by-Step Tutorial

1. **Create an Account**
   - Navigate to http://localhost:5173
   - Click "Sign Up"
   - Enter your email, username, and password
   - You'll be automatically logged in

2. **Upload Documents**
   - Go to the "Documents" page
   - Drag and drop files or click to select
   - Supported formats: PDF, DOCX, TXT, MD, CSV
   - Wait for upload to complete (shows progress)

3. **Start Chatting**
   - Navigate to the "Chat" page
   - Type your question in the input box
   - Press Enter to send (Shift + Enter for new line)
   - The AI will answer based on your uploaded documents
   - See source attributions showing which documents were used

4. **Manage Documents**
   - View all uploaded documents in the Documents page
   - See file size and upload date
   - Delete documents you no longer need

### Example Questions to Try

After uploading documents, try asking:
- "What is the main topic of this document?"
- "Summarize the key points"
- "What does it say about [specific topic]?"
- "Compare the information in these documents"
- "Find all mentions of [keyword]"

## 🧪 Testing

### Manual Testing
Follow the [Testing Guide](./TESTING_GUIDE.md) for comprehensive testing instructions.

### Automated Tests (Coming Soon)
```bash
# Backend tests
cd server
pytest

# Frontend tests
cd client
pnpm test
```

## 📝 License

MIT License - see [LICENSE](./LICENSE) file for details.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ using React, FastAPI, and modern AI tools**

---

## 🎯 Development Status

### ✅ Completed (Checkpoints 1-13) - ALL FEATURES COMPLETE!

**Core Application (Checkpoints 1-10):**
- ✅ **Checkpoint 1**: Project Foundation & Infrastructure
- ✅ **Checkpoint 2**: Backend Foundation & Database Setup
- ✅ **Checkpoint 3**: Authentication System (JWT, bcrypt, endpoints)
- ✅ **Checkpoint 4**: Document Upload & Processing (File handling, parsing)
- ✅ **Checkpoint 5**: Vector Embeddings & Qdrant Integration
- ✅ **Checkpoint 6**: RAG Chat System (Query, retrieval, response)
- ✅ **Checkpoint 7**: Frontend Foundation & Setup (React, Router, Redux)
- ✅ **Checkpoint 8**: Frontend Authentication UI (Login, Signup)
- ✅ **Checkpoint 9**: Document Upload UI (Drag-and-drop, listing)
- ✅ **Checkpoint 10**: Chat Interface UI (Messages, input)

**Polish & Enhancements (Checkpoints 11-13):**
- ✅ **Checkpoint 11**: Integration & UI Polish
  - ✅ Chat history persistence with localStorage
  - ✅ Clear history button with confirmation
  - ✅ Source attribution removed for cleaner UI
  - ✅ Error handling improvements

- ✅ **Checkpoint 12**: Testing & Bug Fixes
  - ✅ Manual testing complete
  - ✅ Bug fixes applied
  - ✅ Edge cases handled
  - ✅ Performance optimization

- ✅ **Checkpoint 13**: Final Polish & Documentation
  - ✅ Comprehensive README with installation guide
  - ✅ Troubleshooting section
  - ✅ Usage examples and tips
  - ✅ Code cleanup and organization

### ⏳ Next: Checkpoint 14 - Deployment (PENDING)

- [ ] Choose deployment platform (Railway, Vercel, AWS, etc.)
- [ ] Configure production environment
- [ ] Set up production databases (PostgreSQL, Qdrant, Redis)
- [ ] Build and deploy frontend
- [ ] Deploy backend API
- [ ] Set up HTTPS/SSL
- [ ] Configure monitoring and logging
- [ ] Create deployment documentation

See [CHECKPOINT.md](./CHECKPOINT.md) for detailed development roadmap and [CHECKPOINT_STATUS.md](./CHECKPOINT_STATUS.md) for current status.

---

## 🚀 What's Working Right Now

✅ **User authentication** with JWT tokens  
✅ **Document upload** with drag-and-drop (PDF, DOCX, TXT, MD, CSV)  
✅ **Document management** (list, view, delete)  
✅ **Vector embeddings** with OpenAI (text-embedding-3-small)  
✅ **Semantic search** with Qdrant vector database  
✅ **RAG chat** with GPT-4o-mini  
✅ **Chat history persistence** with localStorage (survives page refresh)  
✅ **Clear chat history** button with confirmation  
✅ **Beautiful UI** with Tailwind CSS and responsive design  
✅ **Real-time updates** with hot module reloading  
✅ **Error handling** and validation throughout  

---

## 🐛 Troubleshooting

### Common Issues

**1. `email-validator` ImportError**
```bash
cd server
source .venv/bin/activate
uv pip install email-validator==2.1.0
```

**2. Port 8000 already in use**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9
```

**3. PostgreSQL connection errors**
```bash
# Restart services
docker-compose down -v
docker-compose up postgres qdrant redis -d
```

**4. Qdrant point ID format errors**
- Fixed in the latest code (using UUID for point IDs)
- Make sure you're using the latest version

**5. Node.js version issues**
```bash
# Use Node.js 20+
nvm install 20
nvm use 20
```

### Need Help?

- Check [CHECKPOINT_STATUS.md](./CHECKPOINT_STATUS.md) for known issues
- Review [TESTING_GUIDE.md](./TESTING_GUIDE.md) for testing procedures
- Open an issue on GitHub

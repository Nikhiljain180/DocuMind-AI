# DocuMind AI

> **Status**: 🚧 Checkpoint 1 Complete - Foundation & Infrastructure Setup

A full-stack Retrieval-Augmented Generation (RAG) application built with React, TypeScript, FastAPI, and vector databases. Upload documents and get AI-powered answers based on your content.

## 🚀 Features

- **User Authentication**: Secure signup, signin, and logout with JWT tokens
- **Document Upload**: Support for PDF, DOCX, TXT, MD, CSV files (up to 10MB)
- **Intelligent Chat**: ChatGPT-like interface with context-aware responses
- **Vector Search**: Leveraging Qdrant for efficient similarity search
- **OpenAI Integration**: Using GPT-4o-mini for chat and embeddings for document search
- **Conversation History**: Stored in browser localStorage

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
- React 18 + TypeScript
- Vite
- Tailwind CSS
- Redux Toolkit + Context API
- React Dropzone
- Axios

### Backend
- FastAPI
- Python 3.11+
- SQLAlchemy
- LangChain
- OpenAI
- Qdrant
- PostgreSQL
- UV (package manager)

### Infrastructure
- Docker & Docker Compose
- PostgreSQL 15
- Qdrant Vector DB
- Redis (optional, for async tasks)

## 📦 Installation

### Prerequisites
- Node.js 18+ & pnpm
- Python 3.11+
- Docker & Docker Compose
- UV (Python package manager)
- OpenAI API Key

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd DocuMind-AI
   ```

2. **Set up environment variables**
   
   For Backend (Required):
   ```bash
   cd server
   # Copy and edit the .env file
   # IMPORTANT: Add your OpenAI API key!
   # Edit .env and set: OPENAI_API_KEY=sk-your-key-here
   cd ..
   ```
   
   For Frontend (Optional):
   ```bash
   cd client
   # .env is already configured
   cd ..
   ```

3. **Start with Docker**
   ```bash
   docker-compose up
   ```

4. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Qdrant Dashboard: http://localhost:6333/dashboard

## 🔧 Development

### Without Docker

**Start Infrastructure:**
```bash
docker-compose up postgres qdrant redis
```

**Start Backend:**
```bash
cd server
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Start Frontend:**
```bash
cd client
pnpm install
pnpm dev
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

## 🧪 Testing

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

## 🎯 Current Development Status

- ✅ Checkpoint 1: Project Foundation & Infrastructure
- ⏳ Checkpoint 2: Backend Foundation & Database Setup (Next)
- ⏳ Checkpoint 3: Authentication System
- ⏳ Checkpoint 4: Document Upload & Processing
- ⏳ Checkpoint 5: Vector Embeddings & Qdrant Integration
- ⏳ Checkpoint 6: RAG Chat System
- ⏳ Checkpoint 7: Frontend Foundation & Setup
- ⏳ Checkpoint 8: Frontend Authentication UI
- ⏳ Checkpoint 9: Document Upload UI
- ⏳ Checkpoint 10: Chat Interface UI
- ⏳ Checkpoint 11: Complete Integration & UI Polish
- ⏳ Checkpoint 12: Testing & Bug Fixes
- ⏳ Checkpoint 13: Final Polish & Documentation

See [CHECKPOINT.md](./CHECKPOINT.md) for detailed development roadmap.

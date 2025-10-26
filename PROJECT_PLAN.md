# DocuMind AI - Project Plan

## 🎯 Project Overview

A full-stack RAG (Retrieval-Augmented Generation) application with document upload, vector search, and conversational AI capabilities.

---

## 📋 Tech Stack

### Frontend (Client)
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit + Context API
- **Package Manager**: pnpm
- **HTTP Client**: Axios or Fetch API
- **File Upload**: React Dropzone
- **Build Tool**: Vite

### Backend (Server)
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Package Manager**: uv
- **Vector Embeddings**: LangChain + OpenAI
- **Vector Database**: Qdrant
- **Relational Database**: PostgreSQL
- **File Storage**: Local file system
- **Authentication**: JWT tokens

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Environment**: Python virtual environment with uv
- **Node**: Latest LTS

---

## 🏗️ Architecture Overview

```
┌─────────────────┐
│  React Client   │
│  (Port 5173)    │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI       │
│   (Port 8000)   │
└────────┬────────┘
         │
         ├──► PostgreSQL (Auth)
         │    (Port 5432)
         │
         ├──► Qdrant (Vector DB)
         │    (Port 6333)
         │
         └──► Local File System
              (./data/uploads)
```

---

## 📁 Project Structure

```
documind/
├── client/                          # React Frontend
│   ├── src/
│   │   ├── components/              # Reusable UI components
│   │   │   ├── Chat/
│   │   │   │   ├── ChatPanel.tsx
│   │   │   │   ├── MessageList.tsx
│   │   │   │   └── MessageInput.tsx
│   │   │   ├── DocumentUpload/
│   │   │   │   ├── FileUpload.tsx
│   │   │   │   └── UploadProgress.tsx
│   │   │   └── Auth/
│   │   │       ├── SignIn.tsx
│   │   │       └── SignUp.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── AuthPage.tsx
│   │   │   └── Layout.tsx
│   │   ├── store/                  # Redux Toolkit stores
│   │   │   ├── slices/
│   │   │   │   ├── authSlice.ts
│   │   │   │   ├── chatSlice.ts
│   │   │   │   └── uploadSlice.ts
│   │   │   └── store.ts
│   │   ├── context/                # React Context API
│   │   │   ├── AuthContext.tsx
│   │   │   └── SocketContext.tsx
│   │   ├── services/                # API calls
│   │   │   ├── api.ts              # Axios instance
│   │   │   ├── authService.ts
│   │   │   ├── chatService.ts
│   │   │   └── uploadService.ts
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useChat.ts
│   │   ├── utils/
│   │   │   ├── localStorage.ts
│   │   │   └── formatters.ts
│   │   ├── types/
│   │   │   ├── auth.types.ts
│   │   │   ├── chat.types.ts
│   │   │   └── document.types.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── vite.config.ts
│
├── server/                          # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── config.py                # Configuration & env vars
│   │   ├── database.py              # DB connections (PostgreSQL, Qdrant)
│   │   │
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   │
│   │   ├── schemas/                 # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   └── document.py
│   │   │
│   │   ├── api/                     # API routes
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py          # /auth/* routes
│   │   │   │   ├── chat.py          # /chat route
│   │   │   │   └── upload.py        # /upload route
│   │   │   └── dependencies.py      # Shared dependencies
│   │   │
│   │   ├── services/                 # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── document_service.py  # File processing & embedding
│   │   │   └── chat_service.py      # RAG & LLM interaction
│   │   │
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── security.py          # JWT, password hashing
│   │   │   ├── embeddings.py        # LangChain + OpenAI
│   │   │   └── file_parser.py       # Parse uploaded files
│   │   │
│   │   └── middleware/
│   │       └── auth_middleware.py
│   │
│   ├── data/
│   │   ├── uploads/                 # User uploaded files
│   │   └── .gitkeep
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_chat.py
│   │   └── test_upload.py
│   │
│   ├── requirements.txt
│   ├── pyproject.toml               # uv dependencies
│   ├── .env.example
│   └── README.md
│
├── docker/
│   ├── docker-compose.yml
│   ├── Dockerfile.client
│   ├── Dockerfile.server
│   └── .env
│
├── .gitignore
├── README.md
└── PROJECT_PLAN.md
```

---

## 🗄️ Database Schemas

### PostgreSQL (User Authentication)

#### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

#### Documents Table
```sql
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100),
    uploaded_at TIMESTAMP DEFAULT NOW(),
    vector_collection_id VARCHAR(255)  -- Qdrant collection ID
);

CREATE INDEX idx_documents_user_id ON documents(user_id);
```

### Qdrant (Vector Database)
- **Collection Name**: `user_{user_id}_documents`
- **Vector Size**: 1536 (OpenAI text-embedding-ada-002 or text-embedding-3-small)
- **Metadata**: 
  - `user_id`
  - `document_id` 
  - `chunk_index`
  - `original_filename`

---

## 🔌 API Endpoints

### Authentication (`/api/auth`)

#### POST `/api/auth/signup`
**Request:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```
**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "username": "username"
  }
}
```

#### POST `/api/auth/signin`
**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
**Response:** Same as signup

#### POST `/api/auth/logout`
**Headers:** `Authorization: Bearer <token>`
**Response:**
```json
{
  "message": "Successfully logged out"
}
```

### Document Upload (`/api/upload`)

#### POST `/api/upload`
**Headers:** 
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Body:** Form data with file

**Response:**
```json
{
  "document_id": "uuid",
  "filename": "example.pdf",
  "file_size": 1024000,
  "status": "processed",
  "message": "Document uploaded and indexed successfully"
}
```

### Chat (`/api/chat`)

#### POST `/api/chat`
**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "query": "What is in the document?",
  "conversation_id": "optional-uuid"
}
```

**Response:**
```json
{
  "answer": "Based on the document...",
  "sources": [
    {
      "document_id": "uuid",
      "filename": "example.pdf",
      "relevance_score": 0.95
    }
  ],
  "conversation_id": "uuid"
}
```

---

## 🔑 Environment Variables

### Client (`.env`)
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### Server (`.env`)
```env
# Server
APP_NAME=RAG Application
APP_ENV=development
DEBUG=true
PORT=8000
CORS_ORIGINS=http://localhost:5173

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=rag_db
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=rag_password

# Qdrant
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_HTTP_PORT=6334

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload
UPLOAD_DIR=./data/uploads
MAX_FILE_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=.pdf,.txt,.docx,.md,.csv
```

---

## 🐳 Docker Setup

### `docker-compose.yml`
```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: rag_db
      POSTGRES_USER: rag_user
      POSTGRES_PASSWORD: rag_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U rag_user"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Qdrant Vector Database
  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"
      - "6334:6334"
    volumes:
      - qdrant_data:/qdrant/storage
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  # FastAPI Server
  server:
    build:
      context: ./server
      dockerfile: ../docker/Dockerfile.server
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./server:/app
      - ./server/data:/app/data
    depends_on:
      postgres:
        condition: service_healthy
      qdrant:
        condition: service_healthy
    command: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

  # React Client
  client:
    build:
      context: ./client
      dockerfile: ../docker/Dockerfile.client
    ports:
      - "5173:5173"
    env_file:
      - .env
    volumes:
      - ./client:/app
      - /app/node_modules
    depends_on:
      - server
    command: pnpm dev

volumes:
  postgres_data:
  qdrant_data:
```

---

## 📦 Installation Steps

### 1️⃣ Initial Setup

```bash
# Create project structure
mkdir -p documind
cd documind

# Create subdirectories
mkdir -p client server data/uploads docker
```

### 2️⃣ Backend Setup (FastAPI)

```bash
cd server

# Install uv if not already installed
pip install uv

# Initialize uv project
uv init

# Create Python virtual environment
uv venv

# Activate venv (on macOS/Linux)
source .venv/bin/activate

# Or on Windows
# .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Or add dependencies one by one
uv pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic pydantic-settings
uv pip install langchain openai qdrant-client
uv pip install python-jose bcrypt python-multipart
uv pip install pytest httpx  # For testing
```

**Create `requirements.txt`:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
langchain==0.0.350
openai==1.3.7
qdrant-client==1.6.9
python-jose[cryptography]==3.3.0
bcrypt==4.1.2
python-multipart==0.0.6
python-docx==1.1.0  # For .docx parsing
PyPDF2==3.0.1       # For .pdf parsing
pytest==7.4.3
httpx==0.25.2
```

### 3️⃣ Frontend Setup (React + TypeScript)

```bash
cd client

# Install pnpm globally (if not installed)
npm install -g pnpm

# Initialize React + TypeScript + Vite project
pnpm create vite . -- --template react-ts

# Install dependencies
pnpm install

# Install additional packages
pnpm add @reduxjs/toolkit react-redux
pnpm add axios
pnpm add react-dropzone
pnpm add @headlessui/react  # For UI components

# Install dev dependencies
pnpm add -D tailwindcss postcss autoprefixer
pnpm add -D @types/react-router-dom  # If using React Router
```

**Initialize Tailwind:**
```bash
npx tailwindcss init -p
```

Update `tailwind.config.js`:
```js
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 4️⃣ Docker Setup

```bash
# Create docker-compose.yml in root
# Copy the docker-compose.yml content from above

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 5️⃣ Database Initialization

```bash
# Connect to PostgreSQL
docker exec -it documind-postgres-1 psql -U rag_user -d rag_db

# Or run migration scripts
# Create: server/alembic.ini
# Create: server/alembic/env.py

# Initialize Alembic (for migrations)
cd server
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Run migration
alembic upgrade head
```

### 6️⃣ Environment Configuration

```bash
# Server .env
cp server/.env.example server/.env
# Edit server/.env with your values

# Client .env
echo "VITE_API_URL=http://localhost:8000" > client/.env
```

---

## 🚀 Development Workflow

### Start Development

**Option 1: Docker (Recommended)**
```bash
# Start all services
docker-compose up

# Access:
# - Client: http://localhost:5173
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Qdrant UI: http://localhost:6333/dashboard
```

**Option 2: Local Development**
```bash
# Terminal 1: Start PostgreSQL & Qdrant
docker-compose up postgres qdrant

# Terminal 2: Start FastAPI
cd server
uv venv
source .venv/bin/activate
uvicorn app.main:app --reload

# Terminal 3: Start React
cd client
pnpm dev
```

### Testing

```bash
# Backend tests
cd server
pytest

# Frontend tests (if using Vitest)
cd client
pnpm test
```

---

## 📝 Development Checklist

### Phase 1: Project Setup
- [ ] Initialize project structure
- [ ] Set up Docker and docker-compose
- [ ] Configure PostgreSQL and Qdrant
- [ ] Set up environment variables
- [ ] Create database schemas

### Phase 2: Backend Development
- [ ] Configure FastAPI app
- [ ] Set up database models (SQLAlchemy)
- [ ] Implement authentication (JWT)
- [ ] Create upload endpoint
- [ ] Implement file parsing (PDF, DOCX, TXT)
- [ ] Integrate OpenAI embeddings
- [ ] Connect to Qdrant
- [ ] Create chat endpoint with RAG
- [ ] Add error handling and validation

### Phase 3: Frontend Development
- [ ] Set up React + TypeScript + Vite
- [ ] Configure Tailwind CSS
- [ ] Set up Redux Toolkit store
- [ ] Create authentication flow (SignIn, SignUp, Logout)
- [ ] Build HomePage layout
- [ ] Implement file upload component
- [ ] Create chat panel component
- [ ] Implement localStorage for conversations
- [ ] Add routing
- [ ] Style with Tailwind

### Phase 4: Integration & Testing
- [ ] Connect frontend to backend APIs
- [ ] Test authentication flow
- [ ] Test file upload
- [ ] Test chat with RAG
- [ ] Handle edge cases and errors
- [ ] Add loading states and error messages

### Phase 5: Polish & Deploy
- [ ] Add loading indicators
- [ ] Implement proper error handling
- [ ] Add responsive design
- [ ] Performance optimization
- [ ] Security audit
- [ ] Documentation
- [ ] Deployment configuration

---

## 🔧 Key Technologies Explained

### LangChain
- **Purpose**: Orchestrate LLM interactions
- **Use**: Create RAG pipeline, manage document loaders, text splitters
- **Key Classes**: `OpenAIEmbeddings`, `Qdrant`, `RetrievalQA`

### Qdrant
- **Purpose**: Vector similarity search
- **Use**: Store document embeddings, query similar chunks
- **Why**: Fast, scalable, easy to deploy

### Redux Toolkit + Context API
- **Redux**: Global state (auth, chat history, app state)
- **Context API**: Local component state (UI state, modals)

### Redis (Optional - Consider for Production)
- **Purpose**: Async task queue and caching
- **Use**: Background file processing, rate limiting, session storage
- **Recommendation**: ✅ **YES, add Redis** for better scalability
- **Why**: 
  - Async document processing (won't block API)
  - Better user experience (upload → immediate response)
  - Can handle multiple concurrent uploads
  - Rate limiting and caching capabilities

### Mem0 (Knowledge Graph)
- **Purpose**: Create interconnected knowledge graphs from documents
- **Use**: Extract entities, relationships, and semantic connections
- **Recommendation**: ❌ **Not necessary for MVP**
- **Why**: 
  - Your current RAG approach (vector similarity) is sufficient
  - Knowledge graphs are complex and add overhead
  - Can be added later if you need entity extraction and relationship mapping
  - Current design uses vector similarity which is simpler and effective

---

## 🎨 UI/UX Considerations

1. **Authentication**
   - Clean, modern forms
   - Error messages for invalid credentials
   - Success feedback

2. **Home Page**
   - Split screen layout
   - Drag-and-drop file upload
   - Real-time upload progress
   - Chat interface similar to ChatGPT
   - Scrollable chat history

3. **User Experience**
   - Loading skeletons
   - Optimistic UI updates
   - Toast notifications
   - Responsive mobile design

---

## 📚 Additional Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **LangChain Docs**: https://python.langchain.com/
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **Redux Toolkit**: https://redux-toolkit.js.org/
- **Tailwind CSS**: https://tailwindcss.com/

---

## 🔒 Security Considerations

1. **Authentication**: JWT tokens, password hashing with bcrypt
2. **File Upload**: Validate file types and size
3. **CORS**: Configure allowed origins
4. **API Rate Limiting**: Implement to prevent abuse
5. **Input Validation**: Sanitize user inputs
6. **Environment Variables**: Never commit secrets

---

## 📈 Future Enhancements

1. **Multi-user document sharing**
2. **Document versioning**
3. **Streaming responses** (SSE or WebSockets)
4. **Document preview** before upload
5. **Export chat history**
6. **Multi-language support**
7. **Advanced search filters**
8. **User dashboard with analytics**

---

## 🐛 Known Challenges

1. **File Processing**: Different formats require different parsers
2. **Chunking Strategy**: Optimal chunk size for embeddings
3. **Token Limits**: Managing context window for LLM
4. **Vector DB Scalability**: Qdrant works well for MVP
5. **CORS Configuration**: Proper setup for development and production

---

## 📞 Next Steps

1. Review this plan
2. Ask any questions or modifications needed
3. Proceed with setup commands
4. Begin implementation phase by phase

---

**Ready to start building!** 🚀


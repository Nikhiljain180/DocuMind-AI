# DocuMind AI - Architecture & Design Decisions

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│                    (React + TypeScript)                      │
│  Port 5173                                                   │
└────────────────────┬────────────────────────────────────────┘
                     │ REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                        │
│                     (FastAPI Server)                          │
│                      Port 8000                               │
└──────┬───────────────────┬───────────────────┬───────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ PostgreSQL  │  │   Qdrant    │  │    Redis    │
│ Port 5432   │  │ Port 6333   │  │ Port 6379   │
│  (Auth)     │  │ (Vectors)   │  │  (Async)    │
└─────────────┘  └─────────────┘  └─────────────┘
```

## 🎯 Design Decisions

### 1. Why Qdrant for Vector Database?

**✅ Decision**: Use Qdrant for vector similarity search

**Reasoning**:
- Excellent performance for similarity search
- Easy to deploy with Docker
- Good Python SDK
- Built-in filtering and metadata support
- Local-first, no cloud dependency for development

**Alternatives Considered**:
- **Pinecone**: Requires cloud, paid for production
- **Weaviate**: More complex setup
- **Chroma**: Less mature, smaller community

### 2. Redis - Do We Need It?

**✅ Decision**: YES, use Redis for production MVP

**Reasoning**:
- **Async Task Processing**: File uploads can be slow (>10MB files, parsing, embedding)
- **Better UX**: User gets immediate response, processing happens in background
- **Concurrency**: Handle multiple uploads simultaneously
- **Rate Limiting**: Protect API from abuse
- **Caching**: Cache expensive LLM responses

**Implementation Options**:
```python
# Option 1: Celery + Redis (Full-featured)
- Background workers for file processing
- Task queue management
- Retry mechanisms

# Option 2: Redis Queue + Task decorator (Simpler)
- Lightweight async tasks
- Less overhead than Celery
- Good for MVP
```

**Recommendation**: Start with Celery for robust async processing

### 3. Mem0 - Knowledge Graph?

**❌ Decision**: NOT needed for MVP

**Reasoning**:
- Vector similarity search is sufficient for document retrieval
- Knowledge graphs add complexity (entity extraction, relationship mapping)
- Current RAG approach works well for Q&A over documents
- Can be added later if entity/relationship queries are needed

**When to Add Mem0**:
- Need to extract entities (people, places, organizations)
- Want relationship queries (e.g., "Who knows whom?")
- Require semantic graphs for visualization
- Need to connect information across documents

**Future Enhancement**: Add Mem0 for advanced knowledge graph features

### 4. Frontend/Backend Isolation

**✅ Decision**: Complete separation

**Structure**:
```
client/          # Independent React app
server/          # Independent FastAPI app
```

**Benefits**:
- Use client in other projects
- Deploy separately (CDN for frontend, API server for backend)
- Different teams can work on each
- Frontend can consume other APIs too
- Backend can serve multiple clients (web, mobile)

**Communication**: REST API only (no shared code)

### 5. State Management - Redux + Context?

**✅ Decision**: Use both strategically

**Redux Toolkit** (Global State):
- User authentication
- Chat history
- Upload progress
- App-wide settings

**Context API** (Local State):
- Form state
- Modal states
- UI-specific interactions
- Temporary data

**Why Both?**
- Redux: Centralized, predictable, devtools
- Context: Lighter, simpler for local UI state

### 6. File Upload Strategy

**Decision**: Hybrid approach

**Synchronous (for small files <1MB)**:
- Upload → Parse → Embed → Store in DB
- Return success immediately

**Asynchronous (for large files >1MB)**:
- Upload → Return task ID
- Process in background with Celery
- WebSocket notification when complete
- OR polling endpoint for status

**Why?**
- Small files: Fast enough to do synchronously
- Large files: Can block API, needs background processing

### 7. Conversation Storage

**Decision**: Dual storage

**Browser localStorage**:
- Recent conversations (last 10)
- Immediate access, no API calls
- Works offline

**Backend Database** (future):
- Long-term storage
- Sync across devices
- Analytics

**Why localStorage First?**
- Faster, no network delay
- Works offline
- Simpler for MVP
- Can sync to backend later

## 🔧 Technology Choices Explained

### Why FastAPI?
- Modern Python web framework
- Automatic API documentation
- Type hints with Pydantic
- High performance (async/await)
- Easy to learn and use

### Why React + TypeScript?
- Type safety prevents bugs
- Component reusability
- Large ecosystem
- Excellent developer experience

### Why Tailwind CSS?
- Utility-first CSS
- Rapid UI development
- Consistent design
- Small bundle size with purging

### Why PostgreSQL?
- Robust, reliable
- ACID compliance
- Great for user auth and metadata
- Easy to set up

### Why UV for Python?
- Faster than pip
- Better dependency resolution
- Written in Rust (fast)
- Compatible with pip

### Why pnpm?
- Faster than npm/yarn
- Better disk efficiency
- Strict dependency resolution
- Growing adoption

## 📊 Data Flow

### Authentication Flow
```
1. User submits credentials
2. Frontend → POST /api/auth/signin
3. Backend validates credentials
4. Generate JWT token
5. Return token to frontend
6. Store in localStorage
7. Include in subsequent requests
```

### File Upload Flow
```
1. User selects file
2. Frontend validates size/type
3. POST /api/upload with file
4. Backend saves file to disk
5. Parse file (PDF/DOCX/TXT)
6. Split into chunks
7. Generate embeddings (OpenAI)
8. Store in Qdrant
9. Return success
```

### Chat Flow
```
1. User sends message
2. POST /api/chat with query
3. Generate embedding for query
4. Vector search in Qdrant
5. Retrieve top-k chunks
6. Build context for LLM
7. Call OpenAI with context
8. Return answer + sources
9. Display in chat
```

## 🚀 Scalability Considerations

### Current (MVP)
- Single server instance
- Local file storage
- Self-hosted databases
- Synchronous processing

### Future (Production)
- Load balancer
- Cloud storage (S3)
- Managed databases (PostgreSQL Cloud, Qdrant Cloud)
- Background workers (Celery + Redis)
- CDN for frontend
- Caching layer
- Rate limiting

## 🔒 Security Architecture

### Authentication
- JWT tokens (stateless)
- Secure password hashing (bcrypt)
- Token expiration (30 minutes)
- Refresh token strategy (future)

### Data Protection
- Environment variables for secrets
- SQL injection prevention (SQLAlchemy ORM)
- Input validation (Pydantic)
- File type/size validation
- CORS configuration

### API Security
- Rate limiting (with Redis)
- Request validation
- Error handling (no sensitive data leakage)
- HTTPS in production

## 📈 Performance Optimizations

### Backend
- Database connection pooling
- Redis caching for frequent queries
- Async file processing
- Lazy loading of models

### Frontend
- Code splitting
- Lazy loading components
- Debouncing search
- Optimistic UI updates
- Virtualized lists for chat history

## 🧪 Testing Strategy

### Backend
- Unit tests for services
- Integration tests for API
- Mock external services (OpenAI, Qdrant)

### Frontend
- Component tests
- Integration tests for flows
- E2E tests for critical paths

## 🐳 Docker Architecture

### Services
- **postgres**: User authentication data
- **qdrant**: Vector embeddings
- **redis**: Task queue and caching
- **server**: FastAPI application
- **client**: React application

### Volumes
- Persistent data for databases
- Uploaded files storage
- Application code (for hot reload)

---

**This architecture is designed to be:**
- ✅ Modular (frontend/backend separation)
- ✅ Scalable (Redis for async tasks)
- ✅ Secure (JWT, validation, CORS)
- ✅ Performant (caching, async processing)
- ✅ Maintainable (clear structure, type safety)
- ✅ Production-ready (Docker, health checks)


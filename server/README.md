# DocuMind AI - Backend

FastAPI backend for DocuMind AI with authentication, document processing, and AI-powered chat.

## 🎯 Features

- JWT-based user authentication
- Document upload and processing (PDF, DOCX, TXT, MD, CSV)
- Vector embedding generation with OpenAI
- Vector similarity search with Qdrant
- RAG-powered chat with GPT-4o-mini
- PostgreSQL for user management
- FastAPI with automatic API documentation

## 🛠️ Tech Stack

- **FastAPI** - Web framework
- **Python 3.11+** - Programming language
- **SQLAlchemy** - ORM
- **PostgreSQL** - Relational database
- **Qdrant** - Vector database
- **LangChain** - LLM orchestration
- **OpenAI** - Embeddings and chat
- **UV** - Package manager
- **JWT** - Authentication

## 📦 Installation

```bash
# Install uv (if not already installed)
pip install uv

# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key

# Run migrations (if using Alembic)
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

## 🔧 Configuration

Required environment variables in `.env`:

```env
OPENAI_API_KEY=sk-your-key-here
POSTGRES_HOST=localhost
POSTGRES_USER=rag_user
POSTGRES_PASSWORD=rag_password
POSTGRES_DB=rag_db
QDRANT_HOST=localhost
JWT_SECRET_KEY=your-secret-key
```

See `.env.example` for all available options.

## 🏗️ Project Structure

```
server/
├── app/
│   ├── main.py           # FastAPI app entry
│   ├── config.py         # Configuration
│   ├── database.py       # DB connections
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── api/              # API routes
│   ├── services/         # Business logic
│   ├── utils/            # Utilities
│   └── middleware/       # Custom middleware
├── data/
│   └── uploads/          # User uploaded files
├── tests/                # Test files
└── requirements.txt      # Python dependencies
```

## 🚀 Running the Server

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Docker
```bash
docker-compose up server
```

## 📚 API Documentation

Once the server is running:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Login user
- `POST /api/auth/logout` - Logout user

### Documents
- `POST /api/upload` - Upload and process document

### Chat
- `POST /api/chat` - Send chat message with RAG

See the full project documentation for detailed request/response formats.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_auth.py
```

## 🔐 Security

- JWT token-based authentication
- Password hashing with bcrypt
- CORS configuration
- Input validation with Pydantic
- File size and type validation
- SQL injection prevention with SQLAlchemy

## 🐳 Docker

The backend can be run with Docker:

```bash
docker-compose up server
```

## 📝 Development Workflow

1. Make changes to the code
2. Tests run automatically on save (with pytest-watch)
3. API documentation updates automatically
4. Run tests before committing

## 🔗 Standalone Usage

This backend can be used independently with any frontend or as a standalone API service.

## 📄 License

MIT License - part of the DocuMind AI application


## 🔐 Setup Steps

1. **Set up environment variables**:
   ```bash
   cp server/env.example server/.env
   cp client/env.example client/.env
   
   # Edit server/.env and add your OpenAI API key
   # OPENAI_API_KEY=sk-your-actual-key-here
   ```

2. **Initialize Git repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: DocuMind AI"
   ```

3. **Push to GitHub**:
   - Create a new repository on GitHub (name: `documind`)
   - Don't initialize with README
   - Run:
   ```bash
   git remote add origin https://github.com/your-username/documind.git
   git branch -M main
   git push -u origin main
   ```

## ⚠️ Important: Security

- ✅ `.gitignore` is configured to exclude `.env` files
- ✅ Never commit API keys or sensitive data
- ✅ Only `env.example` files are committed to version control
- ✅ Create actual `.env` files locally after cloning

---

## 📂 Project Structure

```
documind/
├── client/          # React frontend (isolated)
├── server/          # FastAPI backend (isolated)
├── docker/
└── data/
```

Both `client/` and `server/` are independent and can be used separately in other projects.

## 🐳 Docker Setup

```bash
# Start all services
docker-compose up

# Services available:
# - Frontend: http://localhost:5173
# - Backend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

## 📚 Documentation

- [README.md](./README.md) - Project overview and features
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture and design decisions
- [PROJECT_PLAN.md](./PROJECT_PLAN.md) - Detailed implementation plan
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guidelines


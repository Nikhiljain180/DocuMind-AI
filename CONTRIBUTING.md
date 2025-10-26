# Contributing to DocuMind AI

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing](#testing)
- [Project Structure](#project-structure)

## 🤝 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them grow
- Focus on constructive feedback
- Value contributions of all kinds

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/documind.git
   cd documind
   ```

3. **Set up upstream**
   ```bash
   git remote add upstream https://github.com/original-owner/documind.git
   ```

## 🛠️ Development Setup

### Prerequisites
- Node.js 18+ with pnpm
- Python 3.11+ with uv
- Docker & Docker Compose
- Git

### Initial Setup

1. **Environment Variables**
   ```bash
   # Backend
   cp server/.env.example server/.env
   # Edit server/.env with your OpenAI API key
   
   # Frontend
   cp client/.env.example client/.env
   ```

2. **Start Infrastructure**
   ```bash
   docker-compose up -d postgres qdrant redis
   ```

3. **Setup Backend**
   ```bash
   cd server
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

4. **Setup Frontend**
   ```bash
   cd client
   pnpm install
   ```

5. **Start Development Servers**
   ```bash
   # Terminal 1: Backend
   cd server && uvicorn app.main:app --reload
   
   # Terminal 2: Frontend
   cd client && pnpm dev
   ```

## ✏️ Making Changes

### Branch Strategy
- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: New features
- `fix/*`: Bug fixes
- `docs/*`: Documentation changes

### Creating a Branch
```bash
git checkout -b feature/your-feature-name
```

### Frontend Structure
```
client/src/
├── components/     # Reusable components
├── pages/          # Page components
├── store/          # Redux store
├── services/        # API services
└── utils/           # Utility functions
```

### Backend Structure
```
server/app/
├── api/            # API routes
├── services/       # Business logic
├── models/         # Database models
├── schemas/        # Pydantic schemas
└── utils/          # Utilities
```

## 💻 Code Style

### Frontend
- Use TypeScript strictly
- Follow React best practices
- Use functional components with hooks
- Use Tailwind CSS for styling
- ESLint and Prettier for formatting

### Backend
- Follow PEP 8 style guide
- Use type hints
- Docstrings for functions/classes
- Black for code formatting
- Pylint for linting

### Example
```python
# Backend
def process_document(file_path: str) -> dict:
    """
    Process uploaded document and extract text.
    
    Args:
        file_path: Path to uploaded file
        
    Returns:
        Extracted text content
    """
    # Implementation
    pass
```

```typescript
// Frontend
interface User {
  id: string;
  email: string;
  username: string;
}

const fetchUser = async (id: string): Promise<User> => {
  // Implementation
};
```

## 📝 Commit Guidelines

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### Examples
```bash
feat: add user authentication endpoint
fix: resolve file upload size validation
docs: update API documentation
refactor: improve chat service performance
```

## 🔄 Pull Request Process

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/develop
   ```

2. **Test your changes**
   ```bash
   # Backend
   cd server && pytest
   
   # Frontend
   cd client && pnpm test
   ```

3. **Create Pull Request**
   - Clear title and description
   - Reference issues
   - Add screenshots for UI changes
   - Ensure all checks pass

4. **Review Process**
   - Address feedback
   - Update PR if needed
   - Maintainers will review and merge

## 🧪 Testing

### Backend Tests
```bash
cd server
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest tests/test_auth.py # Specific test file
```

### Frontend Tests
```bash
cd client
pnpm test                 # Run all tests
pnpm test -- --coverage   # With coverage
```

### Test Guidelines
- Write tests for new features
- Maintain >80% code coverage
- Test both success and error cases
- Mock external services

## 📊 Project Structure

```
documind/
├── client/          # React frontend
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── store/
│       └── services/
├── server/           # FastAPI backend
│   └── app/
│       ├── api/
│       ├── services/
│       └── models/
├── docker/           # Docker configs
├── docs/             # Documentation
└── tests/            # Integration tests
```

## 🐛 Reporting Bugs

Create an issue with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

## 💡 Suggesting Features

Open a feature request with:
- Clear description
- Use case
- Possible implementation approach
- Benefits

## 📚 Documentation

- Update README for major changes
- Add inline code comments
- Update API documentation
- Keep `.env.example` files updated

## 🔍 Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No console.logs or print statements
- [ ] Environment variables are documented
- [ ] No sensitive data in code

## 🤔 Questions?

- Open a discussion
- Check existing issues
- Contact maintainers

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** 🙏


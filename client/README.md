# DocuMind AI - Frontend

A modern React + TypeScript frontend for DocuMind AI with authentication, document upload, and AI-powered chat.

## 🎯 Features

- User authentication (Sign In / Sign Up / Logout)
- Document upload with drag-and-drop
- AI chat interface with conversation history
- Responsive design with Tailwind CSS
- State management with Redux Toolkit + Context API

## 🛠️ Tech Stack

- **React 18** with TypeScript
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Redux Toolkit** - Global state
- **Context API** - Local state
- **Axios** - HTTP client
- **React Dropzone** - File uploads
- **pnpm** - Package manager

## 📦 Installation

```bash
# Install dependencies
pnpm install

# Start development server
pnpm dev

# Build for production
pnpm build

# Preview production build
pnpm preview
```

## 🔧 Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Required environment variables:
```env
VITE_API_URL=http://localhost:8000
```

## 🏗️ Project Structure

```
client/
├── src/
│   ├── components/       # Reusable UI components
│   ├── pages/            # Page components
│   ├── store/            # Redux store and slices
│   ├── context/          # React contexts
│   ├── services/         # API services
│   ├── hooks/            # Custom React hooks
│   ├── utils/            # Utility functions
│   └── types/            # TypeScript types
├── public/
└── package.json
```

## 🚀 Usage

This frontend can be used standalone or with the backend. It communicates with the FastAPI backend via REST API.

### Without Backend
The frontend will work in development mode but API calls will fail without a running backend.

### With Backend
Make sure the backend is running on the URL specified in `.env`.

## 📝 Development

```bash
# Install dependencies
pnpm install

# Run development server
pnpm dev

# Run tests
pnpm test

# Lint code
pnpm lint

# Build for production
pnpm build
```

## 🔗 API Integration

The frontend expects the following API endpoints:

- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/upload` - File upload
- `POST /api/chat` - Chat endpoint

See the backend README for API documentation.

## 📄 License

MIT License - part of the DocuMind AI application


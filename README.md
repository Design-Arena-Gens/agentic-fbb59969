# PerplexiPlay - Agent Playground and Testing Environment

> Open-source platform to build, test & benchmark agentic AI agents using CrewAI, Langchain, and OpenAI.

## Features

### 🔐 Authentication & Authorization
- JWT-based authentication with access and refresh tokens
- Secure password hashing with bcrypt
- Token revocation system
- User registration, login, logout, and token refresh endpoints

### 🤖 Agent Management
- Create, read, update, and delete AI agents
- Support for multiple frameworks:
  - **CrewAI** - Multi-agent collaboration framework
  - **Langchain** - Building applications with LLMs
  - **OpenAI** - Direct OpenAI API integration
- JSON-based agent configuration
- Framework validation

### 🧪 Experiment System
- Run experiments with configured agents
- Track experiment status (pending, running, completed, failed)
- Store experiment results and errors
- Async background task execution
- Real-time status monitoring

## Tech Stack

**Frontend:** Next.js 14, TypeScript, Tailwind CSS, Zustand, React Hook Form, Axios
**Backend:** FastAPI, SQLAlchemy, PostgreSQL/SQLite, Pydantic, JWT, Bcrypt
**AI:** CrewAI, Langchain, OpenAI

## Quick Start

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Run with Docker
docker-compose up --build

# Or run separately
uvicorn backend.main:app --reload --port 8000
npm run dev
```

Access: http://localhost:3000

# PerplexiPlay Architecture

## System Overview

PerplexiPlay is a full-stack platform for building and testing AI agents. The architecture follows a modern three-tier design with clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  (Next.js 14 + React + TypeScript + Tailwind CSS)          │
│  - Pages: Auth, Dashboard, Agent Management                 │
│  - State: Zustand (Auth, User Data)                         │
│  - API Client: Axios with interceptors                      │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS/REST API
┌────────────────────┴────────────────────────────────────────┐
│                     Application Layer                        │
│              (FastAPI + Python 3.11)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Routes                                           │  │
│  │  - /auth/*     - Authentication & JWT                 │  │
│  │  - /agents/*   - Agent CRUD operations               │  │
│  │  - /experiments/* - Experiment management            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Logic                                       │  │
│  │  - Agent Engine (CrewAI, Langchain, OpenAI)          │  │
│  │  - JWT Security (Access + Refresh tokens)            │  │
│  │  - Background Tasks (Async execution)                │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │ SQLAlchemy ORM
┌────────────────────┴────────────────────────────────────────┐
│                      Data Layer                              │
│         (PostgreSQL/SQLite + SQLAlchemy)                    │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Tables                                               │  │
│  │  - users: User accounts & preferences                 │  │
│  │  - agent_configs: AI agent configurations            │  │
│  │  - experiments: Execution records & results           │  │
│  │  - revoked_tokens: JWT blacklist                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Architecture

**Technology Stack:**
- Next.js 14 (App Router)
- React 18 with TypeScript
- Tailwind CSS for styling
- Zustand for state management
- React Hook Form for forms
- Axios for HTTP requests

**Key Components:**

1. **Authentication Flow**
   - Login/Register pages with form validation
   - JWT token storage in Zustand (persisted)
   - Automatic token refresh on 401
   - Protected routes via middleware

2. **Dashboard**
   - Agent list with CRUD operations
   - Experiment history table
   - Real-time status updates

3. **Agent Management**
   - Create/Edit agent forms
   - JSON configuration editor
   - Framework selection (CrewAI/Langchain/OpenAI)

### Backend Architecture

**Technology Stack:**
- FastAPI (async web framework)
- SQLAlchemy (ORM)
- Pydantic (validation)
- python-jose (JWT)
- passlib (password hashing)

**Key Modules:**

1. **Authentication (`/auth`)**
   - Registration with email validation
   - Login with bcrypt password verification
   - JWT access tokens (30 min expiry)
   - Refresh tokens (7 day expiry)
   - Token revocation on logout

2. **Agent Management (`/agents`)**
   - CRUD operations for agent configs
   - Framework validation (enum)
   - JSON config validation
   - User ownership verification

3. **Experiments (`/experiments`)**
   - Create and run experiments
   - Background task execution
   - Status tracking (pending → running → completed/failed)
   - Result storage

4. **Agent Engine**
   - Modular execution for different frameworks
   - CrewAI: Multi-agent crews
   - Langchain: LLM chains and agents
   - OpenAI: Direct API calls
   - Error handling and result formatting

### Database Schema

```sql
-- Users table
users
├── id (PK)
├── username (UNIQUE)
├── email (UNIQUE)
├── hashed_password
├── preferences (JSONB)
├── created_at
└── updated_at

-- Agent configurations
agent_configs
├── id (PK)
├── name
├── framework (ENUM: crewai, langchain, openai)
├── config (JSONB)
├── user_id (FK → users)
├── created_at
└── updated_at

-- Experiments
experiments
├── id (PK)
├── agent_id (FK → agent_configs)
├── status (ENUM: pending, running, completed, failed)
├── input_data (JSONB)
├── result (JSONB)
├── error (TEXT)
├── started_at
├── completed_at
└── created_at

-- Revoked tokens (JWT blacklist)
revoked_tokens
├── id (PK)
├── jti (UNIQUE)
└── revoked_at
```

### Security Architecture

**Authentication Flow:**
```
1. User Login
   ↓
2. Verify credentials (email + bcrypt password)
   ↓
3. Generate tokens
   ├── Access Token (JWT, 30 min, contains user_id + jti)
   └── Refresh Token (JWT, 7 days, contains user_id + jti + type=refresh)
   ↓
4. Return tokens + user data
   ↓
5. Client stores in Zustand (localStorage)
   ↓
6. All API calls include: Authorization: Bearer <access_token>
   ↓
7. Backend validates token:
   ├── Verify signature
   ├── Check expiry
   ├── Check if revoked (jti in revoked_tokens)
   └── Load user from database
   ↓
8. On 401: Auto-refresh using refresh token
   ↓
9. On logout: Revoke token (add jti to revoked_tokens)
```

**Security Measures:**
- Bcrypt password hashing (automatic salt)
- JWT with RS256 signature
- Token revocation (blacklist)
- CORS protection
- Input validation (Pydantic)
- SQL injection protection (ORM)
- XSS protection (React)

### Agent Execution Flow

```
1. User creates experiment via UI
   ↓
2. POST /experiments/
   ├── Validate agent ownership
   ├── Create experiment record (status=pending)
   └── Add background task
   ↓
3. Background worker picks up task
   ├── Update status → running
   ├── Load agent config
   ├── Select framework executor:
   │   ├── CrewAI → Create crew & tasks
   │   ├── Langchain → Initialize agent & tools
   │   └── OpenAI → Call chat.completions API
   ├── Execute with input_data
   ├── Capture result or error
   └── Update experiment:
       ├── status → completed/failed
       ├── result → JSON output
       └── completed_at → timestamp
   ↓
4. User polls GET /experiments/{id}/status
   ↓
5. When completed, fetch GET /experiments/{id}/results
```

### Deployment Architecture

**Development:**
```
localhost:3000 (Next.js dev)
    ↓
localhost:8000 (FastAPI)
    ↓
SQLite file (perplexiplay.db)
```

**Production (Recommended):**
```
Vercel (Frontend)
    ↓ HTTPS
Railway/Heroku (Backend API)
    ↓ SSL
PostgreSQL (Managed DB)
```

### Scalability Considerations

**Current Architecture:**
- Single-instance backend
- In-process background tasks
- Synchronous agent execution

**Future Scaling:**
1. **Horizontal Scaling**
   - Multiple backend instances behind load balancer
   - Celery/RQ for distributed task queue
   - Redis for session storage

2. **Database Scaling**
   - Connection pooling (PgBouncer)
   - Read replicas for queries
   - Database sharding by user_id

3. **Caching Layer**
   - Redis cache for agent configs
   - CDN for static assets
   - API response caching

4. **Async Improvements**
   - WebSocket for real-time updates
   - Server-Sent Events for experiment status
   - Pub/Sub for multi-instance coordination

### API Design

**RESTful Principles:**
- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE)
- JSON request/response
- HTTP status codes
- Pagination (future)

**Authentication:**
- Bearer token in Authorization header
- Refresh token in request body
- Token revocation endpoint

**Error Handling:**
- Consistent error format
- Detailed error messages
- HTTP status codes
- Validation errors

### Development Workflow

```
1. Local Development
   ├── Run backend: uvicorn backend.main:app --reload
   ├── Run frontend: npm run dev
   └── Use SQLite for database

2. Testing
   ├── Backend tests: pytest
   ├── Frontend build: npm run build
   └── Manual testing

3. Deployment
   ├── Build frontend: npm run build
   ├── Deploy to Vercel: vercel deploy --prod
   ├── Build backend: docker build
   └── Deploy to Railway/Heroku

4. CI/CD
   ├── GitHub Actions on push
   ├── Run tests
   └── Auto-deploy to production
```

## Technology Decisions

### Why Next.js?
- Server-side rendering for better SEO
- App Router for modern React patterns
- Built-in API routes (unused here, but available)
- Excellent developer experience
- Easy Vercel deployment

### Why FastAPI?
- Modern async Python framework
- Automatic OpenAPI documentation
- Type safety with Pydantic
- High performance
- Easy background tasks

### Why SQLAlchemy?
- Mature ORM with good docs
- Database agnostic
- Migration support with Alembic
- Relationship management
- Protection against SQL injection

### Why JWT?
- Stateless authentication
- No server-side session storage
- Works across multiple instances
- Standard format (RFC 7519)
- Easy to implement refresh tokens

### Why PostgreSQL?
- Robust and reliable
- JSON support for config fields
- Wide hosting options
- Good performance
- ACID compliance

## Future Enhancements

1. **Real-time Updates**
   - WebSocket connection for live experiment status
   - Push notifications for completions

2. **Agent Collaboration**
   - Multi-agent experiments
   - Agent-to-agent communication
   - Workflow orchestration

3. **Analytics Dashboard**
   - Experiment success rates
   - Agent performance metrics
   - Cost tracking per framework

4. **Team Features**
   - Organizations and teams
   - Shared agent configs
   - Role-based access control

5. **Advanced Agent Features**
   - Tool marketplace
   - Custom tool integration
   - Agent versioning
   - A/B testing between configs

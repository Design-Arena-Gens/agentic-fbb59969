# API Documentation

Base URL: `http://localhost:8000` (dev) or `https://your-api.com` (prod)

## Authentication

All authenticated endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response:** `201 Created`
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "preferences": {},
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

**Errors:**
- `400 Bad Request`: Email or username already exists
- `422 Unprocessable Entity`: Validation error

---

#### POST /auth/login
Login with email and password.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepass123"
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "preferences": {},
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

**Errors:**
- `401 Unauthorized`: Invalid credentials

---

#### POST /auth/refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGc..."
}
```

**Errors:**
- `401 Unauthorized`: Invalid or expired refresh token

---

#### POST /auth/logout
Logout and revoke tokens.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

---

#### GET /auth/me
Get current user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "preferences": {},
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

### Agents

#### GET /agents/
List all agents for the current user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Research Assistant",
    "framework": "crewai",
    "config": {
      "role": "Research Assistant",
      "goal": "Gather information",
      "backstory": "Expert researcher",
      "tools": ["search"],
      "verbose": true
    },
    "user_id": 1,
    "created_at": "2025-01-15T10:30:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  }
]
```

---

#### GET /agents/{agent_id}
Get a specific agent by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Research Assistant",
  "framework": "crewai",
  "config": {
    "role": "Research Assistant",
    "goal": "Gather information"
  },
  "user_id": 1,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

**Errors:**
- `404 Not Found`: Agent not found or not owned by user

---

#### POST /agents/
Create a new agent.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Research Assistant",
  "framework": "crewai",
  "config": {
    "role": "Research Assistant",
    "goal": "Gather and analyze information",
    "backstory": "Expert researcher with attention to detail",
    "tools": ["search", "scrape"],
    "verbose": true
  }
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Research Assistant",
  "framework": "crewai",
  "config": {...},
  "user_id": 1,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T10:30:00Z"
}
```

**Errors:**
- `422 Unprocessable Entity`: Validation error

---

#### PUT /agents/{agent_id}
Update an existing agent.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "name": "Updated Name",
  "config": {
    "role": "Updated Role"
  }
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "name": "Updated Name",
  "framework": "crewai",
  "config": {...},
  "user_id": 1,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-01-15T11:00:00Z"
}
```

**Errors:**
- `404 Not Found`: Agent not found or not owned by user

---

#### DELETE /agents/{agent_id}
Delete an agent.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `204 No Content`

**Errors:**
- `404 Not Found`: Agent not found or not owned by user

---

### Experiments

#### GET /experiments/
List all experiments for the current user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "agent_id": 1,
    "status": "completed",
    "input_data": {
      "task": "Research AI trends"
    },
    "result": {
      "framework": "crewai",
      "output": "AI trends include..."
    },
    "error": null,
    "started_at": "2025-01-15T10:35:00Z",
    "completed_at": "2025-01-15T10:37:00Z",
    "created_at": "2025-01-15T10:35:00Z"
  }
]
```

---

#### GET /experiments/{experiment_id}
Get a specific experiment by ID.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "agent_id": 1,
  "status": "completed",
  "input_data": {...},
  "result": {...},
  "error": null,
  "started_at": "2025-01-15T10:35:00Z",
  "completed_at": "2025-01-15T10:37:00Z",
  "created_at": "2025-01-15T10:35:00Z"
}
```

**Errors:**
- `404 Not Found`: Experiment not found

---

#### POST /experiments/
Create and run a new experiment.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "agent_id": 1,
  "input_data": {
    "task": "Research AI trends in 2025",
    "depth": "detailed"
  }
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "agent_id": 1,
  "status": "pending",
  "input_data": {...},
  "result": null,
  "error": null,
  "started_at": null,
  "completed_at": null,
  "created_at": "2025-01-15T10:35:00Z"
}
```

**Errors:**
- `404 Not Found`: Agent not found or not owned by user
- `422 Unprocessable Entity`: Validation error

---

#### GET /experiments/{experiment_id}/status
Get the current status of an experiment.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "status": "running"
}
```

**Status Values:**
- `pending`: Experiment created, waiting to run
- `running`: Currently executing
- `completed`: Successfully finished
- `failed`: Execution failed

**Errors:**
- `404 Not Found`: Experiment not found

---

#### GET /experiments/{experiment_id}/results
Get the results of a completed experiment.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "agent_id": 1,
  "status": "completed",
  "input_data": {...},
  "result": {
    "framework": "crewai",
    "output": "Detailed analysis of AI trends...",
    "config": {...}
  },
  "error": null,
  "started_at": "2025-01-15T10:35:00Z",
  "completed_at": "2025-01-15T10:37:00Z",
  "created_at": "2025-01-15T10:35:00Z"
}
```

**Errors:**
- `404 Not Found`: Experiment not found
- `400 Bad Request`: Experiment not completed yet

---

## Error Responses

All error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

### Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Request successful, no content to return
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required or failed
- `403 Forbidden`: Authenticated but not authorized
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

### Validation Errors

Pydantic validation errors return detailed field-level errors:

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

## Rate Limiting

Currently no rate limiting is enforced. In production, consider implementing rate limiting to prevent abuse.

## Framework-Specific Configurations

### CrewAI Agent Config
```json
{
  "role": "Research Assistant",
  "goal": "Gather and analyze information",
  "backstory": "Expert researcher with attention to detail",
  "tools": ["search", "scrape"],
  "verbose": true
}
```

### Langchain Agent Config
```json
{
  "llm": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 2000,
  "tools": ["calculator", "wikipedia"],
  "memory": "conversation_buffer",
  "verbose": false
}
```

### OpenAI Agent Config
```json
{
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 1500,
  "system_message": "You are a helpful research assistant"
}
```

## Interactive API Docs

FastAPI provides automatic interactive documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to test all endpoints directly in the browser.

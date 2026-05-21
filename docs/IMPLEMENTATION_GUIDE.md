# ZodiacSync Implementation Guide

Last updated: 22 May 2026

## 1. Project Summary

ZodiacSync is an AI-powered Vedic astrology assistant. The current implementation includes:

- FastAPI backend
- Browser frontend served by the backend
- User registration and login
- Bearer-token authentication
- SQLite persistence for users and chat history
- OpenAI-powered chat responses
- Optional ChromaDB knowledge retrieval
- Docker deployment scaffold
- Smoke test coverage for auth, protected chat, and frontend serving

The project is now a deployable MVP. It is suitable for local use and single-instance deployment. For production scale, the next major backend upgrade should be PostgreSQL plus migrations.

## 2. High-Level Architecture

```text
Browser Frontend
   |
   | HTTP / JSON
   v
FastAPI Backend
   |
   |-- Auth Routes
   |     |-- bcrypt password hashing
   |     |-- HMAC-signed bearer token
   |
   |-- Chat Routes
   |     |-- authenticated user
   |     |-- SQLite chat history
   |     |-- optional ChromaDB context
   |     |-- OpenAI response generation
   |
   |-- Health Routes
   |
   v
SQLite Database

Optional:
ChromaDB vector store for astrology knowledge retrieval
```

## 3. Important Files

```text
src/backend/main.py
```

Creates the FastAPI app, configures CORS, initializes the database on startup, includes route modules, and mounts the frontend at `/app`.

```text
src/backend/database.py
```

Handles SQLite connection management and creates database tables.

```text
src/backend/security.py
```

Handles password hashing, password verification, access-token creation, and token decoding.

```text
src/backend/dependencies.py
```

Contains the `get_current_user` dependency used to protect authenticated routes.

```text
src/backend/routes/
```

Contains FastAPI route modules:

- `auth.py`
- `chat.py`
- `health.py`

```text
src/backend/services/
```

Contains database-facing business logic:

- `auth_service.py`
- `chat_service.py`

```text
src/backend/schemas/
```

Contains Pydantic request and response models.

```text
src/ai_engine/ai_service.py
```

Builds messages and calls OpenAI chat completions.

```text
src/ai_engine/knowledge/store.py
```

Handles optional ChromaDB retrieval.

```text
frontend/
```

Contains the HTML, CSS, and JavaScript frontend served at `/app`.

## 4. Backend Startup Flow

The backend starts from:

```text
src/backend/main.py
```

The app is created by `create_app()`.

On startup, the FastAPI lifespan handler runs:

```python
init_db()
```

This creates the SQLite database tables if they do not already exist.

The app then registers:

- `/health`
- `/auth/register`
- `/auth/login`
- `/auth/me`
- `/chat`
- `/chat/sessions`
- `/chat/sessions/{session_id}/messages`
- `/app`

## 5. Environment Configuration

Environment loading is handled by:

```text
src/config.py
```

The app loads values from the project-root `.env` file.

Important variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET_KEY=replace_with_a_long_random_secret
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=sqlite:///zodiac_sync.db
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
```

### Notes

- `OPENAI_API_KEY` is required for real AI chat responses.
- `JWT_SECRET_KEY` is required for login/register token creation.
- `DATABASE_URL` currently supports only `sqlite:///...`.
- `.env` must never be committed.

## 6. Database Implementation

The app currently uses SQLite through Python's built-in `sqlite3` module.

Default database file:

```text
zodiac_sync.db
```

This file is ignored by Git.

### Tables

#### users

Stores registered users.

```text
id
email
full_name
hashed_password
created_at
```

#### chat_sessions

Stores one chat thread per user conversation.

```text
id
user_id
title
created_at
updated_at
```

#### chat_messages

Stores user and assistant messages as plain text.

```text
id
session_id
role
content
created_at
```

Valid roles:

```text
user
assistant
```

#### birth_profiles

Prepared for future astrology personalization.

```text
id
user_id
date_of_birth
time_of_birth
place_of_birth
latitude
longitude
timezone
created_at
```

This table exists, but there are no API routes for it yet.

## 7. Authentication Implementation

Auth routes live in:

```text
src/backend/routes/auth.py
```

Auth business logic lives in:

```text
src/backend/services/auth_service.py
```

Security helpers live in:

```text
src/backend/security.py
```

### Register Flow

Endpoint:

```http
POST /auth/register
```

Request:

```json
{
  "email": "you@example.com",
  "full_name": "Aryan Sharma",
  "password": "strongpassword"
}
```

Flow:

1. Validate email, full name, and password.
2. Hash password with bcrypt.
3. Insert user into `users`.
4. Create access token.
5. Return token and user object.

### Login Flow

Endpoint:

```http
POST /auth/login
```

Flow:

1. Find user by email.
2. Verify password using bcrypt.
3. Create access token.
4. Return token and user object.

### Current User Flow

Endpoint:

```http
GET /auth/me
Authorization: Bearer <token>
```

Flow:

1. Read bearer token from the `Authorization` header.
2. Verify token signature and expiry.
3. Load user from SQLite.
4. Return user object.

## 8. Token Implementation

Tokens are implemented in:

```text
src/backend/security.py
```

The project uses a JWT-style token:

```text
base64url(header).base64url(payload).base64url(signature)
```

The signature uses:

```text
HMAC-SHA256
```

The secret comes from:

```env
JWT_SECRET_KEY
```

The payload contains:

```text
sub  user id
iat  issued at timestamp
exp  expiry timestamp
```

This avoids adding a separate JWT dependency while still giving the backend signed bearer-token auth.

## 9. Chat Implementation

Chat routes live in:

```text
src/backend/routes/chat.py
```

Chat persistence lives in:

```text
src/backend/services/chat_service.py
```

The `/chat` route is protected. A user must be logged in and must pass:

```http
Authorization: Bearer <token>
```

### Chat Request

```http
POST /chat
```

```json
{
  "message": "Is this a good time to start a new project?",
  "session_id": 1
}
```

`session_id` is optional.

If `session_id` is missing, the backend creates a new chat session.

### Chat Flow

1. Authenticate the current user.
2. Create or validate the chat session.
3. Load recent chat history from SQLite.
4. Retrieve optional astrology knowledge from ChromaDB.
5. Send the user's message, recent history, and retrieved context to OpenAI.
6. Save the user message and assistant response to SQLite.
7. Return the assistant response and session ID.

### What Is Sent To OpenAI?

The backend sends:

- the current user message
- recent chat history for the current session
- optional retrieved astrology knowledge context
- the system prompt from `ai_service.py`

The full database is not sent to OpenAI. Only recent session history is passed as conversational context.

### Is Chat Saved?

Yes.

Chat is saved in SQLite as plain text:

```text
chat_sessions
chat_messages
```

### Is Chat Saved In Vector Format?

No.

User chat messages and assistant responses are not currently embedded or stored in ChromaDB.

Current storage model:

```text
User chat history -> SQLite text tables
Astrology knowledge base -> optional ChromaDB vector store
```

This is intentional for the MVP because vectorizing personal chat has privacy and cost implications.

## 10. AI Implementation

OpenAI chat response generation lives in:

```text
src/ai_engine/ai_service.py
```

The function:

```python
generate_response(query, context, history)
```

builds messages for OpenAI:

1. System prompt describing ZodiacSync's personality and safety rules.
2. Recent chat history.
3. Retrieved astrology knowledge context.
4. Current user question.

The model currently used:

```text
gpt-4o-mini
```

## 11. Knowledge Retrieval Implementation

Knowledge retrieval lives in:

```text
src/ai_engine/knowledge/store.py
```

Embeddings are created in:

```text
src/ai_engine/knowledge/embed.py
```

Document loading is defined in:

```text
src/ai_engine/knowledge/ingest.py
```

Current behavior:

- If ChromaDB is not installed, retrieval is skipped.
- If the Chroma collection is empty, retrieval is skipped.
- If retrieval works, the top matching documents are passed to OpenAI as context.

Important current limitation:

```text
ingest.py currently returns an empty list.
```

That means the vector knowledge base has no real astrology documents yet unless you add them.

## 12. Frontend Implementation

The frontend is stored in:

```text
frontend/
```

Files:

```text
frontend/index.html
frontend/styles.css
frontend/app.js
```

The backend serves it at:

```text
/app
```

Local URL:

```text
http://127.0.0.1:8000/app
```

### Frontend Features

- Login tab
- Register tab
- Token storage in `localStorage`
- Authenticated chat
- Session list
- New chat button
- Message history loading
- Logout

### Frontend API Calls

The frontend calls:

```text
POST /auth/register
POST /auth/login
GET /chat/sessions
GET /chat/sessions/{session_id}/messages
POST /chat
```

For protected routes, it sends:

```http
Authorization: Bearer <token>
```

## 13. Health Endpoint

Endpoint:

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "ai_configured": true,
  "auth_configured": true,
  "database_configured": true,
  "knowledge_store_available": true
}
```

Meaning:

- `ai_configured`: `OPENAI_API_KEY` is present.
- `auth_configured`: `JWT_SECRET_KEY` is present.
- `database_configured`: database path can be resolved.
- `knowledge_store_available`: ChromaDB package is installed.

## 14. Running Locally

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Create `.env`:

```bash
cp .env.example .env
```

Run:

```bash
./run.sh
```

Open frontend:

```text
http://127.0.0.1:8000/app
```

Open API docs:

```text
http://127.0.0.1:8000/docs
```

## 15. Deployment Implementation

Deployment files:

```text
Dockerfile
.dockerignore
```

Docker build:

```bash
docker build -t zodiac-sync .
```

Docker run:

```bash
docker run --env-file .env -p 8000:8000 zodiac-sync
```

Production command:

```bash
uvicorn src.backend.main:app --host 0.0.0.0 --port 8000
```

For Render, Railway, Fly.io, or similar platforms, configure environment variables in the platform dashboard.

Do not upload `.env` to production manually unless the platform specifically supports private env files.

## 16. Testing

Smoke test file:

```text
tests/test_backend_smoke.py
```

Run:

```bash
python3 -m pytest tests/test_backend_smoke.py
```

The smoke test verifies:

- health endpoint
- user registration
- token creation
- `/auth/me`
- protected chat rejects unauthenticated requests
- authenticated chat succeeds with mocked AI
- frontend is served

## 17. Security Notes

Implemented:

- bcrypt password hashing
- signed bearer tokens
- protected chat routes
- `.env` ignored by Git
- SQLite database ignored by Git
- CORS configurable by environment

Still needed before real production:

- rate limiting for `/chat`
- password reset flow
- email verification
- HTTPS-only deployment
- secure cookie auth or token refresh strategy
- structured audit logging
- abuse protection for expensive OpenAI calls
- stronger email validation
- secret rotation plan

## 18. Current Limitations

SQLite is used for persistence. This is fine for a single-instance MVP, but it is not ideal for multi-instance production.

There is no migration tool yet. Tables are created automatically by `init_db()`, but schema migrations should eventually be handled by Alembic or another migration system.

There is no frontend build system. The frontend is simple static HTML/CSS/JS.

There is no vector memory for user chat. User chats are stored only as plain text in SQLite.

There are no Panchang or Kundali calculation APIs yet.

There is no admin dashboard.

There is no billing or subscription system.

## 19. Recommended Next Steps

1. Move from SQLite to PostgreSQL.
2. Add Alembic migrations.
3. Add rate limiting to `/chat`.
4. Add birth profile CRUD APIs.
5. Add Panchang calculation service.
6. Add Kundali generation service.
7. Add real astrology knowledge documents to `ingest.py`.
8. Add CI to run tests on every commit.
9. Add monitoring and structured logs.
10. Deploy MVP backend and frontend together.

## 20. Deployment Readiness Summary

Ready for:

- local demo
- single-instance MVP deployment
- early user testing
- frontend-backed API use

Not yet ready for:

- high traffic
- multi-instance scaling
- sensitive production user data at scale
- paid production launch without rate limiting and monitoring


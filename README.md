# ZodiacSync

ZodiacSync is an AI-powered Vedic astrology assistant with a FastAPI backend, account login, persistent chat sessions, OpenAI-powered responses, optional ChromaDB knowledge retrieval, and a simple browser frontend.

> Sacred guidance, simplified by AI.

## Current Status

This is now a deployable MVP backend plus a lightweight frontend. It supports registration, login, JWT-style bearer tokens, persistent SQLite storage, protected chat, and saved chat sessions. Panchang calculations, Kundali generation, and deeper astrology engines are still roadmap items.

## Features

- FastAPI backend
- Static frontend served at `/app`
- Register, login, and `GET /auth/me`
- Password hashing with bcrypt
- HMAC-signed bearer tokens
- Persistent users, sessions, messages, and birth profile table
- Protected chat endpoint
- OpenAI chat completion for astrology-style guidance
- Optional ChromaDB vector knowledge retrieval
- Graceful fallback when ChromaDB is unavailable or empty
- Health endpoint with config status
- Dockerfile for deployment

## Tech Stack

- Python 3.10+
- FastAPI
- SQLite for the current persistent database
- bcrypt
- OpenAI Python SDK
- Pydantic
- Uvicorn
- ChromaDB for optional vector storage
- HTML/CSS/JavaScript frontend

## Project Structure

```text
ZodiacSync/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── src/
│   ├── backend/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── security.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   └── health.py
│   │   ├── schemas/
│   │   └── services/
│   ├── ai_engine/
│   │   ├── ai_service.py
│   │   └── knowledge/
│   └── config.py
├── Dockerfile
├── requirements.txt
├── run.sh
└── README.md
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET_KEY=replace_with_a_long_random_secret
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=sqlite:///zodiac_sync.db
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:5173
ENVIRONMENT=development
```

Never commit real API keys or production secrets.

## Run Locally

```bash
./run.sh
```

Or:

```bash
uvicorn src.backend.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/app
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Health

```http
GET /health
```

Response:

```json
{
  "status": "ok",
  "ai_configured": true,
  "auth_configured": true,
  "database_configured": true,
  "knowledge_store_available": true
}
```

### Register

```http
POST /auth/register
Content-Type: application/json
```

```json
{
  "email": "you@example.com",
  "full_name": "Aryan Sharma",
  "password": "strongpassword"
}
```

### Login

```http
POST /auth/login
Content-Type: application/json
```

```json
{
  "email": "you@example.com",
  "password": "strongpassword"
}
```

### Current User

```http
GET /auth/me
Authorization: Bearer <token>
```

### Chat

```http
POST /chat
Authorization: Bearer <token>
Content-Type: application/json
```

```json
{
  "message": "Is this a good time to start a new project?",
  "session_id": 1
}
```

`session_id` is optional. If omitted, the backend creates a new chat session.

### Chat Sessions

```http
GET /chat/sessions
Authorization: Bearer <token>
```

```http
GET /chat/sessions/{session_id}/messages
Authorization: Bearer <token>
```

## Knowledge Retrieval

The chat endpoint can use ChromaDB for retrieval-augmented responses. If ChromaDB is unavailable or the collection is empty, the app continues with an empty knowledge context.

To load knowledge:

```bash
python3 run_ingest.py
```

At the moment, `src/ai_engine/knowledge/ingest.py` returns an empty document list. Add curated astrology text chunks there before expecting retrieval results.

## Docker

Build:

```bash
docker build -t zodiac-sync .
```

Run:

```bash
docker run --env-file .env -p 8000:8000 zodiac-sync
```

## Deployment Notes

For a first deployment, Render, Railway, Fly.io, or a small VPS are good options. Set environment variables in the platform dashboard instead of uploading `.env`.

SQLite is acceptable for a single-instance MVP. Before scaling to multiple backend instances, move the database layer to PostgreSQL with migrations.

## Roadmap

- PostgreSQL adapter and Alembic migrations
- Rate limiting for `/chat`
- Password reset flow
- Email verification
- Birth profile API
- Panchang calculations
- Kundali generation
- Production observability and structured logs
- Automated tests in CI

## License

MIT License. See [LICENSE](LICENSE).

---

Last updated: 22 May 2026

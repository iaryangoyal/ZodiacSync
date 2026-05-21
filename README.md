# ZodiacSync

ZodiacSync is an AI-powered Vedic astrology assistant. The current app exposes a FastAPI backend with a conversational `/chat` endpoint, OpenAI-powered responses, optional ChromaDB knowledge retrieval, and a prompt designed to answer like a calm, practical AI Pandit.

> Sacred guidance, simplified by AI.

## Current Status

This repository is an early MVP backend. The chat API is usable today. Panchang, Kundali generation, ritual reminders, frontend UI, and deeper astrology engines are planned or partially documented, but not fully implemented in code yet.

## Features

- FastAPI backend with health and chat endpoints
- OpenAI chat completion for astrology-style guidance
- Project-root `.env` loading through `src/config.py`
- Optional ChromaDB vector knowledge retrieval
- Graceful fallback when ChromaDB is not installed
- In-memory chat history with a bounded message limit
- Local-development CORS support for `localhost` and `127.0.0.1`

## Tech Stack

- Python 3.10+
- FastAPI
- OpenAI Python SDK
- Pydantic
- Uvicorn
- ChromaDB for optional vector storage

## Project Structure

```text
ZodiacSync/
├── src/
│   ├── backend/
│   │   └── main.py              # FastAPI app and API routes
│   ├── ai_engine/
│   │   ├── ai_service.py        # OpenAI chat response generation
│   │   └── knowledge/
│   │       ├── embed.py         # OpenAI embeddings helper
│   │       ├── ingest.py        # Knowledge document loader
│   │       └── store.py         # ChromaDB storage/retrieval
│   └── config.py                # Environment loading helpers
├── docs/                        # Architecture and project notes
├── run_ingest.py                # Knowledge ingestion entrypoint
├── requirements.txt
├── .env.example
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

Then edit `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Never commit real API keys. Keep secrets in `.env` only.

## Run The Backend

Recommended:

```bash
uvicorn src.backend.main:app --reload
```

Direct script mode also works:

```bash
python3 src/backend/main.py
```

The API runs at:

```text
http://127.0.0.1:8000
```

## API Endpoints

### Health

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Chat

```http
POST /chat
Content-Type: application/json
```

Request:

```json
{
  "message": "Is this a good time to start a new project?",
  "user_id": "dev_user"
}
```

Response:

```json
{
  "response": "..."
}
```

`user_id` is optional. If omitted, the backend uses the client host for temporary in-memory chat history.

## Knowledge Retrieval

The chat endpoint can use ChromaDB for retrieval-augmented responses. If `chromadb` is not installed or unavailable, the app logs a warning and continues with an empty knowledge context.

To load knowledge into ChromaDB:

```bash
python3 run_ingest.py
```

At the moment, `src/ai_engine/knowledge/ingest.py` returns an empty document list. Add curated astrology text chunks there before expecting retrieval results.

## Example Curl

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"What details do you need for a birth chart?", "user_id":"local_test"}'
```

## Troubleshooting

`ModuleNotFoundError: No module named 'src'`

Use one of the supported run commands from the project root:

```bash
uvicorn src.backend.main:app --reload
python3 src/backend/main.py
```

`OPENAI_API_KEY is not configured.`

Make sure `.env` exists in the repository root and contains:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

`chromadb is not installed.`

Install requirements:

```bash
python3 -m pip install -r requirements.txt
```

The app can still answer chat requests without ChromaDB, but retrieval-based knowledge will be skipped.

## Roadmap

- Add real astrology knowledge ingestion data
- Build a frontend chat experience
- Add Panchang calculations
- Add birth chart and Kundali generation
- Add user profiles and persistent chat history
- Add structured tests for API and AI helper behavior

## License

MIT License. See [LICENSE](LICENSE).

---

Last updated: 22 May 2026

# ZodiacSync – Project Documentation

## 1. Project Overview
ZodiacSync is an AI-powered platform that brings Vedic astrology and ritual guidance into a modern, digital experience. It provides users with personalized astrological insights, daily Panchang, instant Kundali generation, and conversational spiritual advice, all powered by advanced AI and a curated knowledge base.

## 2. Features
- Daily Panchang and horoscope
- Instant AI-generated birth charts (Kundali)
- Conversational AI for astrology-related questions
- Ritual reminders and personalized guidance

## 3. Architecture
- **Frontend:** (Planned) React Native/Next.js for chat UI and dashboards
- **Backend:** FastAPI (Python) for API endpoints and orchestration
- **AI Engine:** LLM (GPT-4/5) with LangChain for reasoning and response generation
- **Knowledge Base:** Vector DB (ChromaDB) and Knowledge Graph for astrology data
- **Panchang Engine:** (Planned) Astronomical calculations using AstroPy/Swiss Ephemeris

## 4. Setup & Installation
- Python 3.10+
- Install dependencies: `pip install -r requirements.txt`
- Set up environment variables (e.g., `OPENAI_API_KEY`)
- Run backend: `python src/backend/main.py`
- Ingest knowledge: `python run_ingest.py`

## 5. API Endpoints
- `GET /` – Welcome message
- `GET /health` – Health check
- `POST /chat` – Conversational endpoint (send `{ "message": "your question" }`)

## 6. Project Structure
- `src/backend/` – FastAPI backend
- `src/ai_engine/` – AI logic and knowledge management
- `docs/` – Architecture and documentation
- `data/` – (Planned) Knowledge and astrology data
- `notebooks/` – (Planned) Experiments and research

## 7. Roadmap
- Expand knowledge ingestion (add Vedic texts, rituals)
- Build frontend chat UI
- Add Panchang and ephemeris calculations
- Enhance AI personality and accuracy
- Add premium features (compatibility, muhurat, etc.)

## 8. License
MIT License

---
*Last updated: 21 May 2026*

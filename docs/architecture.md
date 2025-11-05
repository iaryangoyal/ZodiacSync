# 🧭 ZodiacSync System Architecture

> Architecture & Data Flow for the **ZodiacSync AI Pandit App**  
> *(Version 1.0 – November 2025)*

---

## 🌟 Overview
ZodiacSync is an AI-driven astrology and ritual guidance platform designed to bring **Hindu Vedic astrology (Jyotish)** into a **modern digital experience**.

It combines:

- 🪔 Astronomical data (Panchang / Ephemeris)  
- 📚 Astrological knowledge (Vedic texts, Kundali rules)  
- 🤖 AI reasoning (LLM chat + knowledge graph retrieval)

---

## 🧩 High-Level System Components

```mermaid
flowchart TD
    A[Mobile / Web App] --> B[Backend API]
    B --> C[AI Engine (LLM + LangChain)]
    C --> D[Vector DB (Pinecone / Qdrant)]
    C --> E[Knowledge Graph (Neo4j)]
    C --> F[Panchang Engine (AstroPy / Swiss Ephemeris)]
    F --> G[Ephemeris / NASA APIs]
    C --> H[Response Generator]
    H --> A


## 🏗️ Layer-by-Layer Breakdown

---

### 1️⃣ Frontend (User Layer)

**Tech:** React Native / Next.js  
**Role:** Provides a conversational and visual interface.

**Key Features**
- Chat UI for AI Pandit interaction  
- Birth detail input (date, time, location)  
- Daily horoscope dashboard  
- Ritual & puja reminders  

---

### 2️⃣ Backend (API Layer)

**Tech:** FastAPI / Node.js (TypeScript)  
**Role:** Core communication bridge between the frontend, AI, and databases.

**Responsibilities**
- User authentication & profile management  
- API endpoints for chat, Panchang, and chart generation  
- Request orchestration between LLM and astrology engines  
- Response caching (Redis)  

---

### 3️⃣ AI Engine Layer

**Tech:** GPT-5 + LangChain / LlamaIndex  
**Role:** Acts as the *digital Pandit brain.*

**Submodules**
- **Prompt Orchestrator:** Structures user input + system context  
- **Retriever:** Pulls relevant knowledge (from Vector DB + Graph)  
- **Response Composer:** Generates final explanation or advice  

**Example Flow**

User Query → "Is today good for travel?"
↓
Retriever finds Panchang info + Vedic text chunks
↓
LLM interprets planetary conditions
↓
Response Composer outputs: "Today’s Nakshatra favors new journeys."


---

### 4️⃣ Vector Database (Knowledge Retrieval Layer)

**Tech:** Pinecone / Qdrant  
**Purpose:** Store and retrieve unstructured text embeddings from astrology books, Panchang data, and rituals.

**Data Sources**
- Curated Vedic scriptures (translated)  
- Panchang explanations  
- Astrology blog archives  
- Mantra and puja descriptions  

**Structure Example**
| ID | Text Snippet | Embedding | Tags |
|----|---------------|------------|------|
| 001 | "When Moon is in Pushya Nakshatra..." | [0.23, 0.14, ...] | Nakshatra, Ritual |
| 002 | "Saturn in 7th House brings delays in marriage." | [0.12, 0.87, ...] | Saturn, Marriage |

---

### 5️⃣ Knowledge Graph (Symbolic Reasoning Layer)

**Tech:** Neo4j / ArangoDB  
**Purpose:** Connect structured astrological entities.

**Schema Example**

Planet → influences → House
House → represents → LifeArea
Zodiac → ruledBy → Planet
Transit → affects → Planet


**Query Example**
> “How does Saturn transiting Aries affect someone with Moon in Libra?”

This logical layer complements the LLM’s natural language reasoning.

---

### 6️⃣ Panchang & Ephemeris Engine

**Tech:** AstroPy + Swiss Ephemeris  
**Purpose:** Generate astronomical positions and Hindu calendar data.

**Outputs**
- Daily Tithi, Nakshatra, Yoga, Karana  
- Sunrise/Sunset, Rahu Kaal, Gulika Kaal  
- Planetary longitudes and aspects  

**APIs / Data Sources**
- [Drik Panchang API](https://www.drikpanchang.com)  
- [NASA JPL Horizons API](https://ssd.jpl.nasa.gov/horizons/)  
- Local caching via PostgreSQL  

---

### 7️⃣ Storage Layer

| Component | Use | Tech |
|------------|-----|------|
| User Data | Profiles, Kundalis, chat history | PostgreSQL |
| Fast Cache | Chat context, ephemeral results | Redis |
| Logs & Metrics | User interactions, response times | MongoDB / Elastic |

---

### 8️⃣ LLM Workflow Summary

```mermaid
sequenceDiagram
    participant User
    participant Backend
    participant AI_Engine
    participant VectorDB
    participant KnowledgeGraph
    participant Panchang

    User->>Backend: Sends query ("When is a good time to start my business?")
    Backend->>AI_Engine: Formats query with context
    AI_Engine->>VectorDB: Retrieve relevant astrology texts
    AI_Engine->>KnowledgeGraph: Fetch symbolic relationships
    AI_Engine->>Panchang: Get current planetary data
    AI_Engine->>Backend: Generate contextual prediction
    Backend->>User: Returns final AI Pandit response

⚙️ Scalability Considerations

| Area                     | Plan                                                 |
| ------------------------ | ---------------------------------------------------- |
| **Load Scaling**         | Stateless APIs behind AWS Lambda / Kubernetes        |
| **Model Updates**        | Fine-tune or prompt-tune periodically                |
| **Data Growth**          | Shard vector DBs and cache hot data                  |
| **Internationalization** | Multilingual responses (English, Hindi, Tamil, etc.) |
| **Privacy**              | Encrypt user data (AES-256) & anonymize birth info   |

Frontend (React Native)
   ↓
Backend API (FastAPI / Node)
   ↓
AI Layer (GPT-5 + LangChain)
   ↓
Vector DB / Knowledge Graph / Panchang Engine
   ↓
Response → Frontend


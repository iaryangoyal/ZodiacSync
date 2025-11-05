# 🪔 ZodiacSync – Your Personal AI Pandit

> *Bringing ancient Vedic wisdom into the modern digital age.*  
> *AI-driven guidance for your daily life, based on Hindu astrology and Panchang.*

---

## 🌟 Vision

**ZodiacSync** replaces (or complements) the traditional Hindu *pandit* experience with an AI-powered guide.  
It blends **Jyotish Shastra (Vedic astrology)**, **astronomical precision**, and **LLM reasoning** to offer instant, private, and personalized insights — anytime, anywhere.

### 💬 Tagline
> “Sacred guidance, simplified by AI.”

---

## 🎯 Target Audience

**Young urban Indians (18–35)** who:
- Believe in astrology and spirituality  
- Prefer tech-friendly, private, on-demand experiences  
- Seek daily guidance without formal rituals or appointments  

---

## 💎 Differentiator

| Traditional Pandit | ZodiacSync |
|--------------------|-------------|
| Limited access | 24/7 AI availability |
| Judgmental / biased | 100% neutral and private |
| Manual charting | Instant AI-generated Kundali |
| Vedic-only | Blends tradition + modern data-driven insights |

---

## 🚀 MVP Features (Phase 1)

| Feature | Description |
|----------|--------------|
| 🗓️ **Daily Panchang / Horoscope** | Displays sunrise, Tithi, Nakshatra, Yoga, Karana, Rahu Kaal, etc. |
| 🧭 **Personal Birth Chart (Janma Kundali)** | Generates Kundali from date, time, and place of birth. |
| 💬 **Conversational AI (Chatbot)** | Ask: “When should I do puja?” / “Is today good for new beginnings?” |
| 🔔 **Ritual Reminders** | Notifications for Ekadashi, Sankranti, Purnima, etc. |
| 🧘‍♂️ **AI Guidance** | Personalized responses powered by GPT-5 and a Vedic knowledge base. |

---

## 🌈 Future Features (Phase 2+)

- 🔮 **Predictive Insights**: Personal yearly/monthly forecasts  
- 💑 **Kundali Milan**: Relationship compatibility analysis  
- 🕉️ **AI Puja Assistant**: Voice-guided rituals and mantras  
- 🪔 **Muhurat Finder**: Auspicious timing suggestions for events  
- 📿 **Mantra Recommendations**: Based on current planetary positions  
- 💰 **Premium Tier**: Access to deeper insights or live astrologer chat  

---

## 🧩 Tech Architecture Overview

```mermaid
flowchart TD
    A[User Chat / Query] --> B[Frontend (React Native)]
    B --> C[Backend API (FastAPI / Node)]
    C --> D[LLM Layer (GPT-5)]
    D --> E[Vector DB (Astrology Knowledge Base)]
    D --> F[Knowledge Graph (Planet ↔ House ↔ Effect)]
    C --> G[Panchang Engine (Ephemeris / AstroPy)]
    D --> H[Response Generator]
    H --> A

# 🛡️ TubeShield AI: YouTube Comment Moderation & Community Intelligence Platform

**TubeShield AI** is an enterprise-grade, multi-agent AI application designed for YouTube comment moderation, sentiment breakdown, community toxicity detection, automated actioning, and AI reply generation.

Powered by **LangGraph**, **LangChain**, **FastAPI**, and **React**, it demonstrates modern AI Engineering principles: StateGraph workflow orchestration, single-responsibility AI agents, structured prompt engineering, and production-ready clean architecture.

---

## 🌟 Key Features

- 🤖 **LangGraph Multi-Agent Engine**: 7 specialized agents processing YouTube comments with state isolation and single responsibility.
- 🎯 **Automated Moderation Matrix**: Categorizes every comment into `Keep`, `Hide`, `Delete`, or `Needs Human Review` with confidence scores and rationale.
- 📊 **Community Health Score (0-100)**: Quantitative indicator measuring channel health based on toxicity, spam ratio, and viewer sentiment.
- 💬 **AI Reply Suggestions**: Context-aware, polite, and professional response generation for questions, feature requests, and complaints.
- ⚡ **Zero-Dependency Mock Mode**: Runs out of the box with realistic fallback data even if OpenAI or YouTube API keys are not configured.
- 🎨 **Executive Analytics Dashboard**: Built with React, Tailwind CSS glassmorphic aesthetics, and Chart.js visual analytics.

---

## 🧩 LangGraph Multi-Agent Architecture & Design Decisions

### Why LangGraph?
Standard linear LLM chains struggle when handling multi-faceted tasks (spam detection, toxicity classification, sentiment intent extraction, moderation policy enforcement, reply generation, and aggregate analytics).

LangGraph solves this by modeling the workflow as a **StateGraph**:
1. **State Isolation**: A shared `ModerationState` TypedDict holds video details, raw comments, processed results, and global analytics.
2. **Single-Responsibility Nodes**: Each node is bound to a single AI agent. If an agent fails or produces low confidence, downstream agents can operate on deterministic fallbacks.
3. **Decoupled Execution**: Graph nodes can be executed sequentially or in parallel for batch operations.

```
                                    ┌───────────────────────┐
                                    │    Input YouTube URL   │
                                    └───────────┬───────────┘
                                                │
                                                ▼
                                    ┌───────────────────────┐
                                    │  Agent 1: Fetch Agent │
                                    └───────────┬───────────┘
                                                │
                                                ▼
                                    ┌───────────────────────┐
                                    │ LangGraph Pipeline    │
                                    └───────────┬───────────┘
                                                │
        ┌───────────────────┬───────────────────┼───────────────────┬───────────────────┐
        │                   │                   │                   │                   │
        ▼                   ▼                   ▼                   ▼                   ▼
Agent 2: Spam      Agent 3: Toxicity   Agent 4: Sentiment  Agent 5: Moderation Agent 6: Reply
Detection Agent    Detection Agent     & Intent Agent      Decision Agent      Generator Agent
        │                   │                   │                   │                   │
        └───────────────────┴───────────────────┼───────────────────┴───────────────────┘
                                                │
                                                ▼
                                    ┌───────────────────────┐
                                    │  Agent 7: Analytics   │
                                    │  & Health Score (0-100│
                                    └───────────┬───────────┘
                                                │
                                                ▼
                                    ┌───────────────────────┐
                                    │  FastAPI & Database   │
                                    └───────────────────────┘
```

---

## 🤖 Detailed AI Agent Breakdown

| Agent | Responsibility | Output Structure | Why it Exists |
|---|---|---|---|
| **Agent 1: Fetch Agent** | Validates YouTube URL, extracts Video ID, calls YouTube API v3 or fallback mock engine. | `VideoMetadata`, `List[RawComment]` | Isolates API fetching and rate-limit handling from AI processing logic. |
| **Agent 2: Spam Detection Agent** | Identifies promotional spam, crypto scams, Telegram links, bot messages, and fake giveaways. | `{ spam: bool, confidence: float, reason: str }` | Focuses strictly on financial fraud and link-spam detection to protect viewers. |
| **Agent 3: Toxicity Detection Agent** | Evaluates harassment, hate speech, threats, and offensive language severity. | `{ category: str, severity: str, confidence: float, reason: str }` | Protects channel safety and policy compliance without mixing sentiment logic. |
| **Agent 4: Sentiment & Intent Agent** | Classifies sentiment (Positive, Neutral, Negative) and intent (Question, Feature Request, Complaint, Praise). | `{ sentiment: str, intent: str, confidence: float, reason: str }` | Identifies what viewers actually want (e.g., source code links, follow-up topics). |
| **Agent 5: Moderation Decision Agent** | Synthesizes outputs from Agents 2, 3, and 4 into a final policy action (`Keep`, `Hide`, `Delete`, `Needs Human Review`). | `{ decision: str, reason: str }` | Acts as the central rule-synthesizer separating risk classification from action taking. |
| **Agent 6: Reply Generator Agent** | Generates short, polite, professional replies for questions, complaints, and feature requests. | `{ suggested_reply: str, tone: str }` | Saves creator time by auto-drafting helpful replies for actionable comments. |
| **Agent 7: Analytics Agent** | Computes aggregate statistics, top keywords, complaints list, and **Community Health Score (0-100)**. | `AnalyticsSummary` | Provides macro community insights and strategic channel recommendations. |

---

## 🧠 Prompt Engineering Decisions

1. **Structured Pydantic Outputs**:
   - Every agent uses LangChain's `PydanticOutputParser` to guarantee strict JSON output.
   - Avoids unstructured free-text responses and ensures seamless database insertion.

2. **Context-Constrained Prompting**:
   - Prompts pass strict guidelines (e.g., Reply Generator limits responses to 1–2 polite sentences).
   - Low temperature (`0.2`) guarantees deterministic and repeatable agent outputs across runs.

3. **Fallback Heuristic Engine**:
   - Every agent includes fallback rule checks. If no API key is provided, the platform operates seamlessly without crashing.

---

## 📁 Project Directory Structure

```
TubeShieldAI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── analyze.py
│   │   │   │   ├── analytics.py
│   │   │   │   ├── comments.py
│   │   │   │   └── health.py
│   │   │   └── router.py
│   │   ├── agents/
│   │   │   ├── fetch_agent.py
│   │   │   ├── spam_agent.py
│   │   │   ├── toxicity_agent.py
│   │   │   ├── sentiment_agent.py
│   │   │   ├── moderation_agent.py
│   │   │   ├── reply_agent.py
│   │   │   └── analytics_agent.py
│   │   ├── graph/
│   │   │   ├── state.py
│   │   │   └── moderation_graph.py
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   └── models.py
│   │   ├── models/
│   │   │   └── schemas.py
│   │   ├── prompts/
│   │   ├── services/
│   │   │   ├── llm_factory.py
│   │   │   └── youtube_service.py
│   │   ├── utils/
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx
│   │   │   ├── UrlInputForm.jsx
│   │   │   ├── VideoCard.jsx
│   │   │   ├── AnalyticsCards.jsx
│   │   │   ├── HealthScoreMeter.jsx
│   │   │   ├── ChartsSection.jsx
│   │   │   ├── KeywordCloud.jsx
│   │   │   ├── CommentTable.jsx
│   │   │   └── ReplyModal.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── README.md
```

---

## ⚡ Quick Start Guide

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file (Optional):
```env
OPENAI_API_KEY=your_openai_key_here
YOUTUBE_API_KEY=your_youtube_key_here
DEFAULT_LLM_PROVIDER=openai
DEFAULT_MODEL_NAME=gpt-4o-mini
```

Run Backend Server:
```bash
uvicorn app.main:app --reload --port 8000
```
- Swagger API Docs: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
- Web Application: `http://localhost:3000`

---

## 🔌 API Endpoint Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/analyze` | Triggers LangGraph moderation pipeline for a YouTube URL |
| `GET` | `/api/results/{video_id}` | Retrieves processed comments and AI decisions for a video |
| `GET` | `/api/analytics/{video_id}` | Retrieves analytics metrics and Community Health Score |
| `POST` | `/api/generate-reply` | Generates on-demand custom AI response for a comment |
| `GET` | `/api/videos` | Lists all analyzed video history |
| `GET` | `/api/health` | Backend status, active provider, and mock mode status |

---

## 🛡️ License & Engineering Credits
Built for AI Engineering demonstration using Python, FastAPI, LangGraph, and React.

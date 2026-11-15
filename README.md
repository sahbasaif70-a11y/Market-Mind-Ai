# 📊 MarketMind AI — Full-Stack Agentic Business Intelligence Platform

**MarketMind AI** is a full-stack, autonomous Agentic AI system and Multi-Format RAG Platform. It is engineered with **Python**, **OpenAI (GPT-4o)**, **FastAPI**, and **React + Vite + Tailwind CSS**. 

The platform autonomously researches complex business queries, breaks tasks into structured sub-questions, executes bounded search & calculation tool loops, audits evidence for quality/contradictions, generates markdown reports with human approval gates, and offers document QA over PDF, JSON, Excel, and CSV files.

---

## 🏗️ Architecture & Project Structure

```text
MarketMind_Ai/
├── MarketMind_Ai/                # Core Agentic AI System
│   ├── main.py                  # CLI Agent Execution Loop
│   ├── run_tests.py             # Automated Unit & Integration Tests
│   ├── requirements.txt         # Core AI Requirements
│   ├── .env.example             # Environment Configuration Template
│   ├── data/corpus/             # Approved Market Corpus & Vendor Specs
│   ├── src/
│   │   ├── config.py            # Guardrails, Path, & Limit Settings
│   │   ├── llm/                 # OpenAI Client Wrapper & Token/Cost Counter
│   │   ├── schemas/             # Pydantic Schemas (Plan, Evidence, Report, Tools)
│   │   ├── agents/              # AI Agents (Planner, Researcher, Comparison, QC, Report)
│   │   ├── crew/                # CrewAI Multi-Agent Workflow Engine
│   │   ├── tools/               # Secure Tool Dispatcher & Implementations
│   │   ├── state/               # Research State & JSON Persistence
│   │   └── approval/            # Human Approval Gate Interface
│   ├── docs/                    # Architecture & API Documentation
│   └── evaluation/              # Ground-Truth Benchmark & Evaluation Suite
│
├── backend/                     # FastAPI Backend API Server
│   ├── main.py                  # API Routes (MarketMind + RAG Endpoints)
│   └── requirements.txt         # Backend Server Dependencies
│
└── frontend/                    # Modern React Web Application
    ├── src/                     # React Components, State, & UI Logic
    ├── package.json             # NPM Manifest & Scripts
    ├── vite.config.js           # Vite Development Server Config
    └── tailwind.config.js       # Tailwind CSS Styling Configuration
```

---

## 🔥 Key Features

### 1. 🤖 Autonomous Agentic Research Engine (`MarketMind_Ai`)
- **Decomposition & Planning:** Breaks high-level business prompts into structured sub-questions.
- **Bounded Tool Loop:** Executes up to 25 controlled tool calls per research cycle.
- **Calculations:** Computes financial metrics (CAGR, sum, averages, growth rate percentages).
- **Quality Control & Audit:** Detects claim contradictions, assesses provenance, and rates confidence.
- **Human Approval Gate:** Reports require human approval (`approve`, `reject`, `revision`, `export`) before finalization.

### 2. ⚡ Multi-Format RAG Platform (`backend`)
- **Supported Formats:** Upload and chat with **PDF**, **JSON**, **Excel (.xlsx, .xls)**, and **CSV** files.
- **Vector Search:** Powered by LangChain, OpenAI Embeddings (`text-embedding-3-small`), and FAISS vector storage.
- **Strict Citation QA:** Answers queries with exact row, page, or key citation metadata.

### 3. 🎨 Modern Web Interface (`frontend`)
- Built with **React**, **Vite**, **Tailwind CSS**, and **Framer Motion**.
- Interactive dashboard for submitting research prompts, tracking agent reasoning, reviewing quality audits, and viewing full markdown reports.
- Document upload and interactive chat interface for multi-format RAG.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ & npm
- OpenAI API Key (`sk-...`)

---

### Step 1: Backend & AI Core Setup

1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies for Backend and Core AI:
   ```bash
   pip install -r backend/requirements.txt
   pip install -r MarketMind_Ai/requirements.txt
   ```

3. Configure Environment Variables:
   Create a `.env` file in the project root (or inside `MarketMind_Ai/`):
   ```env
   OPENAI_API_KEY=sk-proj-your-actual-api-key
   OPENAI_MODEL=gpt-4o-mini
   MAX_ITERATIONS=10
   MAX_TOOL_CALLS=25
   MAX_COST_USD=1.00
   ```

4. Start the FastAPI Backend Server:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```
   *The API server will run at `http://localhost:8000` with Swagger docs at `http://localhost:8000/docs`.*

---

### Step 2: Frontend UI Setup

1. Open a new terminal tab and navigate to `frontend`:
   ```bash
   cd frontend
   npm install
   ```

2. Start the Frontend Development Server:
   ```bash
   npm run dev
   ```
   *Open `http://localhost:5173` in your browser.*

---

### Step 3: Run AI Research via CLI (Optional)

You can also run the autonomous agent directly from the command line:

```bash
cd MarketMind_Ai
python main.py "Research the AI customer support market, compare Zendesk and Intercom pricing, and calculate market CAGR."
```

---

## 🌐 API Reference

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/api/health` | `GET` | Health check and backend status |
| `/api/marketmind/research` | `POST` | Trigger autonomous research workflow |
| `/api/marketmind/crew_research` | `POST` | Trigger multi-agent CrewAI research workflow |
| `/api/marketmind/reports` | `GET` | List all saved research reports |
| `/api/marketmind/reports/{id}` | `GET` | Fetch report details and state |
| `/api/marketmind/approve` | `POST` | Register human approval decision |
| `/api/marketmind/corpus` | `GET` | List active research corpus documents |
| `/api/marketmind/corpus/upload` | `POST` | Upload new `.txt` document to corpus |
| `/api/index` | `POST` | Index PDF/JSON/Excel/CSV document for RAG QA |
| `/api/chat` | `POST` | Query indexed document with citation-grounded RAG |

---

## 🔐 Safety & Guardrails Enforcement

- **Strict Evidence Grounding:** All claims map directly to indexed corpus source document IDs.
- **Arbitrary Code Shielding:** All tool invocations pass through `ToolDispatcher` with strict type validation.
- **Cost & Iteration Limits:** Enforces `MAX_COST_USD` ceiling and maximum tool call iterations to protect against API budget overruns.
- **Human Approval Gate:** Reports are flagged for human review before final publishing or export.

---

## 📄 License
MIT License — feel free to use and adapt for your research and business needs.

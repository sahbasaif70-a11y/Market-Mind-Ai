# 📊 MarketMind AI — Autonomous Business Research & Multi-Agent System

**MarketMind AI** is a state-of-the-art, autonomous Agentic AI system engineered in Python using OpenAI's GPT-4o architecture and **CrewAI multi-agent orchestration**. It automates end-to-end business intelligence, market research, competitor comparison, customer sentiment analysis, financial metric calculation, and quality control auditing.

The system supports both single-agent Plan-Act-Observe research loops and a **4-Agent CrewAI Multi-Agent Workflow** (Market Researcher, Competitor Analyst, Consumer Insights Strategist, and Head of Marketing/GTM Strategist).

---

## 🏗️ Architecture & Core Component Breakdown

```text
MarketMind_Ai/
├── main.py                  # CLI Single-Agent Execution Loop & Entry Point
├── crew_runner.py           # CrewAI Multi-Agent Runner & Kickoff Script
├── run_tests.py             # Automated Unit & Integration Test Suite
├── requirements.txt         # Core Dependencies Manifest
├── .env.example             # Configuration Template
├── data/
│   └── corpus/              # Approved Market Corpus & Vendor Data Files
├── src/
│   ├── config.py            # Path, Budget, & Guardrail Configurations
│   ├── llm/
│   │   ├── client.py        # OpenAI API Wrapper with Rate Limiting
│   │   └── usage.py         # Cost & Token Tracking Engine
│   ├── crew/
│   │   └── crew_manager.py  # CrewAI Multi-Agent Orchestrator & Native Tools
│   ├── agents/
│   │   ├── planner.py       # Task Decomposition & Planning Agent
│   │   ├── researcher.py    # Bounded Plan-Act-Observe Research Loop
│   │   ├── comparison.py    # Vendor Matrix Comparison Agent
│   │   ├── quality_control.py # Contradiction & Provenance Audit Agent
│   │   └── report_generator.py # Report Synthesis & Markdown Generator
│   ├── schemas/
│   │   ├── plan.py          # Research Plan & SubQuestion Schemas
│   │   ├── evidence.py      # Evidence Store & ResearchState Schemas
│   │   ├── report.py        # Final Market Report & Audit Schemas
│   │   └── tools.py         # OpenAI Tool Specs & Function Calls
│   ├── tools/
│   │   ├── dispatcher.py    # Secure Tool Dispatcher & Type Guardrails
│   │   ├── source_validator.py # Document Provenance & ID Validation
│   │   └── impl/
│   │       ├── calc_tools.py   # CAGR, Growth Rate, Sum, & Average Tools
│   │       └── search_tools.py # Corpus Search & Document Retrieval Tools
│   ├── state/
│   │   └── persistence.py   # State Persistence & JSON Storage Manager
│   └── approval/
│       └── cli_gate.py      # Human-in-the-Loop Approval Gate Interface
├── docs/                    # Architecture, API & Abuse Analysis Specs
└── evaluation/              # Benchmark Suite & Ground-Truth Test Cases
```

---

## 👥 CrewAI Multi-Agent Architecture (`src/crew/crew_manager.py`)

MarketMind AI features a dedicated **CrewAI Multi-Agent Engine** with 4 specialized agents working in a sequential pipeline:

| Agent Role | Goal & Responsibilities | Key Tools |
| :--- | :--- | :--- |
| **1. Lead Market Researcher** | Analyzes product niche, industry size (TAM/SAM/SOM), and target audience segments. | `Web Search Tool`, `Search Market Intelligence` |
| **2. Competitor Intelligence Analyst** | Benchmark top 3-5 competitors, pricing plans, USPs, and market gaps. | `Web Scraper Tool`, `Search Market Intelligence` |
| **3. Consumer Insights Strategist** | Analyzes customer reviews, public sentiment, complaints, and unmet market needs. | `Web Search Tool`, `Search Market Intelligence` |
| **4. Head of Marketing & GTM Strategist** | Synthesizes findings into Go-To-Market strategy, pricing recommendations, and ad copy. | `Calculate CAGR & Growth Rates` |

### Dual Execution Modes:
1. **CrewAI Native Mode (`run_crewai_native`):** Uses native CrewAI process kickoff for multi-agent sequential execution.
2. **MarketMind Hybrid Mode (`run_marketmind_hybrid`):** Orchestrates MarketMind AI state engines under CrewAI agent rules if CrewAI library is not installed.

---

## 🌟 Core Features & Single-Agent Pipeline

### 1. 🧠 Autonomous Research Planning (`planner.py`)
- Analyzes unstructured user queries and formulates a structured execution plan.
- Generates targeted sub-questions with specific search objectives.

### 2. 🔄 Bounded Research Execution Loop (`researcher.py`)
- Implements a controlled **Plan-Act-Observe** iterative tool call loop.
- Enforces strict iteration limits (default max 10 steps, 25 tool calls) to prevent infinite loops.

### 3. 🛠️ Secure Tool Suite & Deterministic Math (`tools/`)
- **`search_information`**: Keyword & semantic query over approved market corpus.
- **`retrieve_document`**: Full document retrieval by validated ID.
- **`calculate_metric`**: Deterministic CAGR, Total Growth %, Sum, and Averages.
- **`save_research`**: Structured recording of verified facts mapped to evidence IDs.
- **`compare_companies`**: Automated tabular feature/pricing extraction across vendors.

### 4. ⚖️ Quality Control & Audit Engine (`quality_control.py`)
- Audits facts for contradictions, low confidence levels, and unverified sources.

### 5. 👥 Human-in-the-Loop Approval Gate (`cli_gate.py`)
- Reports require human review before publishing (`approve`, `reject`, `revision`, `export`).

---

## 🚀 Quick Start Guide

### Step 1: Environment Setup
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Environment Configuration
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=sk-proj-your-actual-api-key
OPENAI_MODEL=gpt-4o-mini
MAX_ITERATIONS=10
MAX_TOOL_CALLS=25
MAX_COST_USD=1.00
```

### Step 3: Run Verification Tests
```bash
python run_tests.py
```

### Step 4: Run Market Research Agent

#### Option A: Single-Agent Loop Execution (`main.py`)
```bash
python main.py "Research the AI customer support market, compare Zendesk and Intercom pricing, and calculate market CAGR."
```

#### Option B: CrewAI Multi-Agent Execution (`crew_runner.py`)
```bash
python crew_runner.py "Research the AI customer support software market, compare pricing and features for Zendesk and Intercom, and recommend startup opportunities."
```

---

## 🔐 Safety & Guardrails Enforcement
- **Arbitrary Code Shielding:** Tool calls pass through strict type validation in `ToolDispatcher`.
- **API Budget Protection:** Enforces `MAX_COST_USD` limits and token counter tracking.
- **Strict Evidence Grounding:** Every claim is explicitly linked to source corpus document IDs.

---

## 📄 License
MIT License

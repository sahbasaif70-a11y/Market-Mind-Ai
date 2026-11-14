# MarketMind AI — Autonomous Business Research Agent

MarketMind AI is an advanced Agentic AI system built with Python and OpenAI API (GPT-4o / GPT-4o-mini). It autonomously researches business queries, divides tasks into structured sub-questions, retrieves and validates evidence from approved text corpora, performs metric calculations, detects quality issues/contradictions, and generates human-approved market research reports.

---

## 🏗️ Architecture & Component Breakdown

```
MarketMind_Ai/
├── main.py                  # CLI Main Execution Loop
├── test_phase1.py           # Environment Smoke Test
├── run_tests.py             # Automated Unit Test Runner
├── requirements.txt         # Dependency Manifest
├── .env.example             # Configuration Template
├── data/
│   └── corpus/              # Local Document Corpus (Corpus Data Store)
│       ├── vendor_zendesk.txt
│       ├── vendor_intercom.txt
│       └── ai_support_market_2025.txt
├── src/
│   ├── config.py            # Path & Limit Guardrails
│   ├── llm/
│   │   ├── client.py        # OpenAI API Wrapper
│   │   └── usage.py         # Cost & Token Counter
│   ├── schemas/
│   │   ├── plan.py          # Plan & SubQuestion Pydantic Schemas
│   │   ├── evidence.py      # Evidence & ResearchState Schemas
│   │   ├── report.py        # MarketReport Schemas
│   │   └── tools.py         # OpenAI Tool Specifications
│   ├── agents/
│   │   ├── planner.py       # Research Planner Agent
│   │   ├── researcher.py    # Bounded Plan-Act-Observe Research Loop
│   │   ├── comparison.py    # Matrix Comparison Agent
│   │   ├── quality_control.py # Contradiction & Provenance Audit Agent
│   │   └── report_generator.py # Report Synthesis & Markdown Renderer
│   ├── tools/
│   │   ├── dispatcher.py    # Secure Tool Dispatcher & Guardrails
│   │   └── impl/            # Search & Calculation Tool Implementations
│   ├── state/
│   │   └── persistence.py   # State Persistence & Log Saver
│   └── approval/
│       └── cli_gate.py      # Human Approval Gate Interface
└── runs/                    # Execution Logs & Generated Reports
```

---

## 🚀 Quick Start Guide

### 1. Environment Setup
Create a virtual environment and install requirements:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure OpenAI API Key
Open `.env` (or copy `.env.example` to `.env`) and add your API Key:
```env
OPENAI_API_KEY=sk-proj-your-actual-api-key
OPENAI_MODEL=gpt-4o-mini
MAX_ITERATIONS=10
MAX_TOOL_CALLS=25
MAX_COST_USD=1.00
```

### 3. Run Verification Test
```bash
python test_phase1.py
```

### 4. Run Unit Test Suite
```bash
python run_tests.py
```

### 5. Execute Market Research Agent
Run standard research query:
```bash
python main.py
```

Or pass a custom prompt:
```bash
python main.py "Research the AI customer support market, compare Zendesk and Intercom pricing, and calculate market CAGR."
```

---

## 🛠️ The 6 Required Tools

1. `search_information(query)`: Searches approved text corpus files.
2. `retrieve_document(document_id)`: Fetches full text content of a document.
3. `calculate_metric(metric_type, values)`: Computes Average, Sum, CAGR, or Growth Rate percentage.
4. `save_research(sub_question_id, source_id, claim_text, claim_type)`: Records verified factual claims.
5. `compare_companies(company_names)`: Filters and formats evidence into comparison matrices.
6. `generate_report()`: Synthesizes evidence store into report output.

---

## 🔐 Safety & Guardrails Enforcement
- **No Direct Arbitrary Code Execution:** All tool invocations pass through `ToolDispatcher`.
- **Token & Cost Ceiling:** Bounded by `MAX_COST_USD` limit.
- **Human Approval Gate:** Reports are never published automatically without human review.
- **Strict Evidence Grounding:** All claims map directly to a source document ID.

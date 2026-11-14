# Technical Documentation & System Guide — MarketMind AI

## 1. System Overview & Architecture
MarketMind AI is an autonomous, evidence-grounded market research agent designed for high-integrity business intelligence. The system operates on a Plan-Act-Observe architecture:

1. **Request Analysis & Query Normalization**: Parses user prompts to extract clean topics, validated competitor entities, and comparison criteria.
2. **Sub-Question Planning**: Generates an $M \times N$ matrix of targeted sub-questions.
3. **Bounded Agent Loop**: Executes tools within 5 strict termination conditions (Iterations, Tool Calls, Budget Ceiling, All Questions Resolved, Stuck-Loop Detection).
4. **Source Relevance Validation**: Applies domain credibility and cross-entity rejection rules.
5. **OpenAI LLM Synthesis & Quality Audit**: Dynamically synthesizes executive sections and executes a 10-check quality audit.
6. **Human Approval Gate**: Requires explicit human review before publishing.

## 2. Directory Structure
```
MarketMind_Ai/
├── config.py
├── main.py
├── data/corpus/ (20 text files with planted gap & contradiction)
├── docs/ (Architecture diagram, schemas, technical docs)
├── evaluation/ (Evaluation harness & test cases)
├── runs/ (Saved JSON states & rendered Markdown reports)
├── schemas/ (Standalone JSON schema files)
├── src/
│   ├── agents/ (Planner, Researcher, Comparison, QualityControl, ReportGenerator)
│   ├── approval/ (CLI Human Approval Gate)
│   ├── llm/ (OpenAI SDK client & Usage Tracker)
│   ├── schemas/ (Pydantic schemas)
│   ├── state/ (Persistence & State Management)
│   └── tools/ (Dispatcher, SourceValidator, Search & Calc Impls)
└── tests/ (18 automated regression test cases)
```

## 3. Running the Project
```bash
# 1. Activate Python environment
python backend/main.py

# 2. Run Automated Regression Tests
python -m unittest MarketMind_Ai/tests/test_accuracy_pipeline.py
```

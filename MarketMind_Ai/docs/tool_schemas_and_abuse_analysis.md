# Tool Schemas & Security Abuse Analysis

## 1. Tool Schemas

MarketMind AI registers 6 core tools in `ToolDispatcher`:

1. `search_information(query: str, target_entity: str, criterion: str)`
   - Searches local corpus and targeted live web search.

2. `fetch_webpage(url: str)`
   - Fetches webpage text and parses content snippet.

3. `calculate_metric(start_val: float, end_val: float, start_year: int, end_year: int)`
   - Deterministic math engine for CAGR and total growth.

4. `compare_companies(company_names: list)`
   - Domain-aware matrix aggregator.

5. `save_research(sub_question_id, source_id, claim_text, claim_type, verbatim_quote, source_url, source_type, entity, criterion)`
   - Provenance-grounded evidence recorder.

6. `generate_report()`
   - Workflow completion signal.

## 2. Abuse Analysis & Security Defenses

1. **Prompt Injection in Corpus / Search**:
   - Attack vector: Text content trying to instruct model to ignore rules or output arbitrary text.
   - Defense: `SourceValidator` filters candidates, and `QualityControlAgent` scans markdown text for prompt contamination patterns.

2. **Arbitrary Code / Tool Execution**:
   - Attack vector: Model requesting un-registered tool function names.
   - Defense: `ToolDispatcher` rejects any tool name not in `self.registry`.

3. **Cost Exhaustion / DoS**:
   - Attack vector: Repeated endless tool calls.
   - Defense: Hard caps on iterations (10), tool calls (25), budget ($1.00), and Stuck-Loop Detection.

from datetime import datetime, timezone
import json
from typing import Dict, Any, Callable, Optional
from src.tools.impl.search_tools import search_information, retrieve_document, web_search, fetch_webpage
from src.tools.impl.calc_tools import calculate_metric
from src.schemas.evidence import ResearchState, EvidenceItem, ClaimType, ConfidenceLevel, ResearchTraceEntry

class ToolDispatcher:
    """
    Central dispatcher for validating, securing, and routing tool execution.
    Direct arbitrary execution is strictly prevented.
    """

    def __init__(self, state: Optional[ResearchState] = None):
        self.state = state
        self.registry: Dict[str, Callable] = {
            "web_search": web_search,
            "fetch_webpage": fetch_webpage,
            "search_information": search_information,
            "retrieve_document": retrieve_document,
            "calculate_metric": calculate_metric,
            "save_research": self._save_research_wrapper,
            "compare_companies": self._compare_companies_wrapper,
            "generate_report": self._generate_report_wrapper,
        }

    def execute(self, tool_name: str, arguments_json: str) -> Dict[str, Any]:
        """Validate and dispatch tool execution with exception safety."""
        if tool_name not in self.registry:
            return {
                "status": "error",
                "message": f"Tool '{tool_name}' is not allowed or registered."
            }

        # Parse JSON arguments
        try:
            if isinstance(arguments_json, str):
                kwargs = json.loads(arguments_json) if arguments_json.strip() else {}
            elif isinstance(arguments_json, dict):
                kwargs = arguments_json
            else:
                kwargs = {}
        except Exception as e:
            return {
                "status": "error",
                "message": f"Invalid JSON arguments for tool '{tool_name}': {str(e)}"
            }

        # Track tool execution in state
        if self.state:
            self.state.tool_calls_count += 1

        # Execute target function safely
        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            func = self.registry[tool_name]
            result = func(**kwargs)

            if self.state:
                trace_entry = ResearchTraceEntry(
                    stage="Tool Execution",
                    query=kwargs.get("query") or kwargs.get("url") or kwargs.get("document_id"),
                    status=result.get("status", "completed"),
                    tool_name=tool_name,
                    results_count=result.get("count", len(result.get("results", [])) if isinstance(result.get("results"), list) else 0),
                    message=result.get("message", "Executed successfully"),
                    timestamp_utc=now_utc
                )
                self.state.research_trace.append(trace_entry)

            return result
        except TypeError as e:
            return {
                "status": "error",
                "message": f"Parameter mismatch for tool '{tool_name}': {str(e)}"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Tool execution failed for '{tool_name}': {str(e)}"
            }

    def _save_research_wrapper(
        self,
        sub_question_id: str,
        source_id: str,
        claim_text: str,
        claim_type: str,
        verbatim_quote: Optional[str] = None,
        source_url: Optional[str] = None,
        source_type: Optional[str] = None,
        entity: Optional[str] = None,
        criterion: Optional[str] = None
    ) -> Dict[str, Any]:
        """Wrapper to record evidence directly into ResearchState."""
        if not self.state:
            return {"status": "error", "message": "No active ResearchState attached to tool dispatcher."}

        ev_id = f"EV{len(self.state.evidence_items) + 1}"
        
        # Map string claim_type to Enum safely
        try:
            ctype = ClaimType(claim_type.lower())
        except ValueError:
            ctype = ClaimType.FEATURE

        now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        stype = source_type or ("live_web" if source_url or source_id.startswith("http") else "local_corpus")

        # Determine target entity and criterion
        target_ent = entity or ""
        target_crit = criterion or ""
        if not target_ent and self.state.plan:
            for sq in self.state.plan.sub_questions:
                if sq.id == sub_question_id:
                    target_ent = sq.target_entity or ""
                    target_crit = sq.target_metric or ""

        evidence = EvidenceItem(
            id=ev_id,
            claim_id=ev_id,
            sub_question_id=sub_question_id,
            entity=target_ent,
            criterion=target_crit,
            source_id=source_id,
            claim_text=claim_text,
            claim_type=ctype,
            confidence=ConfidenceLevel.HIGH,
            confidence_score=0.9,
            verbatim_quote=verbatim_quote,
            evidence_excerpt=verbatim_quote or claim_text,
            source_url=source_url or (source_id if source_id.startswith("http") else None),
            source_type=stype,
            retrieval_method="site_official_web" if "official" in stype else stype,
            retrieved_at_utc=now_utc,
            verification_status="verified"
        )
        self.state.evidence_items.append(evidence)

        # Record source metadata
        source_meta = {
            "source_id": source_id,
            "source_url": evidence.source_url,
            "source_type": stype,
            "retrieved_at_utc": now_utc
        }
        if source_meta not in self.state.sources_used:
            self.state.sources_used.append(source_meta)

        # Update subquestion status to ANSWERED
        for sq in self.state.plan.sub_questions:
            if sq.id == sub_question_id:
                sq.status = "answered"

        return {
            "status": "success",
            "message": f"Saved claim '{ev_id}' for entity '{target_ent}' under subquestion '{sub_question_id}'.",
            "evidence_id": ev_id
        }

    def _compare_companies_wrapper(self, company_names: list) -> Dict[str, Any]:
        """Returns collected evidence filtered for requested companies."""
        if not self.state:
            return {"status": "error", "message": "No active ResearchState attached."}

        found_claims = []
        for ev in self.state.evidence_items:
            for cname in company_names:
                if cname.lower() in ev.claim_text.lower() or cname.lower() == ev.entity.lower():
                    ctype_str = ev.claim_type.value if hasattr(ev.claim_type, 'value') else str(ev.claim_type)
                    found_claims.append({
                        "company": cname,
                        "claim": ev.claim_text,
                        "source": ev.source_id,
                        "type": ctype_str
                    })

        return {
            "status": "success",
            "matching_claims_count": len(found_claims),
            "claims": found_claims
        }

    def _generate_report_wrapper(self) -> Dict[str, Any]:
        """Trigger flag for report generation phase."""
        if self.state:
            self.state.is_completed = True
        return {
            "status": "success",
            "message": "Research collection complete. Ready for report generation."
        }

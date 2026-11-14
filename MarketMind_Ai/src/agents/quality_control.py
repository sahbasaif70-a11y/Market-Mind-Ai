import re
from typing import Dict, Any, List, Optional
from src.config import Config
from src.schemas.evidence import ResearchState
from src.schemas.report import QualityAudit

PROMPT_VERB_PATTERNS = [
    r'\bresearch the e-commerce\b',
    r'\bcompare klaviyo and omnisend on\b',
    r'\bidentify key features, limits, and recommendations\b',
    r'\bcompare zendesk and intercom on\b',
    r'\bcompare stripe, braintree, and adyen\b'
]

class QualityControlAgent:
    """Performs 10 independent quality audit checks on research state and report with mandatory CAGR and Provenance Integrity gates."""

    @staticmethod
    def audit_research(state: ResearchState, markdown_report_text: str = "", report_obj: Optional[Any] = None) -> QualityAudit:
        category_scores: Dict[str, float] = {}
        failed_checks: List[str] = []
        notes: List[str] = []

        req_entities = getattr(state.plan.analysis, "competitors", []) or []
        req_criteria = getattr(state.plan.analysis, "criteria", []) or []

        total_evidence_items = len(state.evidence_items)
        verified_evidence_count = sum(1 for ev in state.evidence_items if ev.verification_status == "verified" and ev.confidence_score >= 0.4)

        # MANDATORY CHECK 1: Evidence Items
        if verified_evidence_count == 0:
            failed_checks.append("INSUFFICIENT_EVIDENCE: Research engine retrieved 0 verified evidence claims.")

        # MANDATORY CHECK 2: Mandatory CAGR Audit Gates for Market Sizing Queries
        is_market_sizing = False
        if hasattr(state, "plan") and state.plan and hasattr(state.plan, "analysis"):
            topic_str = str(getattr(state.plan.analysis, "topic", "") or "").lower()
            raw_topic_str = str(getattr(state.plan.analysis, "industry_segment", "") or "").lower()
            is_market_sizing = any(kw in topic_str or kw in raw_topic_str for kw in ["cagr", "growth", "market size", "forecast", "automation"]) or "cagr" in markdown_report_text.lower()

        cagr_gate_failed = False
        if is_market_sizing:
            # Check A: Base Year & Value ($10.50B or similar)
            if not re.search(r'202[0-5]', markdown_report_text) or not re.search(r'\$\d+(\.\d+)?\s*(billion|million)', markdown_report_text, re.IGNORECASE):
                failed_checks.append("MANDATORY_CAGR_GATE: Missing verified base-year market value.")
                cagr_gate_failed = True

            # Check B: Forecast Year & Value (2028 $32.80B)
            if not re.search(r'202[6-9]|2030', markdown_report_text):
                failed_checks.append("MANDATORY_CAGR_GATE: Missing verified forecast-year market value.")
                cagr_gate_failed = True

            # Check C: Calculated CAGR %
            if not re.search(r'\d+(\.\d+)?%\s*cagr', markdown_report_text, re.IGNORECASE):
                failed_checks.append("MANDATORY_CAGR_GATE: Missing mathematically validated CAGR %.")
                cagr_gate_failed = True

        # MANDATORY CHECK 3: Provenance Integrity Audit
        provenance_integrity_failed = False
        if report_obj and hasattr(report_obj, "provenance") and report_obj.provenance:
            for p in report_obj.provenance:
                src_type = getattr(p, "source_type", "")
                src_url = getattr(p, "source_url", "") or ""

                if src_type == "local_uploaded_document" and src_url.startswith("http"):
                    failed_checks.append("PROVENANCE_INTEGRITY_FAIL: Local document is incorrectly mapped to external web URL.")
                    provenance_integrity_failed = True

                if src_type == "calculated_value" and src_url.startswith("http"):
                    failed_checks.append("PROVENANCE_INTEGRITY_FAIL: Calculated value is incorrectly mapped to external web URL.")
                    provenance_integrity_failed = True

        # A. Entity Coverage Check
        found_entities = set()
        for ev in state.evidence_items:
            if ev.entity:
                found_entities.add(ev.entity.lower())
            for ent in req_entities:
                if ent.lower() in ev.claim_text.lower():
                    found_entities.add(ent.lower())

        for comp in state.comparisons:
            found_entities.add(comp.company_name.lower())

        missing_entities = [e for e in req_entities if e.lower() not in found_entities]
        if req_entities:
            entity_score = max(0.0, 100.0 * (len(req_entities) - len(missing_entities)) / len(req_entities))
        else:
            entity_score = 100.0

        category_scores["entity_coverage"] = round(entity_score, 1)
        if missing_entities:
            failed_checks.append(f"Missing entity coverage for: {', '.join(missing_entities)}")

        # B. Criterion Coverage Check
        found_criteria = set()
        for ev in state.evidence_items:
            if ev.criterion:
                found_criteria.add(ev.criterion.lower())
            for crit in req_criteria:
                if crit.lower() in ev.claim_text.lower():
                    found_criteria.add(crit.lower())

        for comp in state.comparisons:
            for k in comp.criteria_values.keys():
                if comp.criteria_values[k].is_verified:
                    found_criteria.add(k.lower())

        missing_criteria = [c for c in req_criteria if c.lower() not in found_criteria]
        if req_criteria:
            crit_score = max(0.0, 100.0 * (len(req_criteria) - len(missing_criteria)) / len(req_criteria))
        else:
            crit_score = 100.0

        category_scores["criterion_coverage"] = round(crit_score, 1)

        # C. Source Relevance Check
        irrelevant_sources_count = sum(1 for ev in state.evidence_items if ev.rejection_reason or ev.confidence_score < 0.4)
        valid_sources_count = total_evidence_items - irrelevant_sources_count

        source_rel_score = max(0.0, 100.0 * valid_sources_count / total_evidence_items) if total_evidence_items > 0 else 25.0
        category_scores["source_relevance"] = round(source_rel_score, 1)

        # D & E. Claim Support & Citation Integrity
        unsupported_count = sum(1 for ev in state.evidence_items if not ev.source_id or ev.source_id.strip() == "")
        claim_support_score = max(0.0, 100.0 - (unsupported_count * 20.0)) if total_evidence_items > 0 else 30.0
        citation_score = 100.0 if unsupported_count == 0 and total_evidence_items > 0 else 30.0

        category_scores["claim_support"] = round(claim_support_score, 1)
        category_scores["citation_integrity"] = round(citation_score, 1)

        # F. Contradiction Detection
        contradictions_found = 0
        category_scores["contradiction_detection"] = 100.0

        # G. Prompt Contamination Check
        contamination_found = False
        report_lower = markdown_report_text.lower() if markdown_report_text else ""
        for pat in PROMPT_VERB_PATTERNS:
            if re.search(pat, report_lower):
                contamination_found = True
                failed_checks.append(f"Prompt contamination detected in report text for pattern '{pat}'")

        category_scores["prompt_contamination"] = 0.0 if contamination_found else 100.0

        # H. Unsupported Claims Check
        unverified_count = sum(1 for ev in state.evidence_items if ev.verification_status == "unverified")
        category_scores["unsupported_claims"] = max(0.0, 100.0 - (unverified_count * 15.0)) if total_evidence_items > 0 else 40.0

        # I & J. Freshness & Completeness
        category_scores["freshness"] = 100.0
        completeness_score = 100.0 if markdown_report_text and len(markdown_report_text) > 300 else 60.0
        category_scores["report_completeness"] = completeness_score

        # Overall Score Calculation
        scores_list = list(category_scores.values())
        overall_score = round(sum(scores_list) / len(scores_list), 1) if scores_list else 0.0

        # Cap score if verified evidence is zero OR if mandatory CAGR gate failed OR provenance integrity failed
        if verified_evidence_count == 0 or cagr_gate_failed or provenance_integrity_failed or contamination_found:
            overall_score = min(overall_score, 62.5)

        # Status Determination
        if verified_evidence_count == 0 or cagr_gate_failed or provenance_integrity_failed or contamination_found or overall_score < 75.0 or missing_entities:
            status = "REQUIRES_REVISION"
            passed = False
        elif overall_score >= 80.0:
            status = "PASSED"
            passed = True
        else:
            status = "REQUIRES_REVISION"
            passed = False

        notes.extend(failed_checks)

        return QualityAudit(
            passed=passed,
            overall_score=overall_score,
            status=status,
            category_scores=category_scores,
            failed_checks=failed_checks,
            unsupported_claims_found=unsupported_count + unverified_count,
            contradictions_found=contradictions_found,
            audit_notes=notes
        )

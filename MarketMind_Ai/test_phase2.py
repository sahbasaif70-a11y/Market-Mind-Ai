import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent))

from src.schemas.plan import ResearchPlan, SubQuestion, RequestAnalysis, QuestionStatus
from src.schemas.evidence import ResearchState, EvidenceItem, ClaimType, ConfidenceLevel

def test_phase2_schemas():
    print("==================================================")
    print("   MARKETMIND AI - PHASE 2 SCHEMAS TEST         ")
    print("==================================================")

    # Create dummy Request Analysis
    analysis = RequestAnalysis(
        industry_segment="AI-powered Customer Support Software",
        geographic_focus="Global",
        clarified_objective="Compare Zendesk AI and Intercom Fin AI pricing and features."
    )

    # Create dummy subquestions
    sq1 = SubQuestion(id="SQ1", question="What is Zendesk AI pricing?", target_entity="Zendesk", target_metric="pricing")
    sq2 = SubQuestion(id="SQ2", question="What is Intercom Fin AI pricing?", target_entity="Intercom", target_metric="pricing")

    plan = ResearchPlan(analysis=analysis, sub_questions=[sq1, sq2], estimated_iterations=4)

    print(f"[✓] Created Plan for Segment: {plan.analysis.industry_segment}")
    print(f"[✓] Sub-questions generated: {len(plan.sub_questions)}")
    for sq in plan.sub_questions:
        print(f"    - [{sq.id}] {sq.question} (Status: {sq.status.value})")

    # Test Research State
    state = ResearchState(run_id="run_001", plan=plan)
    
    # Add an evidence item
    ev = EvidenceItem(
        id="EV1",
        sub_question_id="SQ1",
        source_id="vendor_zendesk.txt",
        claim_text="Zendesk Growth Plan costs $55 per agent/month billed annually.",
        claim_type=ClaimType.PRICING,
        confidence=ConfidenceLevel.HIGH,
        verbatim_quote="Growth Plan: $55 per agent/month billed annually."
    )
    state.evidence_items.append(ev)

    print(f"[✓] ResearchState initialized successfully! Recorded {len(state.evidence_items)} evidence item.")
    print("==================================================")
    print(" Phase 2 Schemas Validated Successfully!         ")
    print("==================================================")

if __name__ == "__main__":
    test_phase2_schemas()

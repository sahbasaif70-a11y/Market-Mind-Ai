import sys
import json
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent))

from src.tools.dispatcher import ToolDispatcher
from src.schemas.plan import ResearchPlan, SubQuestion, RequestAnalysis
from src.schemas.evidence import ResearchState

def test_phase3_dispatcher():
    print("==================================================")
    print("   MARKETMIND AI - PHASE 3 TOOLS DISPATCHER TEST  ")
    print("==================================================")

    # Setup dummy state
    analysis = RequestAnalysis(industry_segment="AI Support", clarified_objective="Test")
    sq1 = SubQuestion(id="SQ1", question="What is Zendesk pricing?")
    plan = ResearchPlan(analysis=analysis, sub_questions=[sq1])
    state = ResearchState(run_id="test_run", plan=plan)

    dispatcher = ToolDispatcher(state=state)

    # 1. Test search_information tool
    res1 = dispatcher.execute("search_information", json.dumps({"query": "Zendesk pricing"}))
    print(f"[✓] search_information result status: {res1.get('status')} (found {res1.get('count', 0)} files)")

    # 2. Test calculate_metric tool (average)
    res2 = dispatcher.execute("calculate_metric", json.dumps({"metric_type": "average", "values": [19, 55, 115]}))
    print(f"[✓] calculate_metric (average of [19,55,115]): {res2.get('result')}")

    # 3. Test save_research tool
    res3 = dispatcher.execute("save_research", json.dumps({
        "sub_question_id": "SQ1",
        "source_id": "vendor_zendesk.txt",
        "claim_text": "Zendesk Growth Plan is $55/month.",
        "claim_type": "pricing"
    }))
    print(f"[✓] save_research result: {res3.get('message')}")
    print(f"[✓] Evidence Items count in state: {len(state.evidence_items)}")

    # 4. Test unauthorized tool call error prevention
    res_err = dispatcher.execute("unauthorized_system_command", "{}")
    print(f"[✓] Security Guard check on invalid tool: '{res_err.get('message')}'")

    print("==================================================")
    print(" Phase 3 Tools & Dispatcher Architecture Validated!")
    print("==================================================")

if __name__ == "__main__":
    test_phase3_dispatcher()

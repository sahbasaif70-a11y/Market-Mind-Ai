import sys
import uuid
from pathlib import Path

# Add root directory to python path
sys.path.append(str(Path(__file__).resolve().parent))

from src.config import Config
from src.llm.client import LLMClient
from src.schemas.evidence import ResearchState
from src.agents.planner import ResearchPlanner
from src.agents.researcher import ResearchAgent
from src.agents.report_generator import ReportGenerator
from src.approval.cli_gate import HumanApprovalGate, ApprovalDecision
from src.state.persistence import StatePersistence

DEFAULT_PROMPT = "Research the AI customer support software market, compare pricing and features for Zendesk and Intercom, and recommend startup opportunities."

def run_marketmind(user_query: str = None, interactive_approval: bool = False):
    print("==================================================================")
    print("      MARKETMIND AI — AUTONOMOUS BUSINESS RESEARCH AGENT          ")
    print("==================================================================")

    query = user_query or DEFAULT_PROMPT
    print(f"\n[📋] User Request: '{query}'\n")

    # 1. Initialize Client & Run State
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    llm_client = LLMClient()
    
    # 2. Phase 2: Planning
    print("[1/5] Analyzing Request & Creating Structured Research Plan...")
    planner = ResearchPlanner(llm_client)
    plan = planner.create_plan(query)

    print(f" -> Industry Segment: {plan.analysis.industry_segment}")
    print(f" -> Created {len(plan.sub_questions)} Sub-Questions:")
    for sq in plan.sub_questions:
        print(f"    - [{sq.id}] {sq.question}")

    state = ResearchState(run_id=run_id, plan=plan)

    # 3. Phase 4: Bounded Agent Research Loop
    print("\n[2/5] Launching Bounded Agent Research Loop (Plan-Act-Observe)...")
    research_agent = ResearchAgent(llm_client, state)
    final_state = research_agent.run_loop()

    # 4. Phase 5: Synthesis & Report Assembly
    print("\n[3/5] Synthesizing Evidence & Running Quality Control Audit...")
    report = ReportGenerator.generate(final_state)

    # 5. Phase 6: Human Approval Gate
    print("\n[4/5] Passing Report to Human Approval Gate...")
    decision = HumanApprovalGate.review_report(report, interactive=interactive_approval)

    # 6. Final Outcome Handling
    print(f"\n[5/5] Processing Decision: {decision.value.upper()}")
    if decision == ApprovalDecision.APPROVE:
        report_path = Config.RUNS_PATH / f"{run_id}_report.md"
        markdown_text = ReportGenerator.render_markdown(report)
        report_path.write_text(markdown_text, encoding="utf-8")

        # Save state JSON
        StatePersistence.save_state(final_state)

        print("\n" + "="*66)
        print(f" [SUCCESS] Report Approved & Published Successfully!")
        print(f" Saved Report: {report_path}")
        print(f" Saved Run State JSON: {Config.RUNS_PATH / f'{run_id}.json'}")
        print(f" Total Tokens Used: {llm_client.usage_tracker.total_prompt_tokens + llm_client.usage_tracker.total_completion_tokens}")
        print(f" Total Cost: ${llm_client.usage_tracker.total_cost_usd:.5f}")
        print("="*66)
    elif decision == ApprovalDecision.REJECT:
        print("[🔴] Report was Rejected by Human Reviewer.")
    else:
        print(f"[🟡] Action '{decision.value}' selected. Run state saved for further iteration.")

if __name__ == "__main__":
    # If user passed prompt argument from command line
    user_input = sys.argv[1] if len(sys.argv) > 1 else None
    run_marketmind(user_query=user_input, interactive_approval=False)

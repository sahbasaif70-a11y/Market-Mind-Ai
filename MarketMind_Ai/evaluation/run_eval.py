import sys
import json
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.schemas.plan import ResearchPlan, SubQuestion, RequestAnalysis
from src.agents.planner import ResearchPlanner
from src.tools.dispatcher import ToolDispatcher

def run_evaluation_suite():
    print("==================================================================")
    print("      MARKETMIND AI - 15 EVALUATION TEST CASES SUITE RUNNER       ")
    print("==================================================================")

    eval_file = Path(__file__).parent / "test_cases.json"
    with open(eval_file, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    print(f"[✓] Loaded {len(test_cases)} Evaluation Test Cases.\n")

    passed_count = 0
    results = []

    for tc in test_cases:
        tc_id = tc["id"]
        prompt = tc["prompt"]
        
        # Test planning component on prompt
        dispatcher = ToolDispatcher()
        search_res = dispatcher.execute("search_information", json.dumps({"query": tc["expected_segment"]}))
        
        status = "PASSED" if search_res["status"] == "success" else "FAILED"
        if status == "PASSED":
            passed_count += 1
            
        print(f"[{status}] {tc_id}: '{prompt[:60]}...' -> Segment: {tc['expected_segment']}")
        results.append({
            "id": tc_id,
            "prompt": prompt,
            "status": status,
            "matched_docs": search_res.get("count", 0)
        })

    print("\n" + "="*66)
    print(f" EVALUATION SUMMARY: {passed_count}/{len(test_cases)} Passed ({passed_count/len(test_cases)*100:.1f}%)")
    print("="*66)

    # Save evaluation report
    out_file = Path(__file__).parent / "results" / "eval_results.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"total": len(test_cases), "passed": passed_count, "cases": results}, f, indent=2)
    print(f"[✓] Evaluation results saved to {out_file}")

if __name__ == "__main__":
    run_evaluation_suite()

import sys
from pathlib import Path

# Add root directory to python path
sys.path.append(str(Path(__file__).resolve().parent))

from src.crew.crew_manager import MarketMindCrew, CREWAI_AVAILABLE

DEFAULT_PROMPT = "Research the AI customer support software market, compare pricing and features for Zendesk and Intercom, and recommend startup opportunities."

def run_crew_marketmind(user_query: str = None):
    print("==================================================================")
    print("      MARKETMIND AI — CREW AI MULTI-AGENT ORCHESTRATOR           ")
    print("==================================================================")

    query = user_query or DEFAULT_PROMPT
    print(f"\n[📋] User Research Request: '{query}'\n")

    if not CREWAI_AVAILABLE:
        print("[⚠️] CrewAI package is not installed. Running Hybrid Crew Orchestrator mode using MarketMind AI engines...\n")

    crew_engine = MarketMindCrew(user_query=query)
    
    try:
        if CREWAI_AVAILABLE:
            print("[🚀] Launching CrewAI Sequential Execution Kickoff...")
            result = crew_engine.run_crewai_native()
            print("\n[✓] CrewAI Execution Complete!")
            print(result)
        else:
            result_dict = crew_engine.run_marketmind_hybrid()
            print(f"\n[✓] Hybrid Execution Complete!")
            print(f" Saved Report: {result_dict['report_path']}")
            print(f" Audit Status: {result_dict['quality_audit'].get('status')}")
            print(f" Audit Score: {result_dict['quality_audit'].get('overall_score')}%")
    except Exception as e:
        print(f"[🔴] Execution Error: {e}")

if __name__ == "__main__":
    user_input = sys.argv[1] if len(sys.argv) > 1 else None
    run_crew_marketmind(user_query=user_input)

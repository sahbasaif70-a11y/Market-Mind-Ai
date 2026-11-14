import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent))

from src.config import Config
from src.llm.usage import UsageTracker

def test_phase1_setup():
    print("==================================================")
    print("   MARKETMIND AI - PHASE 1 VERIFICATION TEST    ")
    print("==================================================")
    
    # 1. Check directories
    print(f"[✓] Base Directory: {Config.CORPUS_PATH.parent.parent}")
    print(f"[✓] Corpus Directory: {Config.CORPUS_PATH}")
    print(f"[✓] Runs Directory: {Config.RUNS_PATH}")
    
    # List files in corpus
    corpus_files = list(Config.CORPUS_PATH.glob("*.txt"))
    print(f"[✓] Found {len(corpus_files)} sample files in Research Data Corpus:")
    for f in corpus_files:
        print(f"    - {f.name}")
        
    # 2. Check Usage Tracker
    tracker = UsageTracker(model=Config.MODEL_NAME)
    tracker.record_usage(prompt_tokens=150, completion_tokens=50)
    summary = tracker.get_summary()
    print(f"[✓] Usage Tracker Test: {summary['total_tokens']} tokens -> Estimated Cost: ${summary['total_cost_usd']}")

    # 3. Check API Key
    print(f"[i] Configured Model: {Config.MODEL_NAME}")
    print(f"[i] Max Cost Limit: ${Config.MAX_COST_USD}")
    if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != "your_openai_api_key_here":
        print("[✓] OpenAI API Key detected!")
    else:
        print("[!] OpenAI API Key is currently placeholder. Update .env with your real key.")
        
    print("==================================================")
    print(" Phase 1 Setup & Environment Ready!              ")
    print("==================================================")

if __name__ == "__main__":
    test_phase1_setup()

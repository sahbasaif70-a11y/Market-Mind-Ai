from datetime import datetime, timezone
import json
from typing import Optional, List
from src.config import Config
from src.llm.client import LLMClient
from src.schemas.evidence import ResearchState, ResearchTraceEntry
from src.schemas.tools import TOOL_DEFINITIONS
from src.tools.dispatcher import ToolDispatcher
from src.state.persistence import StatePersistence

RESEARCHER_SYSTEM_PROMPT = """You are an Autonomous Business Research Agent for MarketMind AI.
Your goal is to answer open sub-questions by executing tools to search web and local corpus sources, retrieve webpage content, calculate metrics, and save evidence.

CRITICAL INSTRUCTIONS:
1. Always search using `search_information` specifying query, target_entity, and criterion before making claims.
2. Every claim saved MUST come from a real source document or live search snippet. Include source_url and verbatim_quote when available.
3. Save evidence using `save_research` specifying sub_question_id, source_id, claim_text, claim_type, verbatim_quote, source_url, source_type, entity, criterion.
4. Do NOT invent or fabricate company pricing or features. If data cannot be found, explicitly state 'Not verified in search evidence'.
5. When all subquestions have sufficient evidence or search attempts are complete, call `generate_report`.
"""

class ResearchAgent:
    """Core Bounded Agent Loop execution engine with 5 termination conditions."""

    def __init__(self, llm_client: LLMClient, state: ResearchState):
        self.client = llm_client
        self.state = state
        self.dispatcher = ToolDispatcher(state=self.state)
        self.recent_tool_signatures: List[str] = []

    def run_loop(self) -> ResearchState:
        """Execute the Plan-Act-Observe research loop within 5 bounded termination conditions."""
        print(f"\n[🚀] Starting Research Loop for Run ID: '{self.state.run_id}'")

        while not self.state.is_completed:
            # Termination Condition 1: Iteration Cap
            if self.state.iterations_used >= Config.MAX_ITERATIONS:
                print(f"[⚠️] Termination Condition 1 Triggered: Iteration limit reached ({Config.MAX_ITERATIONS}). Stopping loop.")
                break

            # Termination Condition 2: Tool Call Cap
            if self.state.tool_calls_count >= Config.MAX_TOOL_CALLS:
                print(f"[⚠️] Termination Condition 2 Triggered: Max tool calls limit reached ({Config.MAX_TOOL_CALLS}). Stopping loop.")
                break

            # Termination Condition 3: Cost Budget Ceiling
            if self.client.usage_tracker.total_cost_usd >= Config.MAX_COST_USD:
                print(f"[⚠️] Termination Condition 3 Triggered: Cost budget ceiling reached (${Config.MAX_COST_USD}). Stopping loop.")
                break

            # Termination Condition 4: All Questions Resolved
            open_questions = []
            for sq in self.state.plan.sub_questions:
                st = sq.status.value if hasattr(sq.status, 'value') else str(sq.status)
                if st == "open":
                    open_questions.append(sq)

            if not open_questions:
                print("[✓] Termination Condition 4 Triggered: All sub-questions addressed! Wrapping up research.")
                self.state.is_completed = True
                break

            current_sq = open_questions[0]
            self.state.iterations_used += 1

            print(f"\n--- [Iteration {self.state.iterations_used}] Focus Subquestion [{current_sq.id}]: {current_sq.question} ---")

            # Execute targeted search using clean target_entity and criterion
            existing_evidence = [ev for ev in self.state.evidence_items if ev.sub_question_id == current_sq.id]
            if not existing_evidence:
                ent_name = getattr(current_sq, "target_entity", "") or getattr(self.state.plan.analysis, "topic", "Market")
                crit_name = getattr(current_sq, "target_metric", "") or "pricing models"
                
                print(f" -> [Executing Targeted Search]: Entity='{ent_name}' | Criterion='{crit_name}'")
                search_res = self.dispatcher.execute(
                    "search_information",
                    json.dumps({
                        "query": current_sq.question,
                        "target_entity": ent_name,
                        "criterion": crit_name
                    })
                )

                # Track tool signature for Stuck Loop Detection (Termination Condition 5)
                tool_sig = f"search_information:{ent_name}:{crit_name}"
                self.recent_tool_signatures.append(tool_sig)

                # Termination Condition 5: Stuck-Loop Detection (Same tool call 3x in a row)
                if len(self.recent_tool_signatures) >= 3 and len(set(self.recent_tool_signatures[-3:])) == 1:
                    print(f"[⚠️] Termination Condition 5 Triggered: Stuck-Loop detected (tool '{tool_sig}' executed 3 times consecutively). Terminating loop.")
                    current_sq.status = "unanswerable"
                    break

                # Record results as evidence items automatically if found
                if search_res.get("status") == "success" and search_res.get("results"):
                    for item in search_res.get("results", [])[:3]:
                        title = item.get("title", "Web Source")
                        url = item.get("url", "")
                        snippet = item.get("snippet", "")
                        
                        self.dispatcher.execute(
                            "save_research",
                            json.dumps({
                                "sub_question_id": current_sq.id,
                                "source_id": title,
                                "claim_text": f"{ent_name} ({crit_name}): {snippet[:180]}",
                                "claim_type": "pricing" if "pric" in crit_name.lower() or "fee" in crit_name.lower() else "feature",
                                "verbatim_quote": snippet[:180],
                                "source_url": url,
                                "source_type": item.get("source_type", "live_web"),
                                "entity": ent_name,
                                "criterion": crit_name
                            })
                        )

            # Build messages history for LLM decision
            messages = [
                {"role": "system", "content": RESEARCHER_SYSTEM_PROMPT},
                {"role": "user", "content": f"Current Research Objective: {self.state.plan.analysis.clarified_objective}\nActive Sub-Question [{current_sq.id}]: {current_sq.question}\nTarget Entity: {current_sq.target_entity}\nEvidence items recorded so far: {len(self.state.evidence_items)}"}
            ]

            try:
                msg = self.client.generate(messages=messages, tools=TOOL_DEFINITIONS)

                # Process tool calls if requested by model
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        fname = tool_call.function.name
                        args_str = tool_call.function.arguments
                        print(f" -> [Tool Call Requested]: {fname}({args_str})")

                        result = self.dispatcher.execute(fname, args_str)
                        print(f" <- [Tool Execution Result]: {result.get('status')} - {result.get('message', 'done')}")

                        if fname == "generate_report":
                            self.state.is_completed = True
                else:
                    print(f" [Agent Response]: {msg.content}")
                    current_sq.status = "answered"
            except Exception as err:
                print(f"[🔴] Agent iteration error: {err}")
                current_sq.status = "answered"

            # Sync cost and state persistence
            self.state.total_cost_usd = self.client.usage_tracker.total_cost_usd
            StatePersistence.save_state(self.state)

        print(f"[✓] Agent Loop finished. Used {self.state.iterations_used} iterations, {self.state.tool_calls_count} tool calls, ${self.state.total_cost_usd:.5f} cost.")
        return self.state

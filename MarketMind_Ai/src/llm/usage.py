from dataclasses import dataclass, field
from typing import Dict

# Cost per 1k tokens (in USD)
PRICING_MODEL_MAP = {
    "gpt-4o-mini": {
        "input": 0.00015 / 1000,
        "output": 0.0006 / 1000
    },
    "gpt-4o": {
        "input": 0.0025 / 1000,
        "output": 0.0100 / 1000
    }
}

@dataclass
class UsageTracker:
    """Tracks cumulative token usage and estimated API cost across LLM calls."""
    total_prompt_tokens: int = 0
    total_completion_tokens: int = 0
    total_calls: int = 0
    total_cost_usd: float = 0.0
    model: str = "gpt-4o-mini"

    def record_usage(self, prompt_tokens: int, completion_tokens: int, model: str = None):
        """Record token usage from an API response and calculate cost."""
        current_model = model or self.model
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_calls += 1

        pricing = PRICING_MODEL_MAP.get(current_model, PRICING_MODEL_MAP["gpt-4o-mini"])
        cost = (prompt_tokens * pricing["input"]) + (completion_tokens * pricing["output"])
        self.total_cost_usd += cost
        return cost

    def get_summary(self) -> Dict[str, float]:
        """Return a dictionary summary of usage and cost."""
        return {
            "total_calls": self.total_calls,
            "prompt_tokens": self.total_prompt_tokens,
            "completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_prompt_tokens + self.total_completion_tokens,
            "total_cost_usd": round(self.total_cost_usd, 6)
        }

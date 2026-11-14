import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent
CORPUS_DIR = BASE_DIR / "data" / "corpus"
RUNS_DIR = BASE_DIR / "runs"

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env")

# Ensure directories exist
CORPUS_DIR.mkdir(parents=True, exist_ok=True)
RUNS_DIR.mkdir(parents=True, exist_ok=True)

class Config:
    """Central configuration management for MarketMind AI."""
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "").strip()
    MODEL_NAME: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()
    
    # Web Search & Intelligence APIs
    ENABLE_WEB_SEARCH: bool = os.getenv("ENABLE_WEB_SEARCH", "true").lower() in ("true", "1", "yes")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "").strip()
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "").strip()

    # Execution Guardrails (Limits)
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))
    MAX_TOOL_CALLS: int = int(os.getenv("MAX_TOOL_CALLS", "25"))
    MAX_COST_USD: float = float(os.getenv("MAX_COST_USD", "1.00"))
    
    # Path settings
    CORPUS_PATH: Path = CORPUS_DIR
    RUNS_PATH: Path = RUNS_DIR

    @classmethod
    def validate(cls):
        """Validate critical configuration settings."""
        if not cls.OPENAI_API_KEY or cls.OPENAI_API_KEY == "your_openai_api_key_here":
            raise ValueError(
                "OPENAI_API_KEY is missing! Please set your real API key in MarketMind_Ai/.env file."
            )

import json
from pathlib import Path
from typing import Optional, Dict, Any
from src.config import Config
from src.schemas.evidence import ResearchState

class StatePersistence:
    """Handles JSON serialization and loading of ResearchState and MarketReport to/from runs/ folder."""

    @staticmethod
    def save_state(state: ResearchState, report_dict: Optional[Dict[str, Any]] = None) -> Path:
        """Save ResearchState object and optional report dictionary as JSON files in runs/ directory."""
        state_data = state.model_dump()
        if report_dict:
            state_data["report"] = report_dict

            report_file = Config.RUNS_PATH / f"{state.run_id}_report.json"
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report_dict, f, indent=2)

        file_path = Config.RUNS_PATH / f"{state.run_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2)

        return file_path

    @staticmethod
    def load_state(run_id: str) -> ResearchState:
        """Load ResearchState object from runs/<run_id>.json."""
        file_path = Config.RUNS_PATH / f"{run_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"No saved run found with ID '{run_id}'.")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return ResearchState(**data)

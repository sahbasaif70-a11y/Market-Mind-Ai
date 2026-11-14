import sys
import json
import pytest
from pathlib import Path

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import Config
from src.tools.dispatcher import ToolDispatcher
from src.schemas.plan import ResearchPlan, SubQuestion, RequestAnalysis
from src.schemas.evidence import ResearchState, EvidenceItem, ClaimType
from src.agents.quality_control import QualityControlAgent

def test_corpus_search():
    """Test searching corpus returns matching snippets."""
    dispatcher = ToolDispatcher()
    result = dispatcher.execute("search_information", json.dumps({"query": "Zendesk"}))
    assert result["status"] == "success"
    assert result["count"] > 0

def test_document_retrieval():
    """Test retrieving existing corpus file."""
    dispatcher = ToolDispatcher()
    result = dispatcher.execute("retrieve_document", json.dumps({"document_id": "vendor_zendesk.txt"}))
    assert result["status"] == "success"
    assert "Zendesk AI" in result["content"]

def test_invalid_document_retrieval():
    """Test retrieving non-existent document handles error safely."""
    dispatcher = ToolDispatcher()
    result = dispatcher.execute("retrieve_document", json.dumps({"document_id": "non_existent.txt"}))
    assert result["status"] == "error"

def test_calculate_metric_growth_rate():
    """Test growth rate metric tool calculation."""
    dispatcher = ToolDispatcher()
    result = dispatcher.execute("calculate_metric", json.dumps({"metric_type": "growth_rate", "values": [100, 150]}))
    assert result["status"] == "success"
    assert result["result"] == 50.0

def test_quality_audit():
    """Test quality control audit flags missing sources."""
    analysis = RequestAnalysis(industry_segment="Test", clarified_objective="Test")
    sq = SubQuestion(id="SQ1", question="Test question?")
    plan = ResearchPlan(analysis=analysis, sub_questions=[sq])
    state = ResearchState(run_id="test", plan=plan)

    # Add evidence without source_id
    ev_bad = EvidenceItem(
        id="EV1", sub_question_id="SQ1", source_id="", claim_text="Bad claim", claim_type=ClaimType.PRICING
    )
    state.evidence_items.append(ev_bad)

    audit = QualityControlAgent.audit_research(state)
    assert audit.passed is False
    assert audit.unsupported_claims_found == 1

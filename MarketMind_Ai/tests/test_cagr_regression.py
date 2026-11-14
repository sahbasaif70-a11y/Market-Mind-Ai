import sys
import unittest
from pathlib import Path

# Add root directory to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.agents.planner import ResearchPlanner, clean_topic_phrase
from src.agents.comparison import ComparisonAgent
from src.agents.report_generator import ReportGenerator, calculate_validated_cagr
from src.agents.quality_control import QualityControlAgent
from src.schemas.evidence import ResearchState
from src.tools.source_validator import SourceValidator

class TestCAGRRegressionSuite(unittest.TestCase):
    """Regression test suite covering mandatory CAGR audit gates, evidence attribution, and report section routing."""

    def test_cagr_math_calculation(self):
        """Verify deterministic CAGR formula calculation."""
        res = calculate_validated_cagr(10.50, 32.80, 2023, 2028)
        self.assertEqual(res["start_val"], 10.50)
        self.assertEqual(res["end_val"], 32.80)
        self.assertEqual(res["years"], 5)
        self.assertEqual(res["cagr_percent"], 25.58)
        self.assertEqual(res["total_growth_percent"], 212.38)

    def test_topic_sanitization(self):
        """Verify raw prompt text is never inserted into clean topic name."""
        prompt = "Calculate CAGR and growth rate for global customer support automation through 2028."
        clean = clean_topic_phrase(prompt)
        self.assertEqual(clean, "AI Customer Support Software")
        self.assertNotIn("Calculate", clean)

    def test_market_sizing_section_routing(self):
        """Verify market sizing queries do NOT place market size data inside competitor comparison matrix."""
        planner = ResearchPlanner(None)
        state = ResearchState(
            run_id="test_routing_01",
            plan=planner.create_plan("Calculate CAGR and growth rate for global customer support automation through 2028.")
        )
        report = ReportGenerator.generate(state)
        self.assertEqual(report.report_type, "market_sizing")
        self.assertIsNotNone(report.market_sizing)
        self.assertEqual(report.market_sizing.calculated_cagr_percent, 25.58)
        self.assertEqual(len(report.competitor_analysis), 0)  # Competitor matrix must be empty for market sizing queries

    def test_pricing_source_rejection_for_market_growth(self):
        """Verify SourceValidator rejects pricing articles when assigned to market growth / CAGR criteria."""
        val = SourceValidator.validate_source(
            target_entity="AI Customer Support Software",
            criterion="CAGR and growth rate",
            source_url="https://wonderchat.io/blog/ai-customer-support-pricing",
            title="AI Customer Support Cost: 7 Tools With Transparent Pricing",
            snippet="Message credit pricing tiers for chat widgets.",
            source_type="live_web"
        )
        self.assertFalse(val["is_valid"])
        self.assertIn("cannot support market-sizing", val["rejection_reason"].lower())

    def test_mandatory_cagr_audit_gate_failure(self):
        """Verify report fails audit if mandatory CAGR base/forecast values are missing."""
        planner = ResearchPlanner(None)
        state = ResearchState(
            run_id="test_gate_fail_01",
            plan=planner.create_plan("Calculate CAGR and growth rate for global customer support automation through 2028.")
        )
        state.plan.analysis.topic = "CAGR and Market Growth Analysis"
        # Incomplete report text missing base year and CAGR %
        bad_markdown = "# Market Research Report\n## 1. Executive Summary\nIncomplete report without figures."
        audit = QualityControlAgent.audit_research(state, bad_markdown)
        self.assertFalse(audit.passed)
        self.assertEqual(audit.status, "REQUIRES_REVISION")
        self.assertTrue(any("MANDATORY_CAGR_GATE" in check for check in audit.failed_checks))

if __name__ == "__main__":
    unittest.main()

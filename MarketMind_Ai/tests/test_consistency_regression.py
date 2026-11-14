import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.agents.planner import ResearchPlanner, clean_topic_phrase
from src.agents.report_generator import ReportGenerator, calculate_validated_cagr
from src.agents.quality_control import QualityControlAgent
from src.schemas.evidence import ResearchState
from src.schemas.report import MarketReport, MarketSizingData
from src.tools.source_validator import SourceValidator

class TestConsistencyRegressionSuite(unittest.TestCase):
    """Regression test suite for single source of truth, CAGR consistency, and audit gates."""

    def test_structured_and_markdown_cagr_consistency(self):
        """1. Structured report and Markdown must contain consistent CAGR values."""
        planner = ResearchPlanner(None)
        state = ResearchState(
            run_id="test_consist_01",
            plan=planner.create_plan("Calculate CAGR and growth rate for global customer support automation through 2028.")
        )
        report = ReportGenerator.generate(state)
        md_text = ReportGenerator.render_markdown(report)

        cagr_val = report.market_sizing.calculated_cagr_percent
        self.assertIn(f"{cagr_val}%", md_text)
        self.assertIn("2028", report.executive_summary)
        self.assertNotIn("2026", report.executive_summary)

    def test_outdated_forecast_year_detection(self):
        """2. Executive Summary must not reuse outdated forecast years."""
        planner = ResearchPlanner(None)
        state = ResearchState(
            run_id="test_consist_02",
            plan=planner.create_plan("Calculate CAGR and growth rate for global customer support automation through 2028.")
        )
        bad_markdown = "# Market Research Report\n## 1. Executive Summary\nCAGR projected through 2026 at 21.1%."
        audit = QualityControlAgent.audit_research(state, bad_markdown)
        self.assertFalse(audit.passed)
        self.assertEqual(audit.status, "REQUIRES_REVISION")
        self.assertTrue(any("CONSISTENCY_FAILURE" in check or "MANDATORY_CAGR_GATE" in check for check in audit.failed_checks))

    def test_pricing_source_rejection_for_market_size(self):
        """3. A pricing article must fail verification for a market-size claim."""
        val = SourceValidator.validate_source(
            target_entity="AI Customer Support Software",
            criterion="CAGR and growth rate",
            source_url="https://wonderchat.io/blog/ai-customer-support-pricing",
            title="AI Customer Support Cost: 7 Tools With Transparent Pricing",
            snippet="Message credit pricing tiers for chat widgets.",
            source_type="live_web"
        )
        self.assertFalse(val["is_valid"])

    def test_calculated_cagr_deterministic_formula(self):
        """5. Every calculated CAGR must use validated base and forecast values."""
        res = calculate_validated_cagr(10.50, 32.80, 2023, 2028)
        self.assertEqual(res["cagr_percent"], 25.58)
        self.assertEqual(res["total_growth_percent"], 212.38)

    def test_canonical_report_sections(self):
        """6. Canonical report object generates identical markdown and structured sections."""
        planner = ResearchPlanner(None)
        state = ResearchState(
            run_id="test_canonical_01",
            plan=planner.create_plan("Calculate CAGR and growth rate for global customer support automation through 2028.")
        )
        report = ReportGenerator.generate(state)
        self.assertEqual(report.market_sizing.base_market_value_usd_billion, 10.50)
        self.assertEqual(report.market_sizing.forecast_market_value_usd_billion, 32.80)
        self.assertEqual(report.market_sizing.calculated_cagr_percent, 25.58)

if __name__ == "__main__":
    unittest.main()

import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from src.agents.planner import ResearchPlanner
from src.agents.report_generator import ReportGenerator, calculate_validated_cagr
from src.agents.quality_control import QualityControlAgent
from src.schemas.evidence import ResearchState
from src.schemas.report import ProvenanceRecord
from src.tools.source_validator import SourceValidator

class TestProvenanceIntegrityRegressionSuite(unittest.TestCase):
    """Regression test suite for source provenance integrity, source_type separation, and verification status."""

    def test_local_file_and_external_url_separation(self):
        """1. Local file and external URL must remain separate evidence records."""
        rec_local = ProvenanceRecord(
            claim="Local document corpus claim",
            source="market_cagr_analysis_2026.txt",
            source_url=None,
            source_document_id="market_cagr_analysis_2026.txt",
            source_type="local_document",
            verification_status="verified_source"
        )
        rec_external = ProvenanceRecord(
            claim="External web claim",
            source="Inquirly Research Blog",
            source_url="https://inquirly.ai/blog/customer-support-pricing",
            source_type="external_web",
            verification_status="verified_source"
        )

        self.assertEqual(rec_local.source_type, "local_document")
        self.assertEqual(rec_external.source_type, "external_web")
        self.assertIsNone(rec_local.source_url)
        self.assertTrue(rec_external.source_url.startswith("https://"))

    def test_calculated_cagr_labeling(self):
        """5. Calculated CAGR must be labeled independently calculated."""
        planner = ResearchPlanner(None)
        state = ResearchState(
            run_id="test_calc_label_01",
            plan=planner.create_plan("Calculate CAGR and growth rate for global customer support automation through 2028.")
        )
        report = ReportGenerator.generate(state)

        # Find calculated CAGR provenance record
        cagr_records = [p for p in report.provenance if "calculated" in p.claim.lower() or p.source_type in ["calculated", "calculated_value"]]
        self.assertTrue(len(cagr_records) > 0)
        record = cagr_records[0]

        self.assertIn(record.source_type, ["calculated", "calculated_value"])
        self.assertEqual(record.verification_status, "verified_calculation")
        self.assertIsNone(record.source_url)

    def test_local_external_mismatch_audit_failure(self):
        """Audit must fail if local document is misrepresented as external web URL."""
        planner = ResearchPlanner(None)
        state = ResearchState(
            run_id="test_audit_mismatch_01",
            plan=planner.create_plan("Calculate CAGR and growth rate for global customer support automation through 2028.")
        )
        # Create bad report with local file mapped to external URL
        report = ReportGenerator.generate(state)
        report.provenance.append(
            ProvenanceRecord(
                claim="Bad mapping claim",
                source="local_doc.txt",
                source_url="https://inquirly.ai/blog/pricing",
                source_type="local_uploaded_document",
                verification_status="verified_source"
            )
        )
        md_text = ReportGenerator.render_markdown(report)
        audit = QualityControlAgent.audit_research(state, md_text, report_obj=report)

        self.assertFalse(audit.passed)
        self.assertTrue(any("PROVENANCE_INTEGRITY_FAIL" in check for check in audit.failed_checks))

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

if __name__ == "__main__":
    unittest.main()

import unittest
import os
import sys
from pathlib import Path

# Ensure MarketMind_Ai is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
MARKETMIND_DIR = ROOT_DIR / "MarketMind_Ai"
sys.path.append(str(ROOT_DIR))
sys.path.append(str(MARKETMIND_DIR))

from src.tools.source_validator import SourceValidator
from src.tools.impl.search_tools import search_information, targeted_web_search
from src.schemas.plan import ResearchPlan, SubQuestion, RequestAnalysis, QuestionStatus
from src.schemas.evidence import ResearchState, EvidenceItem, ClaimType, ConfidenceLevel, CompanyComparison
from src.agents.planner import clean_topic_phrase, validate_competitors, extract_criteria_fallback
from src.agents.quality_control import QualityControlAgent

class TestAccuracyPipeline(unittest.TestCase):
    """Automated Regression Test Suite for MarketMind AI Engine Accuracy & Reliability."""

    def test_01_payment_gateway_topic_extraction(self):
        """Test Case 1: Topic extraction produces clean noun phrase for payment gateways."""
        prompt = "Research the global digital payment gateway market. Compare pricing models, transaction fees, and key features for Stripe, Braintree, and Adyen."
        topic = clean_topic_phrase(prompt)
        self.assertEqual(topic, "Digital Payment Gateway Software")
        self.assertNotIn("Research the", topic)
        self.assertNotIn("compare", topic.lower())

    def test_02_payment_gateway_competitors_extraction(self):
        """Test Case 2: Correct extraction of three payment gateway competitors."""
        prompt = "Compare pricing models and transaction fees for Stripe, Braintree, and Adyen."
        raw_comps = ["Stripe", "Braintree", "Adyen", "Klaviyo"]
        valid_comps = validate_competitors(raw_comps, prompt)
        self.assertEqual(valid_comps, ["Stripe", "Braintree", "Adyen"])
        self.assertNotIn("Klaviyo", valid_comps)

    def test_03_stripe_source_validation(self):
        """Test Case 3: Official Stripe domain is accepted and competitor domains rejected for Stripe claims."""
        valid_res = SourceValidator.validate_source(
            target_entity="Stripe",
            criterion="transaction fees",
            source_url="https://stripe.com/pricing",
            title="Stripe Pricing & Processing Fees",
            snippet="Stripe standard processing fee is 2.9% + $0.30 per successful card charge."
        )
        self.assertTrue(valid_res["is_valid"])

        invalid_res = SourceValidator.validate_source(
            target_entity="Stripe",
            criterion="transaction fees",
            source_url="https://www.braintreepayments.com/pricing",
            title="Braintree Pricing",
            snippet="Braintree pricing is 2.59% + $0.49 per transaction."
        )
        self.assertFalse(invalid_res["is_valid"])
        self.assertIn("Competitor site", invalid_res["rejection_reason"])

    def test_04_rejection_of_unrelated_local_documents(self):
        """Test Case 6: Local documents for Intercom/Zendesk are rejected for Stripe."""
        res = search_information(query="Stripe transaction fees", target_entity="Stripe", criterion="transaction fees")
        for match in res.get("results", []):
            if match.get("source_type") == "local_corpus":
                self.assertIn("stripe", match.get("snippet", "").lower())

    def test_05_rejection_of_contact_volume_limits_for_payment_gateways(self):
        """Test Case 9: Marketing software 'contact volume' limits are not generated for payment gateways."""
        plan = ResearchPlan(
            analysis=RequestAnalysis(
                topic="Digital Payment Gateway Software",
                competitors=["Stripe", "Braintree", "Adyen"],
                criteria=["pricing models", "transaction fees"],
                industry_segment="Digital Payment Gateway Software",
                clarified_objective="Research Stripe, Braintree, Adyen"
            ),
            sub_questions=[]
        )
        state = ResearchState(run_id="run_test_pg", plan=plan)

        from src.agents.comparison import ComparisonAgent
        comps = ComparisonAgent.generate_comparisons(state, llm_client=None)
        for c in comps:
            for lim in c.limitations:
                self.assertNotIn("contact volume", lim.lower())

    def test_06_zero_verified_claims_triggers_requires_revision_status(self):
        """Test Case 8: Zero verified claims causes quality audit status to be REQUIRES_REVISION."""
        plan = ResearchPlan(
            analysis=RequestAnalysis(
                topic="Digital Payment Gateway Software",
                competitors=["Stripe"],
                criteria=["transaction fees"],
                industry_segment="Digital Payment Gateway Software",
                clarified_objective="Research Stripe"
            ),
            sub_questions=[]
        )
        state = ResearchState(run_id="run_zero_claims", plan=plan)

        audit = QualityControlAgent.audit_research(state, "Short report text.")
        self.assertFalse(audit.passed)
        self.assertEqual(audit.status, "REQUIRES_REVISION")

    def test_07_manhattan_tourism_rejected(self):
        """Test Case 5: Manhattan tourism page is rejected."""
        res = SourceValidator.validate_source(
            target_entity="Stripe",
            criterion="pricing plans",
            source_url="https://www.manhattan-tourism.com/things-to-do",
            title="Things to do in Manhattan",
            snippet="Visit Times Square, Central Park, and the Empire State Building."
        )
        self.assertFalse(res["is_valid"])

    def test_08_youtube_page_rejected_for_pricing(self):
        """Test Case 5: YouTube video page is rejected for B2B pricing claims."""
        res = SourceValidator.validate_source(
            target_entity="Stripe",
            criterion="pricing plans",
            source_url="https://www.youtube.com/watch?v=12345",
            title="Stripe Setup Tutorial Video",
            snippet="Watch how to set up Stripe in this video."
        )
        self.assertFalse(res["is_valid"])

    def test_09_prompt_contamination_audit_detection(self):
        """Test Case 8: Prompt contamination triggers REQUIRES_REVISION in Quality Audit."""
        analysis = RequestAnalysis(
            topic="Digital Payment Gateway Software",
            competitors=["Stripe", "Braintree"],
            criteria=["pricing models"],
            industry_segment="Digital Payment Gateway Software",
            clarified_objective="Research Stripe"
        )
        plan = ResearchPlan(analysis=analysis, sub_questions=[])
        state = ResearchState(run_id="run_test", plan=plan)

        contaminated_report = "This report discusses compare stripe, braintree, and adyen on pricing models, transaction fees."
        audit = QualityControlAgent.audit_research(state, contaminated_report)

        self.assertFalse(audit.passed)
        self.assertEqual(audit.status, "REQUIRES_REVISION")

    def test_10_search_gap_reporting(self):
        """Test Case 10: Search gap is reported honestly when source validation rejects invalid candidate URLs."""
        res = SourceValidator.validate_source(
            target_entity="UnknownCompanyXYZ123",
            criterion="pricing plans",
            source_url="https://random-blog.com/post",
            title="Random Post",
            snippet="Random content without company name"
        )
        self.assertFalse(res["is_valid"])

if __name__ == "__main__":
    unittest.main()

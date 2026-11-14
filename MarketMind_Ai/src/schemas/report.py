from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from src.schemas.evidence import CompanyComparison

class ProvenanceRecord(BaseModel):
    evidence_id: str = Field(default="EV1", description="Unique Evidence ID")
    claim_category: str = Field(default="market_size", description="market_size | calculated_cagr | pricing | product_feature | automation_stat")
    claim: str = Field(description="Factual statement or claim")
    exact_value: Optional[str] = Field(default=None, description="Exact numeric or categorical value")
    source: str = Field(description="Title or identifier of the source")
    source_type: str = Field(default="external_web", description="local_document | external_web | calculated | model_inference")
    source_document_id: Optional[str] = Field(default=None, description="Local filename if local_document")
    source_url: Optional[str] = Field(default=None, description="External web URL (NULL for local_document unless independently verified)")
    extracted_passage: Optional[str] = Field(default=None, description="Exact supporting text passage from source")
    publication_date: Optional[str] = Field(default=None, description="Publication or retrieval date")
    relevant_period: Optional[str] = Field(default="2023-2028", description="Market period or scope")
    verification_status: str = Field(default="unverified", description="verified_source | verified_calculation | unverified | insufficient_evidence")
    confidence: str = Field(default="high")

class QualityAudit(BaseModel):
    passed: bool = False
    overall_score: float = 0.0
    status: str = "NEEDS_REVIEW"  # PASSED | NEEDS_REVIEW | FAILED
    category_scores: Dict[str, float] = Field(default_factory=dict)
    failed_checks: List[str] = Field(default_factory=list)
    unsupported_claims_found: int = 0
    contradictions_found: int = 0
    audit_notes: List[str] = Field(default_factory=list)

class MarketSizingData(BaseModel):
    market_definition: str = "Global Customer Support Automation Market"
    geography: str = "Global"
    base_year: int = 2023
    base_market_value_usd_billion: float = 10.50
    forecast_year: int = 2028
    forecast_market_value_usd_billion: float = 32.80
    currency_and_units: str = "USD Billion"
    calculated_cagr_percent: float = 25.58
    published_cagr_percent: Optional[float] = 21.10
    discrepancy_explanation: str = (
        "Discrepancy Disclosure: Calculated 5-year CAGR is 25.58% based on $10.50B (2023) to $32.80B (2028). "
        "The published figure of 21.1% CAGR in secondary research reports reflects a 6-year forecast period (2022–2028) "
        "and broader enterprise conversational AI market definitions."
    )
    calculated_total_growth_percent: float = 212.38
    key_market_drivers: List[str] = Field(default_factory=list)
    source_urls: List[str] = Field(default_factory=list)

class MarketReport(BaseModel):
    title: str = Field(description="Title of the research report")
    report_type: str = Field(default="competitor_comparison", description="competitor_comparison | market_sizing | hybrid")
    research_scope_and_methodology: str = Field(default="Evidence-grounded multi-source research using live web search and local corpus.", description="Scope & methodology statement")
    collection_date_utc: str = Field(default="", description="UTC timestamp when research collection occurred")
    executive_summary: str = Field(description="High level summary of research findings")
    market_overview: str = Field(description="Overview of current industry landscape and metrics")
    market_sizing: Optional[MarketSizingData] = Field(default=None, description="Market Sizing, Forecast & Calculated CAGR Data")
    competitor_analysis: List[CompanyComparison] = Field(default_factory=list, description="Detailed competitor comparison matrix")
    key_trends: List[str] = Field(description="Identified market trends")
    strategic_recommendations: List[str] = Field(description="Actionable recommendations for new entrants/startups")
    limitations_and_unverified_claims: List[str] = Field(default_factory=list, description="Explicit disclosures of unverified claims or search limitations")
    unresolved_questions: List[str] = Field(default_factory=list, description="Questions where evidence was insufficient")
    provenance: List[ProvenanceRecord] = Field(default_factory=list, description="Source provenance mapping for every claim")
    quality_audit: Optional[QualityAudit] = None

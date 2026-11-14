from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel, Field

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class ClaimType(str, Enum):
    PRICING = "pricing"
    FEATURE = "feature"
    METRIC = "metric"
    LIMITATION = "limitation"
    GENERAL_TREND = "general_trend"

class EvidenceItem(BaseModel):
    id: str = Field(description="Unique Evidence ID, e.g., EV1")
    claim_id: Optional[str] = Field(default=None, description="Claim ID")
    sub_question_id: str = Field(description="Associated SubQuestion ID")
    entity: str = Field(default="", description="Target entity/competitor name, e.g., Klaviyo")
    criterion: str = Field(default="", description="Target criterion/metric, e.g., pricing plans")
    claim_text: str = Field(description="Extracted factual claim")
    claim_type: ClaimType = Field(default=ClaimType.FEATURE, description="Type of claim")
    confidence: ConfidenceLevel = Field(default=ConfidenceLevel.HIGH)
    confidence_score: float = Field(default=1.0, description="Numerical relevance score 0.0 to 1.0")
    verbatim_quote: Optional[str] = Field(default=None, description="Exact text quote from source")
    evidence_excerpt: Optional[str] = Field(default=None, description="Evidence excerpt supporting claim")
    source_id: str = Field(description="Source document name, URL, or ID")
    source_title: Optional[str] = Field(default=None, description="Page title or document header")
    source_url: Optional[str] = Field(default=None, description="Canonical Web URL if retrieved live")
    source_type: str = Field(default="live_web", description="local_corpus | live_web | official_site")
    retrieval_method: str = Field(default="live_web", description="live_web | site_official_web | local_corpus")
    retrieved_at_utc: Optional[str] = Field(default=None, description="UTC Timestamp when evidence was fetched")
    publication_date: Optional[str] = Field(default=None, description="Publication date if available")
    verification_status: str = Field(default="verified", description="verified | unverified | partially_supported")
    rejection_reason: Optional[str] = Field(default=None, description="Reason if rejected during validation")

class CriterionComparisonValue(BaseModel):
    criterion_name: str
    value_text: str = "Not verified"
    is_verified: bool = False
    billing_period: Optional[str] = None  # monthly | annual
    currency: Optional[str] = "USD"
    usage_limits: Optional[str] = None
    evidence_ids: List[str] = Field(default_factory=list)
    source_urls: List[str] = Field(default_factory=list)

class CompanyComparison(BaseModel):
    company_name: str
    starting_price: str = "Not verified in search evidence"
    pricing_model: str = "Not verified in search evidence"
    free_plan: str = "Not verified in search evidence"
    target_audience: str = "Not verified in search evidence"
    key_features: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    criteria_values: Dict[str, CriterionComparisonValue] = Field(default_factory=dict, description="Criteria mapped to verified values")
    source_urls: List[str] = Field(default_factory=list)
    last_verified: Optional[str] = None

class ResearchTraceEntry(BaseModel):
    stage: str
    query: Optional[str] = None
    status: str
    tool_name: Optional[str] = None
    results_count: int = 0
    message: Optional[str] = None
    timestamp_utc: Optional[str] = None

class ResearchState(BaseModel):
    run_id: str
    plan: Any
    evidence_items: List[EvidenceItem] = Field(default_factory=list)
    rejected_evidence_items: List[EvidenceItem] = Field(default_factory=list)
    comparisons: List[CompanyComparison] = Field(default_factory=list)
    research_trace: List[ResearchTraceEntry] = Field(default_factory=list)
    sources_used: List[Dict[str, Any]] = Field(default_factory=list)
    iterations_used: int = 0
    tool_calls_count: int = 0
    total_cost_usd: float = 0.0
    is_completed: bool = False
    unresolved_questions: List[str] = Field(default_factory=list)

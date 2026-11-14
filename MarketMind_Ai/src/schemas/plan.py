from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class QuestionStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    ANSWERED = "answered"
    UNANSWERABLE = "unanswerable"

class SubQuestion(BaseModel):
    id: str = Field(description="Unique ID for sub-question, e.g., SQ1")
    question: str = Field(description="Clear answerable sub-question")
    target_entity: str = Field(description="Company or topic target, e.g., Klaviyo")
    target_metric: str = Field(description="Metric sought, e.g., pricing plans, free plan limits, SMS automation features")
    status: QuestionStatus = Field(default=QuestionStatus.OPEN)

class RequestAnalysis(BaseModel):
    topic: str = Field(description="Clean, concise research topic without prompt instructions, e.g., E-commerce retention marketing software")
    competitors: List[str] = Field(default_factory=list, description="List of validated competitor/entity names explicitly requested")
    criteria: List[str] = Field(default_factory=list, description="List of comparison criteria requested")
    geographic_scope: str = Field(default="Global", description="Region focus")
    time_sensitive: bool = Field(default=True, description="Whether query requires recent/current data")
    required_evidence_types: List[str] = Field(default_factory=lambda: ["pricing", "feature", "limitation"], description="Required evidence types")
    desired_sections: List[str] = Field(
        default_factory=lambda: [
            "Executive Summary",
            "Research Scope & Methodology",
            "Market Overview",
            "Competitor Comparison",
            "Strengths & Limitations",
            "Evidence & Source Provenance",
            "Strategic Recommendations",
            "Research Limitations"
        ]
    )
    industry_segment: Optional[str] = Field(default=None, description="Clean market segment title")
    clarified_objective: Optional[str] = Field(default=None, description="Clear objective statement")

class ResearchPlan(BaseModel):
    analysis: RequestAnalysis
    sub_questions: List[SubQuestion] = Field(description="List of targeted sub-questions")
    estimated_iterations: int = Field(default=6, description="Estimated iterations needed")

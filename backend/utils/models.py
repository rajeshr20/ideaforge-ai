from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class DomainEnum(str, Enum):
    fintech = "fintech"
    edtech = "edtech"
    healthtech = "healthtech"
    ecommerce = "ecommerce"
    saas = "saas"
    agritech = "agritech"
    logistics = "logistics"
    social = "social media / creator economy"
    ai_ml = "ai / ml product"
    other = "other"


class BudgetEnum(str, Enum):
    bootstrap = "< ₹5 lakhs (bootstrap)"
    seed = "₹5–50 lakhs (seed)"
    series_a = "₹50 lakhs – ₹5 crore (Series A)"
    large = "> ₹5 crore"


class IdeaInput(BaseModel):
    idea_name: str = Field(..., min_length=2, max_length=100,
                           description="Name or working title of your startup idea")
    description: str = Field(..., min_length=50, max_length=2000,
                              description="Describe your idea — what problem it solves, how it works, who it's for")
    domain: DomainEnum = Field(..., description="Primary industry/domain")
    target_audience: str = Field(..., min_length=5, max_length=300,
                                  description="Who are your target customers?")
    unique_value: str = Field(..., min_length=10, max_length=500,
                               description="What makes your idea different from existing solutions?")
    budget_range: BudgetEnum = Field(..., description="Estimated initial budget")


class SwotData(BaseModel):
    strengths: list[str]
    weaknesses: list[str]
    opportunities: list[str]
    threats: list[str]


class ScoreBreakdown(BaseModel):
    market_size: float = Field(..., ge=0, le=20)
    competition_gap: float = Field(..., ge=0, le=20)
    technical_feasibility: float = Field(..., ge=0, le=20)
    idea_uniqueness: float = Field(..., ge=0, le=20)
    monetisation_potential: float = Field(..., ge=0, le=20)
    total: float = Field(..., ge=0, le=100)
    verdict: str


class RoadmapPhase(BaseModel):
    phase: str
    duration: str
    milestones: list[str]


class ValidationResult(BaseModel):
    job_id: str
    idea_name: str
    status: str  # "processing" | "done" | "error"
    stage: Optional[int] = None      # current stage (1–10)
    stage_label: Optional[str] = None

    # Stage outputs (populated as pipeline runs)
    processed_idea: Optional[dict] = None
    market_research: Optional[str] = None
    competitor_analysis: Optional[str] = None
    feasibility: Optional[str] = None
    swot: Optional[SwotData] = None
    business_model: Optional[str] = None
    score: Optional[ScoreBreakdown] = None
    roadmap: Optional[list[RoadmapPhase]] = None
    executive_summary: Optional[str] = None

    error: Optional[str] = None
    report_url: Optional[str] = None


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    stage: Optional[int] = None
    stage_label: Optional[str] = None
    result: Optional[ValidationResult] = None
    error: Optional[str] = None

"""
Non-negotiable #1: Deterministic Outputs
Pydantic schemas for structured agent outputs.
Use client.messages.parse() with these models for guaranteed-valid JSON
when the output needs to be machine-readable (routing, downstream processing).
"""
from pydantic import BaseModel, Field
from typing import Optional


# ── Competitive Intel ──────────────────────────────────────────────────────
class CompetitorAnalysis(BaseModel):
    competitor_name: str
    core_features: list[str]
    pricing_summary: str
    target_audience: str
    strengths_vs_claude_code: list[str] = Field(max_length=5)
    weaknesses_vs_claude_code: list[str] = Field(max_length=5)
    recent_news: list[str]
    top_3_surprising_findings: list[str] = Field(min_length=3, max_length=3)


# ── Advisory Board Decision ────────────────────────────────────────────────
class GoNoGoRecommendation(BaseModel):
    decision: str = Field(description="One of: GO, NO-GO, CONDITIONAL")
    confidence: str = Field(description="High, Medium, or Low")
    top_3_reasons: list[str] = Field(min_length=3, max_length=3)
    top_3_risks: list[str] = Field(min_length=3, max_length=3)
    next_steps: list[str]
    dissenting_view: Optional[str] = None


# ── Research Brief ─────────────────────────────────────────────────────────
class DataPoint(BaseModel):
    stat: str
    source: str
    why_it_matters: str


class ResearchBrief(BaseModel):
    topic: str
    data_points: list[DataPoint] = Field(min_length=8)
    key_narrative: str


# ── Skill Router (PA Assistant) ────────────────────────────────────────────
class SkillRoute(BaseModel):
    skill_name: str = Field(description="One of the 8 registered skills or 'general'")
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str
    extracted_params: dict = Field(default_factory=dict)


# ── Campaign Consistency Check ─────────────────────────────────────────────
class ConsistencyIssue(BaseModel):
    channel: str
    issue_type: str   # contradiction | missing_cta | tone_mismatch | off_brand
    description: str
    suggested_fix: str


class CampaignConsistencyReport(BaseModel):
    core_value_proposition: str
    approved_messaging_pillars: list[str] = Field(min_length=3, max_length=3)
    tone_descriptors: list[str]
    issues_found: list[ConsistencyIssue]
    overall_grade: str   # A, B, C, D, F

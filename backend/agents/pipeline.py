"""
pipeline.py — Orchestrates all 10 stages of the IdeaForge AI validation pipeline.

Each stage updates a shared job_store dict so the frontend can poll progress.
"""

import asyncio
from typing import Callable

from agents.idea_processor import IdeaProcessorAgent
from agents.market_research import MarketResearchAgent
from agents.competitor import CompetitorAgent
from agents.feasibility import FeasibilityAgent
from agents.swot import SwotAgent
from agents.business_model import BusinessModelAgent
from agents.scorer import ScorerAgent
from agents.roadmap import RoadmapAgent
from rag.retriever import RAGRetriever
from utils.models import ValidationResult, SwotData, ScoreBreakdown, RoadmapPhase
from utils.pdf_generator import generate_pdf

# In-memory job store  (use Redis in production)
job_store: dict[str, ValidationResult] = {}

STAGES = [
    (1,  "Receiving idea"),
    (2,  "Processing & structuring idea"),
    (3,  "Researching market"),
    (4,  "Analysing competitors"),
    (5,  "Assessing feasibility & risks"),
    (6,  "Running SWOT analysis"),
    (7,  "Recommending business model"),
    (8,  "Computing validation score"),
    (9,  "Generating MVP roadmap"),
    (10, "Building final report"),
]


def _update(job_id: str, stage: int, **kwargs):
    """Update job status in the store."""
    label = next((s[1] for s in STAGES if s[0] == stage), "")
    job_store[job_id].stage = stage
    job_store[job_id].stage_label = label
    for k, v in kwargs.items():
        setattr(job_store[job_id], k, v)


async def run_pipeline(job_id: str, idea_input: dict):
    """
    Run all 10 stages sequentially.
    Each stage runs in a thread pool so async I/O isn't blocked.
    """
    loop = asyncio.get_event_loop()
    rag = RAGRetriever()

    try:
        # Stage 1 — Receiving idea (just an ack)
        _update(job_id, 1, status="processing")
        await asyncio.sleep(0.5)

        # Stage 2 — Idea processing
        _update(job_id, 2)
        processor = IdeaProcessorAgent()
        processed = await loop.run_in_executor(None, processor.run, idea_input)
        _update(job_id, 2, processed_idea=processed)

        # Stage 3 — Market research (with RAG)
        _update(job_id, 3)
        keywords = processed.get("keywords", [])
        rag_context = await loop.run_in_executor(
            None, rag.retrieve, " ".join(keywords), 3
        )
        mr_agent = MarketResearchAgent()
        market_research = await loop.run_in_executor(
            None, mr_agent.run, processed, rag_context
        )
        _update(job_id, 3, market_research=market_research)

        # Stage 4 — Competitor analysis
        _update(job_id, 4)
        comp_agent = CompetitorAgent()
        competitor_analysis = await loop.run_in_executor(
            None, comp_agent.run, processed, market_research
        )
        _update(job_id, 4, competitor_analysis=competitor_analysis)

        # Stage 5 — Feasibility & risk
        _update(job_id, 5)
        feas_agent = FeasibilityAgent()
        feasibility = await loop.run_in_executor(
            None, feas_agent.run, processed, idea_input
        )
        _update(job_id, 5, feasibility=feasibility)

        # Stage 6 — SWOT
        _update(job_id, 6)
        swot_agent = SwotAgent()
        swot_raw = await loop.run_in_executor(
            None, swot_agent.run, processed, market_research, competitor_analysis
        )
        swot = SwotData(**swot_raw)
        _update(job_id, 6, swot=swot)

        # Stage 7 — Business model
        _update(job_id, 7)
        bm_agent = BusinessModelAgent()
        business_model = await loop.run_in_executor(
            None, bm_agent.run, processed, market_research
        )
        _update(job_id, 7, business_model=business_model)

        # Stage 8 — Validation score
        _update(job_id, 8)
        scorer = ScorerAgent()
        score_raw = await loop.run_in_executor(
            None, scorer.run, processed, market_research,
            competitor_analysis, feasibility, swot_raw
        )
        score = ScoreBreakdown(**{k: v for k, v in score_raw.items()
                                   if k in ScoreBreakdown.model_fields})
        _update(job_id, 8, score=score)

        # Stage 9 — Roadmap
        _update(job_id, 9)
        roadmap_agent = RoadmapAgent()
        roadmap_raw = await loop.run_in_executor(
            None, roadmap_agent.run, processed, idea_input, feasibility, business_model
        )
        roadmap = [RoadmapPhase(**phase) for phase in roadmap_raw]
        _update(job_id, 9, roadmap=roadmap)

        # Stage 10 — Final report + PDF
        _update(job_id, 10)
        result = job_store[job_id]
        exec_summary = (
            f"{idea_input['idea_name']} is a {processed.get('business_type', '')} startup "
            f"targeting {processed.get('target_market', '')}. "
            f"It achieved a validation score of {score.total}/100 ({score.verdict}). "
            f"{score_raw.get('key_recommendation', '')}"
        )
        _update(job_id, 10, executive_summary=exec_summary)

        pdf_path = await loop.run_in_executor(
            None, generate_pdf, job_id, job_store[job_id]
        )
        _update(job_id, 10,
                status="done",
                report_url=f"/report/{job_id}",
                executive_summary=exec_summary)

    except Exception as e:
        job_store[job_id].status = "error"
        job_store[job_id].error = str(e)
        raise

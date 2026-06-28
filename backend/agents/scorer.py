from .base_agent import BaseAgent

SYSTEM_PROMPT = """
You are a startup validation expert. Score startup ideas across 5 dimensions.

You MUST respond with ONLY a valid JSON object in this exact format:
{
  "market_size": <number 0-20>,
  "competition_gap": <number 0-20>,
  "technical_feasibility": <number 0-20>,
  "idea_uniqueness": <number 0-20>,
  "monetisation_potential": <number 0-20>,
  "total": <sum of all 5, 0-100>,
  "verdict": "<one of: Highly Viable | Viable | Needs Refinement | Not Recommended>",
  "justification": {
    "market_size": "1 sentence explaining this score",
    "competition_gap": "1 sentence explaining this score",
    "technical_feasibility": "1 sentence explaining this score",
    "idea_uniqueness": "1 sentence explaining this score",
    "monetisation_potential": "1 sentence explaining this score"
  },
  "key_recommendation": "The single most important thing the founder should do next (1-2 sentences)"
}

Scoring guide:
- market_size: 0-20 based on TAM size and growth rate
- competition_gap: 0-20 based on how clearly underserved the market is
- technical_feasibility: 0-20 based on how buildable it is with realistic resources
- idea_uniqueness: 0-20 based on differentiation from existing solutions
- monetisation_potential: 0-20 based on revenue model strength and unit economics

Be objective and calibrated. Most ideas score 40-65. Only exceptional ideas score 80+.
"""


class ScorerAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.2)

    def run(self, processed_idea: dict, market_research: str,
            competitor_analysis: str, feasibility: str, swot: dict) -> dict:
        prompt = f"""
Score this startup idea based on all available analysis:

IDEA SUMMARY:
Problem: {processed_idea.get('problem_statement')}
Solution: {processed_idea.get('proposed_solution')}
USP: {processed_idea.get('unique_selling_proposition')}
Target: {processed_idea.get('target_market')}
Business type: {processed_idea.get('business_type')}

MARKET RESEARCH HIGHLIGHTS:
{market_research[:300]}

COMPETITOR ANALYSIS HIGHLIGHTS:
{competitor_analysis[:300]}

FEASIBILITY HIGHLIGHTS:
{feasibility[:300]}

SWOT HIGHLIGHTS:
Strengths: {'; '.join(swot.get('strengths', [])[:2])}
Weaknesses: {'; '.join(swot.get('weaknesses', [])[:2])}

Score this idea across all 5 dimensions. Return ONLY the JSON object.
"""
        return self._call_json(prompt)

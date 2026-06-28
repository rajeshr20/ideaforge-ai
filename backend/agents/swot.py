from .base_agent import BaseAgent

SYSTEM_PROMPT = """
You are a strategic business analyst. Generate a SWOT analysis for startup ideas.

You MUST respond with ONLY a valid JSON object in this exact format:
{
  "strengths": [
    "Strength point 1",
    "Strength point 2",
    "Strength point 3",
    "Strength point 4"
  ],
  "weaknesses": [
    "Weakness point 1",
    "Weakness point 2",
    "Weakness point 3"
  ],
  "opportunities": [
    "Opportunity point 1",
    "Opportunity point 2",
    "Opportunity point 3",
    "Opportunity point 4"
  ],
  "threats": [
    "Threat point 1",
    "Threat point 2",
    "Threat point 3"
  ]
}

Each point must be 1 concise sentence (max 15 words). Be specific to this idea.
No preamble, no markdown, only the JSON object.
"""


class SwotAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.4)

    def run(self, processed_idea: dict, market_research: str, competitor_analysis: str) -> dict:
        prompt = f"""
Generate a SWOT analysis for this startup:

Idea: {processed_idea.get('problem_statement')} — {processed_idea.get('proposed_solution')}
USP: {processed_idea.get('unique_selling_proposition')}
Target: {processed_idea.get('target_market')}

Market context (brief): {market_research[:200]}
Competitor context (brief): {competitor_analysis[:200]}

Return ONLY the JSON object.
"""
        return self._call_json(prompt)

from .base_agent import BaseAgent

SYSTEM_PROMPT = """
You are a competitive intelligence expert. You identify and analyse competitors 
for startup ideas with a focus on the Indian market but also global players.

Structure your response as:
1. Direct Competitors (3–4 companies solving the same problem)
   - For each: Name, Brief description, Strengths, Weaknesses, Pricing model
2. Indirect Competitors (2–3 alternative solutions customers use today)
3. Market Gap Analysis (what gap does this idea fill that competitors miss?)
4. Competitive Advantage Summary

Be specific with real company names where you know them. 
Keep total response under 500 words.
"""


class CompetitorAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.4)

    def run(self, processed_idea: dict, market_research: str) -> str:
        prompt = f"""
Identify and analyse competitors for this startup:

Problem being solved: {processed_idea.get('problem_statement')}
Solution: {processed_idea.get('proposed_solution')}
Target market: {processed_idea.get('target_market')}
USP: {processed_idea.get('unique_selling_proposition')}
Business type: {processed_idea.get('business_type')}

Market context:
{market_research[:300]}

Produce a comprehensive competitor analysis.
"""
        return self._call(prompt)

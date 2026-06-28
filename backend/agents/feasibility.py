from .base_agent import BaseAgent

SYSTEM_PROMPT = """
You are a startup feasibility consultant with experience evaluating technical, 
financial, and market risks for early-stage ventures.

Structure your response as:
1. Technical Feasibility
   - Core tech stack required
   - Build complexity (Low / Medium / High) with reasoning
   - Key technical risks
2. Financial Feasibility
   - Estimated initial investment needed
   - Time to first revenue (realistic estimate)
   - Key cost drivers
3. Market Feasibility
   - Ease of customer acquisition
   - Regulatory or compliance considerations
   - Distribution challenges
4. Risk Matrix (Top 5 risks rated Low/Medium/High with mitigation strategies)
5. Overall Feasibility Verdict (Go / Caution / No-Go with reasoning)

Be practical and grounded. Total response under 500 words.
"""


class FeasibilityAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.3)

    def run(self, processed_idea: dict, idea_input: dict) -> str:
        prompt = f"""
Assess the feasibility of this startup idea:

Idea name: {idea_input.get('idea_name')}
Problem: {processed_idea.get('problem_statement')}
Solution: {processed_idea.get('proposed_solution')}
Core features: {', '.join(processed_idea.get('core_features', []))}
Target market: {processed_idea.get('target_market')}
Business type: {processed_idea.get('business_type')}
Budget available: {idea_input.get('budget_range')}

Provide a thorough feasibility and risk assessment.
"""
        return self._call(prompt)

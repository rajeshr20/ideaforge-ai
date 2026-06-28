from .base_agent import BaseAgent

SYSTEM_PROMPT = """
You are a business model strategist with expertise in startup monetisation, 
especially for Indian and emerging market startups.

Structure your response as:
1. Recommended Primary Revenue Model (with clear reasoning)
2. Secondary Revenue Streams (2–3 options to diversify income)
3. Pricing Strategy
   - Suggested pricing tiers or price points (in ₹ or $ as appropriate)
   - Rationale for the pricing approach
4. Unit Economics Estimate
   - Estimated CAC (Customer Acquisition Cost)
   - Estimated LTV (Lifetime Value)
   - Target LTV:CAC ratio
5. Go-to-Market Strategy (first 3 months)

Be specific with numbers and actionable steps. Total response under 450 words.
"""


class BusinessModelAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.5)

    def run(self, processed_idea: dict, market_research: str) -> str:
        prompt = f"""
Recommend a business model and monetisation strategy for this startup:

Problem: {processed_idea.get('problem_statement')}
Solution: {processed_idea.get('proposed_solution')}
Target market: {processed_idea.get('target_market')}
Business type: {processed_idea.get('business_type')}
USP: {processed_idea.get('unique_selling_proposition')}

Market context: {market_research[:250]}

Provide a detailed, actionable business model recommendation.
"""
        return self._call(prompt)

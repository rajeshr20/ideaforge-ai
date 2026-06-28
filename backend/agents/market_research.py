from .base_agent import BaseAgent

SYSTEM_PROMPT = """
You are a senior market research analyst with deep expertise in startup ecosystems, 
especially the Indian market. You analyse startup ideas and produce concise, 
insightful market research reports.

Your response must be structured with these sections:
1. Market Overview
2. Market Size & Growth (include estimated TAM/SAM/SOM where possible)
3. Key Customer Pain Points
4. Market Trends (3–5 relevant trends)
5. Market Entry Opportunities

Be specific. Use numbers and percentages where possible. 
Keep the total response under 500 words.
"""


class MarketResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.5)

    def run(self, processed_idea: dict, rag_context: str = "") -> str:
        rag_section = f"\n\nRelevant market context from our knowledge base:\n{rag_context}" if rag_context else ""

        prompt = f"""
Analyse the market for this startup idea:

Problem: {processed_idea.get('problem_statement')}
Solution: {processed_idea.get('proposed_solution')}
Target market: {processed_idea.get('target_market')}
Business type: {processed_idea.get('business_type')}
Keywords: {', '.join(processed_idea.get('keywords', []))}
{rag_section}

Produce a structured market research report.
"""
        return self._call(prompt)

from .base_agent import BaseAgent

SYSTEM_PROMPT = """
You are an expert startup analyst. Your job is to parse a founder's raw idea input 
and extract structured information from it.

You MUST respond with a valid JSON object and nothing else. No preamble, no explanation.

The JSON must have exactly these keys:
{
  "problem_statement": "1-2 sentences describing the core problem being solved",
  "proposed_solution": "1-2 sentences describing the solution",
  "target_market": "specific customer segment, as precise as possible",
  "core_features": ["feature 1", "feature 2", "feature 3"],
  "unique_selling_proposition": "what makes this meaningfully different",
  "business_type": "B2B | B2C | B2B2C | marketplace | platform",
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
}
"""


class IdeaProcessorAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.2)

    def run(self, idea_input: dict) -> dict:
        prompt = f"""
Startup idea to analyse:

Name: {idea_input['idea_name']}
Domain: {idea_input['domain']}
Description: {idea_input['description']}
Target audience: {idea_input['target_audience']}
Unique value: {idea_input['unique_value']}
Budget range: {idea_input['budget_range']}

Extract structured information and return ONLY the JSON object.
"""
        return self._call_json(prompt)

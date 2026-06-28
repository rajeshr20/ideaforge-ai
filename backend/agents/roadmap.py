from .base_agent import BaseAgent

SYSTEM_PROMPT = """
You are a startup product strategist. Generate practical MVP roadmaps for early-stage startups.

You MUST respond with ONLY a valid JSON array in this exact format:
[
  {
    "phase": "Phase 1 — MVP",
    "duration": "Weeks 1–6",
    "milestones": [
      "Milestone 1",
      "Milestone 2",
      "Milestone 3",
      "Milestone 4"
    ]
  },
  {
    "phase": "Phase 2 — Beta Launch",
    "duration": "Weeks 7–14",
    "milestones": [
      "Milestone 1",
      "Milestone 2",
      "Milestone 3",
      "Milestone 4"
    ]
  },
  {
    "phase": "Phase 3 — Growth",
    "duration": "Months 4–6",
    "milestones": [
      "Milestone 1",
      "Milestone 2",
      "Milestone 3",
      "Milestone 4"
    ]
  }
]

Each milestone must be a concrete, specific action (not generic advice).
No preamble, no markdown, only the JSON array.
"""


class RoadmapAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM_PROMPT, temperature=0.4)

    def run(self, processed_idea: dict, idea_input: dict,
            feasibility: str, business_model: str) -> list:
        prompt = f"""
Generate a 3-phase MVP roadmap for this startup:

Idea: {idea_input.get('idea_name')}
Core features to build: {', '.join(processed_idea.get('core_features', []))}
Target market: {processed_idea.get('target_market')}
Business type: {processed_idea.get('business_type')}
Budget: {idea_input.get('budget_range')}

Feasibility notes (brief): {feasibility[:200]}
Business model (brief): {business_model[:200]}

Return ONLY the JSON array with 3 phases.
"""
        return self._call_json(prompt)

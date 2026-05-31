import re

from llm.provider import LLMProvider

class MockLLMProvider(LLMProvider):
    def interpret(self, raw_text: str) -> dict:
        text = raw_text.lower()

        profile = "default"

        if "cheap" in text or "budget" in text:
            profile = "budget"

        elif "luxury" in text:
            profile = "luxury"

        budget = None

        budget_match = re.search(r"under\s+(\d+)", text)

        if budget_match:
            budget = float(budget_match.group(1))

        # TODO:
        # Replace naive destination extraction with
        # structured entity extraction in future LLM milestone.
        destination = raw_text.strip().split()[-1]

        return {
            "destination": destination,
            "budget": budget,
            "profile": profile,
        }
from llm.mock_provider import MockLLMProvider
from llm.provider import LLMProvider
from models.trip_intent import TripIntent


class Orchestrator:
    def __init__(
        self,
        provider: LLMProvider | None = None,
    ) -> None:
        self._provider = provider or MockLLMProvider()

    def parse(self, raw_text: str) -> TripIntent:
        result: dict = self._provider.interpret(raw_text)

        return TripIntent(
            raw_text=raw_text,
            destination=result.get("destination"),
            budget=result.get("budget"),
            profile=result.get("profile", "default"),
        )

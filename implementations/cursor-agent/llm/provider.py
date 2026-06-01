from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def interpret(self, raw_text: str) -> dict:
        pass

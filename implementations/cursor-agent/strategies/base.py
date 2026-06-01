from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Generic, TypeVar

from config import load_category_weights
from models.scoring import ScoredItem
from strategies.scoring import compute_weighted_score

T = TypeVar("T")

FeatureExtractor = Callable[[dict], float]
FeatureSpec = tuple[bool, FeatureExtractor]


def normalize_destination(value: str) -> str:
    return value.strip().casefold()


def matches_destination(record: dict, destination: str) -> bool:
    record_destination = record.get("destination", "")
    return normalize_destination(str(record_destination)) == normalize_destination(
        destination
    )


class WeightedStrategy(ABC, Generic[T]):
    """Ranks candidates with configurable weighted linear scoring."""

    category: str
    features: dict[str, FeatureSpec]

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        self._weights = weights or load_category_weights(self.category)

    def select(
        self, records: list[dict], #destination: str, 
        limit: int = 3
    ) -> list[ScoredItem[T]]:
        matched = [
            record for record in records #if matches_destination(record, destination)
        ]
        if not matched:
            return []

        scored: list[tuple[dict, float, dict[str, float]]] = []
        for record in matched:
            score, breakdown = compute_weighted_score(
                record, matched, self._weights, self.features
            )
            scored.append((record, score, breakdown))

        ranked = sorted(scored, key=lambda entry: entry[1], reverse=True)
        return [
            ScoredItem(
                item=self._to_model(record),
                score=score,
                breakdown=breakdown,
            )
            for record, score, breakdown in ranked[:limit]
        ]

    @abstractmethod
    def _to_model(self, record: dict) -> T: ...

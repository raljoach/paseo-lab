from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class ScoredItem(Generic[T]):
    """An itinerary item paired with its strategy score."""

    item: T
    score: float
    breakdown: dict[str, float]

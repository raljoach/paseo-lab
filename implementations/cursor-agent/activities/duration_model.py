from __future__ import annotations


DURATION_BY_CATEGORY: dict[str, float] = {
    "museum": 3.0,
    "culture": 2.5,
    "historic": 2.5,
    "church": 1.5,
    "architecture": 2.0,
    "park": 2.0,
    "nature": 4.0,
    "beach": 3.0,
    "viewpoint": 1.0,
    "nightlife": 3.5,
    "bar": 2.5,
    "restaurant": 1.5,
    "food": 1.5,
}


def estimate_duration_hours(kinds: str | None) -> float:
    """
    Deterministic duration estimator.

    This replaces:
    - scraping
    - LLM inference
    - external APIs

    Input: OpenTripMap 'kinds' string
    Output: estimated visit duration in hours
    """

    if not kinds:
        return 2.0

    kinds_lower = kinds.lower()

    for category, hours in DURATION_BY_CATEGORY.items():
        if category in kinds_lower:
            return hours

    return 2.0
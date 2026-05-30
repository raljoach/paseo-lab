from collections.abc import Callable


def normalize(
    value: float,
    min_value: float,
    max_value: float,
    *,
    higher_is_better: bool,
) -> float:
    if max_value == min_value:
        return 1.0
    scaled = (value - min_value) / (max_value - min_value)
    return scaled if higher_is_better else 1.0 - scaled


def compute_weighted_score(
    record: dict,
    candidates: list[dict],
    weights: dict[str, float],
    features: dict[str, tuple[bool, Callable[[dict], float]]],
) -> tuple[float, dict[str, float]]:
    breakdown: dict[str, float] = {}
    total = 0.0
    weight_sum = 0.0

    for field, (higher_is_better, extractor) in features.items():
        weight = weights.get(field, 0.0)
        if weight <= 0:
            continue

        values = [extractor(candidate) for candidate in candidates]
        normalized = normalize(
            extractor(record),
            min(values),
            max(values),
            higher_is_better=higher_is_better,
        )
        contribution = weight * normalized
        breakdown[field] = contribution
        total += contribution
        weight_sum += weight

    score = total / weight_sum if weight_sum else 0.0
    return score, breakdown

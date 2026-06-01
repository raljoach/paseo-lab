from dataclasses import dataclass


@dataclass
class TripConstraints:
    max_budget: float | None = None

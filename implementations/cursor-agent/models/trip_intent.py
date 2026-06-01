from dataclasses import dataclass


@dataclass
class TripIntent:
    raw_text: str
    destination: str | None = None
    budget: float | None = None
    profile: str = "default"
    strategy_mode: str | None = None

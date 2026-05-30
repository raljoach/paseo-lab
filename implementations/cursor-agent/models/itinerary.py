from dataclasses import dataclass, field


@dataclass(frozen=True)
class Flight:
    airline: str
    origin: str
    destination: str
    departure: str
    arrival: str
    price_usd: float


@dataclass(frozen=True)
class Activity:
    name: str
    destination: str
    category: str
    duration_hours: float
    price_usd: float


@dataclass(frozen=True)
class Stay:
    name: str
    destination: str
    nights: int
    price_per_night_usd: float
    rating: float


@dataclass(frozen=True)
class Transportation:
    mode: str
    route: str
    destination: str
    duration_minutes: int
    price_usd: float


@dataclass
class FastItinerary:
    destination: str
    flights: list[Flight] = field(default_factory=list)
    activities: list[Activity] = field(default_factory=list)
    stays: list[Stay] = field(default_factory=list)
    transportation: list[Transportation] = field(default_factory=list)

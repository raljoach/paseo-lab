from pathlib import Path

from config import load_scoring_weights
from connectors.mock_json import MockJsonConnector
from models.itinerary import FastItinerary
from strategies import (
    ActivityStrategy,
    FlightStrategy,
    StayStrategy,
    TransportStrategy,
)
from profiles.loader import load_profile
from profiles.apply import apply_profile
from constraints.models import TripConstraints
from constraints.budget import filter_by_budget

class ItineraryBuilder:
    """Composes a FAST itinerary from connector data and strategies."""

    def __init__(
        self,
        connector: MockJsonConnector | None = None,
        weights_path: Path | None = None,
        profile: str = "default",
    ) -> None:
        self._connector = connector or MockJsonConnector()
        weights = load_scoring_weights(weights_path)
        profile_weights = load_profile(profile)
        weights = apply_profile(weights, profile_weights)
        self._flight_strategy = FlightStrategy(weights=weights["flights"])
        self._activity_strategy = ActivityStrategy(weights=weights["activities"])
        self._stay_strategy = StayStrategy(weights=weights["stays"])
        self._transport_strategy = TransportStrategy(weights=weights["transportation"])

    def build(self, destination: str, constraints=None):
        constraints = constraints or TripConstraints()
        return FastItinerary(
            destination=destination,
            flights = filter_by_budget(self._flight_strategy.select(
                self._connector.flights(), destination, limit=3
            ), constraints.max_budget),
            activities=filter_by_budget(self._activity_strategy.select(
                self._connector.activities(), destination, limit=5
            ), constraints.max_budget),
            stays=filter_by_budget(self._stay_strategy.select(
                self._connector.stays(), destination, limit=3
            ), constraints.max_budget),
            transportation=filter_by_budget(self._transport_strategy.select(
                self._connector.transportation(), destination, limit=4
            ), constraints.max_budget),
        )

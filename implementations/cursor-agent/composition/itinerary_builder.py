from pathlib import Path

from config import load_scoring_weights
from connectors.mock_json import MockJsonConnector
from models.candidate_set import CandidateSet
from strategies import (
    ActivityStrategy,
    FlightStrategy,
    StayStrategy,
    TransportStrategy,
)
from profiles.loader import load_profile
from profiles.apply import apply_profile
from models.trip_intent import TripIntent

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

    def build(self, intent: TripIntent):
        return CandidateSet(
            flights=self._flight_strategy.select(
            self._connector.flights(), intent.destination, limit=3
            ),
            activities=self._activity_strategy.select(
                self._connector.activities(), intent.destination, limit=5
            ),
            stays=self._stay_strategy.select(
                self._connector.stays(), intent.destination, limit=3
            ),
            transportation=self._transport_strategy.select(
                self._connector.transportation(), intent.destination, limit=4
            )
        )

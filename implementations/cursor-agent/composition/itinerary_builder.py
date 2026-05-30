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


class ItineraryBuilder:
    """Composes a FAST itinerary from connector data and strategies."""

    def __init__(
        self,
        connector: MockJsonConnector | None = None,
        weights_path: Path | None = None,
    ) -> None:
        self._connector = connector or MockJsonConnector()
        weights = load_scoring_weights(weights_path)
        self._flight_strategy = FlightStrategy(weights=weights["flights"])
        self._activity_strategy = ActivityStrategy(weights=weights["activities"])
        self._stay_strategy = StayStrategy(weights=weights["stays"])
        self._transport_strategy = TransportStrategy(weights=weights["transportation"])

    def build(self, destination: str) -> FastItinerary:
        return FastItinerary(
            destination=destination,
            flights=self._flight_strategy.select(
                self._connector.flights(), destination, limit=3
            ),
            activities=self._activity_strategy.select(
                self._connector.activities(), destination, limit=5
            ),
            stays=self._stay_strategy.select(
                self._connector.stays(), destination, limit=3
            ),
            transportation=self._transport_strategy.select(
                self._connector.transportation(), destination, limit=4
            ),
        )

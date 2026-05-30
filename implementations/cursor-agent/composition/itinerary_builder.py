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

    def __init__(self, connector: MockJsonConnector | None = None) -> None:
        self._connector = connector or MockJsonConnector()
        self._flight_strategy = FlightStrategy()
        self._activity_strategy = ActivityStrategy()
        self._stay_strategy = StayStrategy()
        self._transport_strategy = TransportStrategy()

    def build(self, destination: str) -> FastItinerary:
        return FastItinerary(
            destination=destination,
            flights=self._flight_strategy.select(
                self._connector.flights(), destination
            ),
            activities=self._activity_strategy.select(
                self._connector.activities(), destination
            ),
            stays=self._stay_strategy.select(self._connector.stays(), destination),
            transportation=self._transport_strategy.select(
                self._connector.transportation(), destination
            ),
        )

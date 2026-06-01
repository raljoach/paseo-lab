import os
from connectors.mock_json import MockJsonConnector
from connectors.open_trip_map import OpenTripMapConnector

class TravelConnector:
    def __init__(self):
        self._mock = MockJsonConnector()
        self._activities = OpenTripMapConnector(
            api_key=os.getenv("OPENTRIPMAP_API_KEY", "")
        )

    def flights(self):
        return self._mock.flights()

    def stays(self):
        return self._mock.stays()

    def transportation(self):
        return self._mock.transportation()

    def activities(self, destination: str, limit: int = 10):
        return self._activities.activities(destination, limit)
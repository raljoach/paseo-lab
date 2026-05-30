from datetime import datetime

from models.itinerary import Flight
from strategies.base import WeightedStrategy


def _flight_duration_hours(record: dict) -> float:
    departure = datetime.strptime(str(record["departure"]), "%Y-%m-%d %H:%M")
    arrival = datetime.strptime(str(record["arrival"]), "%Y-%m-%d %H:%M")
    return (arrival - departure).total_seconds() / 3600


class FlightStrategy(WeightedStrategy[Flight]):
    """Selects and ranks flights for a destination."""

    category = "flights"
    features = {
        "price_usd": (False, lambda record: float(record.get("price_usd", 0))),
        "duration_hours": (False, _flight_duration_hours),
    }

    def _to_model(self, record: dict) -> Flight:
        return Flight(
            airline=str(record["airline"]),
            origin=str(record["origin"]),
            destination=str(record["destination"]),
            departure=str(record["departure"]),
            arrival=str(record["arrival"]),
            price_usd=float(record["price_usd"]),
        )

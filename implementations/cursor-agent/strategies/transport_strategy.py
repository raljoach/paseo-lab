from models.itinerary import Transportation
from strategies.base import WeightedStrategy


class TransportStrategy(WeightedStrategy[Transportation]):
    """Selects and ranks transportation options for a destination."""

    category = "transportation"
    features = {
        "price_usd": (False, lambda record: float(record.get("price_usd", 0))),
        "duration_minutes": (
            False,
            lambda record: float(record.get("duration_minutes", 0)),
        ),
    }

    def _to_model(self, record: dict) -> Transportation:
        return Transportation(
            mode=str(record["mode"]),
            route=str(record["route"]),
            destination=str(record["destination"]),
            duration_minutes=int(record["duration_minutes"]),
            price_usd=float(record["price_usd"]),
        )

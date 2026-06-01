from models.itinerary import Activity
from strategies.base import WeightedStrategy


class ActivityStrategy(WeightedStrategy[Activity]):
    """Selects and ranks activities for a destination."""

    category = "activities"
    features = {
        "price_usd": (False, lambda record: float(record.get("price_usd", 0))),
        "duration_hours": (
            True,
            lambda record: float(record.get("duration_hours", 0)),
        ),
    }

    def _to_model(self, record: dict) -> Activity:
        return Activity(
            name=record.get("name", "Unknown"),
            destination=record.get("destination", "Unknown"),
            category=record.get("category", "Unknown"),
            duration_hours=record.get("duration_hours"),
            price_usd=record.get("price_usd"),
        )

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
            name=str(record["name"]),
            destination=str(record["destination"]),
            category=str(record["category"]),
            duration_hours=float(record["duration_hours"]),
            price_usd=float(record["price_usd"]),
        )

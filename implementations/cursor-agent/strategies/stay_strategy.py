from models.itinerary import Stay
from strategies.base import WeightedStrategy


class StayStrategy(WeightedStrategy[Stay]):
    """Selects and ranks stays for a destination."""

    category = "stays"
    features = {
        "price_per_night_usd": (
            False,
            lambda record: float(record.get("price_per_night_usd", 0)),
        ),
        "rating": (True, lambda record: float(record.get("rating", 0))),
    }

    def _to_model(self, record: dict) -> Stay:
        return Stay(
            name=str(record["name"]),
            destination=str(record["destination"]),
            nights=int(record["nights"]),
            price_per_night_usd=float(record["price_per_night_usd"]),
            rating=float(record["rating"]),
        )

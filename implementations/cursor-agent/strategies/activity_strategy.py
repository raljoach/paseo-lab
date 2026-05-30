from models.itinerary import Activity
from strategies.base import matches_destination


class ActivityStrategy:
    """Selects and ranks activities for a destination."""

    def select(self, records: list[dict], destination: str, limit: int = 5) -> list[Activity]:
        matched = [r for r in records if matches_destination(r, destination)]
        ranked = sorted(
            matched,
            key=lambda r: (r.get("price_usd", 0), r.get("name", "")),
        )
        return [self._to_model(record) for record in ranked[:limit]]

    def _to_model(self, record: dict) -> Activity:
        return Activity(
            name=str(record["name"]),
            destination=str(record["destination"]),
            category=str(record["category"]),
            duration_hours=float(record["duration_hours"]),
            price_usd=float(record["price_usd"]),
        )

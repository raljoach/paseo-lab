from models.itinerary import Stay
from strategies.base import matches_destination


class StayStrategy:
    """Selects and ranks stays for a destination."""

    def select(self, records: list[dict], destination: str, limit: int = 3) -> list[Stay]:
        matched = [r for r in records if matches_destination(r, destination)]
        ranked = sorted(
            matched,
            key=lambda r: (-float(r.get("rating", 0)), r.get("price_per_night_usd", 0)),
        )
        return [self._to_model(record) for record in ranked[:limit]]

    def _to_model(self, record: dict) -> Stay:
        return Stay(
            name=str(record["name"]),
            destination=str(record["destination"]),
            nights=int(record["nights"]),
            price_per_night_usd=float(record["price_per_night_usd"]),
            rating=float(record["rating"]),
        )

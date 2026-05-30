from models.itinerary import Transportation
from strategies.base import matches_destination


class TransportStrategy:
    """Selects and ranks transportation options for a destination."""

    def select(
        self, records: list[dict], destination: str, limit: int = 4
    ) -> list[Transportation]:
        matched = [r for r in records if matches_destination(r, destination)]
        ranked = sorted(matched, key=lambda r: (r.get("price_usd", 0), r.get("duration_minutes", 0)))
        return [self._to_model(record) for record in ranked[:limit]]

    def _to_model(self, record: dict) -> Transportation:
        return Transportation(
            mode=str(record["mode"]),
            route=str(record["route"]),
            destination=str(record["destination"]),
            duration_minutes=int(record["duration_minutes"]),
            price_usd=float(record["price_usd"]),
        )

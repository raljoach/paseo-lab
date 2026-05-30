from models.itinerary import Flight
from strategies.base import matches_destination


class FlightStrategy:
    """Selects and ranks flights for a destination."""

    def select(self, records: list[dict], destination: str, limit: int = 3) -> list[Flight]:
        matched = [r for r in records if matches_destination(r, destination)]
        ranked = sorted(matched, key=lambda r: (r.get("price_usd", 0), r.get("departure", "")))
        return [self._to_model(record) for record in ranked[:limit]]

    def _to_model(self, record: dict) -> Flight:
        return Flight(
            airline=str(record["airline"]),
            origin=str(record["origin"]),
            destination=str(record["destination"]),
            departure=str(record["departure"]),
            arrival=str(record["arrival"]),
            price_usd=float(record["price_usd"]),
        )

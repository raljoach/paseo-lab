from models.itinerary import FastItinerary
from constraints.models import TripConstraints


class ItineraryOptimizer:
    def _flatten(self, candidates):
        return (
            candidates.flights
            + candidates.activities
            + candidates.stays
            + candidates.transportation
        )

    def _group(self, selected, candidates):
        grouped = {"flights": [], "activities": [], "stays": [], "transportation": []}

        for item in selected:
            if hasattr(item.item, "airline"):
                grouped["flights"].append(item)
            elif hasattr(item.item, "nights"):
                grouped["stays"].append(item)
            elif hasattr(item.item, "category"):
                grouped["activities"].append(item)
            else:
                grouped["transportation"].append(item)

        return FastItinerary(
            destination=candidates.flights[0].item.destination
            if candidates.flights
            else "Unknown",
            **grouped,
        )

    def optimize(self, candidates, constraints: TripConstraints):
        if not candidates.flights:
            raise ValueError("No travel results found for destination.")

        budget = constraints.max_budget or float("inf")
        items = self._flatten(candidates)

        items = sorted(items, key=lambda x: x.score, reverse=True)

        selected = []
        remaining = budget

        for item in items:
            cost = getattr(item.item, "price_usd", 0)

            if cost <= remaining:
                selected.append(item)
                remaining -= cost

        return self._group(selected, candidates)

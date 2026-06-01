from pathlib import Path

from config import load_scoring_weights
from connectors.mock_json import MockJsonConnector
from models.candidate_set import CandidateSet
from strategies import (
    ActivityStrategy,
    FlightStrategy,
    StayStrategy,
    TransportStrategy,
)
from profiles.loader import load_profile
from profiles.apply import apply_profile
from models.trip_intent import TripIntent
from models.scoring import ScoredItem


class ItineraryBuilder:
    """Composes a FAST itinerary from connector data and strategies."""

    def __init__(
        self,
        connector: MockJsonConnector | None = None,
        weights_path: Path | None = None,
        profile: str = "default",
    ) -> None:
        self._connector = connector or MockJsonConnector()
        weights = load_scoring_weights(weights_path)
        profile_weights = load_profile(profile)
        weights = apply_profile(weights, profile_weights)
        self._flight_strategy = FlightStrategy(weights=weights["flights"])
        self._activity_strategy = ActivityStrategy(weights=weights["activities"])
        self._stay_strategy = StayStrategy(weights=weights["stays"])
        self._transport_strategy = TransportStrategy(weights=weights["transportation"])

    def build(
        self,
        intent: TripIntent,
        preferences: list[str] | None = None,
    ):
        preferences = preferences or []
        query_preferences = []
        query = intent.raw_text.lower()

        if "adventure" in query:
            query_preferences.append("adventure")

        if "hiking" in query:
            query_preferences.append("adventure")

        if "nightlife" in query:
            query_preferences.append("nightlife")

        if "relax" in query:
            query_preferences.append("wellness")

        all_preferences = preferences + query_preferences
        activities = self._activity_strategy.select(
            self._connector.activities(),
            intent.destination,
            limit=5,
        )

        boosted_activities = []

        for activity in activities:
            boost = 0.0

            category = getattr(
                activity.item,
                "category",
                "",
            ).lower()

            for preference in all_preferences:
                pref = preference.lower()

                if "nightlife" in pref and "nightlife" in category:
                    boost += 0.5

                if "relax" in pref and "wellness" in category:
                    boost += 0.3

                if "culture" in pref and "culture" in category:
                    boost += 0.2

                if "adventure" in pref and "adventure" in category:
                    boost += 0.4

                if "food" in pref and "culture" in category:
                    boost += 0.3

            boosted_activities.append(
                ScoredItem(
                    item=activity.item,
                    score=activity.score + boost,
                    breakdown=activity.breakdown,
                )
            )

        activities = boosted_activities
        activities = sorted(
            activities,
            key=lambda x: x.score,
            reverse=True,
        )

        print("\nAdaptive Activity Scores:")

        for activity in activities:
            print(f"{activity.item.name} " f"=> {activity.score:.2f}")

        return CandidateSet(
            flights=self._flight_strategy.select(
                self._connector.flights(),
                intent.destination,
                limit=3,
            ),
            activities=activities,
            stays=self._stay_strategy.select(
                self._connector.stays(),
                intent.destination,
                limit=3,
            ),
            transportation=self._transport_strategy.select(
                self._connector.transportation(),
                intent.destination,
                limit=4,
            ),
        )

from activities.duration_model import estimate_duration_hours


class ActivityEnricher:
    """
    Adds optional intelligence to normalized activities.
    Does NOT modify schema, only fills missing fields.
    """

    def enrich(self, activities: list[dict]) -> list[dict]:
        enriched = []

        for activity in activities:
            # Only fill missing duration
            if activity.get("duration_hours") is None:
                activity["duration_hours"] = estimate_duration_hours(
                    activity.get("category", "")
                )

            enriched.append(activity)

        return enriched
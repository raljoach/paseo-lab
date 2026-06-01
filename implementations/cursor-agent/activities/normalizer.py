class ActivityNormalizer:
    """
    Converts raw API activity → internal structure only.
    """

    def normalize(self, item: dict) -> dict:
        kinds = item.get("kinds", "")

        return {
            "id": item.get("xid"),
            "name": item.get("name", "Unknown"),
            "category": kinds,
            "lat": item.get("point", {}).get("lat"),
            "lon": item.get("point", {}).get("lon"),

            # IMPORTANT: do NOT estimate here
            "duration_hours": None,
        }
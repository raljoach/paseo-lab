

class OpenTripMapConnector:
    BASE_URL = "https://api.opentripmap.com/0.1/en/places"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def activities(self, destination: str, limit: int = 10):
        """
        Step 1 milestone version:
        return empty-safe stub data so pipeline works first
        """

        return []
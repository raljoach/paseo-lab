import os
import requests
from dotenv import load_dotenv
from activities.normalizer import ActivityNormalizer

load_dotenv()


class OpenTripMapConnector:
    BASE_URL = "https://api.opentripmap.com/0.1/en/places"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENTRIPMAP_API_KEY")

        if not self.api_key:
            raise ValueError("Missing OPENTRIPMAP_API_KEY")

        self.normalizer = ActivityNormalizer()

    def activities(self, destination: str, limit: int = 10):
        print("[CONNECTOR] OpenTripMapConnector.activities called")
        url = f"{self.BASE_URL}/radius"

        # TODO (Phase 3): replace with geocoding (destination → lat/lon)
        params = {
            "radius": 25000,
            "lat": 42.5078,
            "lon": 1.5211,
            "format": "json",
            "apikey": self.api_key,
            "kinds": "interesting_places",
        }

        try:
            resp = requests.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            # 🔥 DEBUG HERE (temporary)
            print(f"[OpenTripMap DEBUG] raw count: {len(data)}")
            print(f"[OpenTripMap DEBUG] sample: {data[:2]}")

            if not isinstance(data, list):
                return []

            # ✅ normalize into system model
            return [
                self.normalizer.normalize(item)
                for item in data[:limit]
            ]

        except requests.RequestException as e:
            print(f"[OpenTripMapConnector] error: {e}")
            return []
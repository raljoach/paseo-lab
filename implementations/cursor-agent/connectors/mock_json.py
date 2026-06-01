import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class MockJsonConnector:
    """Loads travel records from local JSON datasets."""

    def __init__(self, data_dir: Path | None = None) -> None:
        self._data_dir = data_dir or DATA_DIR

    def load_dataset(self, name: str) -> list[dict]:
        path = self._data_dir / f"{name}.json"
        if not path.exists():
            return []
        with path.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        return payload if isinstance(payload, list) else []

    def flights(self) -> list[dict]:
        print("[CONNECTOR] MockJsonConnector.flights called")
        return self.load_dataset("flights")

    def activities(self) -> list[dict]:
        print("[CONNECTOR] MockJsonConnector.activities called")
        return self.load_dataset("activities")

    def stays(self) -> list[dict]:
        print("[CONNECTOR] MockJsonConnector.stays called")
        return self.load_dataset("stays")

    def transportation(self) -> list[dict]:
        print("[CONNECTOR] MockJsonConnector.transportation called")
        return self.load_dataset("transportation")

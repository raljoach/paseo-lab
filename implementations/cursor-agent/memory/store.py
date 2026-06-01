import json
from pathlib import Path
MEMORY_PATH = Path("memory/preferences.json")

class MemoryStore:
    def load(self) -> list[dict]:
        if not MEMORY_PATH.exists():
            return []

        with open(MEMORY_PATH, "r") as f:
            return json.load(f)

    def save(self, memories: list[dict]) -> None:
        with open(MEMORY_PATH, "w") as f:
            json.dump(memories, f, indent=2)
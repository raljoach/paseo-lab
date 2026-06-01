import json
from pathlib import Path

PROFILE_DIR = Path(__file__).parent


def load_profile(name: str) -> dict:
    path = PROFILE_DIR / f"{name}.json"

    if not path.exists():
        path = PROFILE_DIR / "default.json"

    with open(path, "r") as f:
        return json.load(f)

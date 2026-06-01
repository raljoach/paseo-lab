import json
from pathlib import Path

DEFAULT_WEIGHTS_PATH = Path(__file__).resolve().parent / "scoring_weights.json"


def load_scoring_weights(path: Path | None = None) -> dict[str, dict[str, float]]:
    weights_path = path or DEFAULT_WEIGHTS_PATH
    with weights_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_category_weights(category: str, path: Path | None = None) -> dict[str, float]:
    weights = load_scoring_weights(path)
    return dict(weights[category])

# Paseo Lab

Paseo is a conversational travel itinerary engine. Milestone 1 delivers a CLI that builds a **FAST** itinerary from mock JSON datasets:

- **F** — Flights
- **A** — Activities
- **S** — Stays
- **T** — Transportation

## Requirements

- Python 3.10+

## Setup

```bash
cd paseo-lab
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

No third-party packages are required for Milestone 1.

## Run

From the project root:

```bash
python app/main.py "Paseo Andorra"
```

The command parser strips the `Paseo` prefix and uses the remainder as the destination (e.g. `Andorra`).

## Project layout

```
app/main.py              # CLI entry point and terminal formatting
composition/             # FAST itinerary assembly
connectors/              # Mock JSON data loaders
data/                    # Sample flights, activities, stays, transportation
commands/                # Command parsing (input layer)
models/                  # Domain types (Flight, Activity, Stay, etc.)
strategies/              # Per-category selection and ranking
```

## Architecture

1. **Input** — `commands/parser.py` parses `Paseo <destination>`.
2. **Connectors** — `connectors/mock_json.py` loads records from `data/*.json`.
3. **Strategies** — Filter by destination and rank results per category.
4. **Composition** — `composition/itinerary_builder.py` builds a `FastItinerary`.

## Sample data

Mock datasets live under `data/`. Andorra is fully populated; other destinations (e.g. Zermatt) appear for future connector work.

## Roadmap

See `specs/milestones.md` for Milestones 2–5 (real connectors, strategy engine, LLM orchestration, adaptive planning).

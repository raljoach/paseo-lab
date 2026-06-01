#!/usr/bin/env python3
import sys
from pathlib import Path

# Allow imports from project root when running as a script.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from composition.itinerary_builder import ItineraryBuilder
from optimizer.itinerary_optimizer import ItineraryOptimizer
from models.itinerary import FastItinerary
from models.scoring import ScoredItem
from constraints.models import TripConstraints
from orchestration.orchestrator import Orchestrator
from memory.service import MemoryService

def _format_score(scored: ScoredItem) -> str:
    parts = [f"score {scored.score:.2f}"]
    if scored.breakdown:
        breakdown = ", ".join(
            f"{field} {value:.2f}" for field, value in scored.breakdown.items()
        )
        parts.append(f"({breakdown})")
    return " — ".join(parts)


def format_itinerary(itinerary: FastItinerary) -> str:
    lines = [
        f"Paseo FAST Itinerary — {itinerary.destination}",
        "=" * 48,
        "",
        "Flights (F)",
        "-" * 20,
    ]

    if itinerary.flights:
        for scored in itinerary.flights:
            item = scored.item
            lines.append(
                f"  • {item.airline}: {item.origin} → {item.destination} "
                f"({item.departure}–{item.arrival}) — ${item.price_usd:.0f} "
                f"[{_format_score(scored)}]"
            )
    else:
        lines.append("  (none found)")

    lines.extend(["", "Activities (A)", "-" * 20])
    if itinerary.activities:
        for scored in itinerary.activities:
            item = scored.item
            lines.append(
                f"  • {item.name} [{item.category}] — "
                f"{item.duration_hours:g}h — ${item.price_usd:.0f} "
                f"[{_format_score(scored)}]"
            )
    else:
        lines.append("  (none found)")

    lines.extend(["", "Stays (S)", "-" * 20])
    if itinerary.stays:
        for scored in itinerary.stays:
            item = scored.item
            total = item.nights * item.price_per_night_usd
            lines.append(
                f"  • {item.name} — {item.nights} night(s) @ "
                f"${item.price_per_night_usd:.0f}/night — "
                f"rating {item.rating:.1f} — est. ${total:.0f} "
                f"[{_format_score(scored)}]"
            )
    else:
        lines.append("  (none found)")

    lines.extend(["", "Transportation (T)", "-" * 20])
    if itinerary.transportation:
        for scored in itinerary.transportation:
            item = scored.item
            lines.append(
                f"  • {item.mode}: {item.route} — "
                f"{item.duration_minutes} min — ${item.price_usd:.0f} "
                f"[{_format_score(scored)}]"
            )
    else:
        lines.append("  (none found)")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]

    if not args:
        print(
            'Usage: python app/main.py "cheap trip under 500 to Andorra"',
            file=sys.stderr,
        )
        return 1

    raw_text = " ".join(args)

    orchestrator = Orchestrator()

    intent = orchestrator.parse(raw_text)
    memory_service = MemoryService()

    preferences = memory_service.retrieve(
        raw_text
    )

    print("\nRetrieved Preferences:")

    for preference in preferences:
        print(f"- {preference}")

    constraints = TripConstraints(
        max_budget=intent.budget
    )

    builder = ItineraryBuilder(
        profile=intent.profile
    )

    optimizer = ItineraryOptimizer()
    candidates = builder.build(
        intent,
        preferences
    )

    try:
        itinerary = optimizer.optimize(
            candidates,
            constraints
        )

    except ValueError as exc:
        print(f"\nError: {exc}")
        return 1

    print(format_itinerary(itinerary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

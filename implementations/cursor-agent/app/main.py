#!/usr/bin/env python3
import sys
from pathlib import Path
import argparse

# Allow imports from project root when running as a script.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from composition.itinerary_builder import ItineraryBuilder
from models.itinerary import FastItinerary
from models.scoring import ScoredItem
from constraints.models import TripConstraints

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

def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Paseo Itinerary Generator")

    parser.add_argument(
        "--destination",
        required=True,
        help="Travel destination (e.g. Andorra)"
    )

    parser.add_argument(
        "--profile",
        default="default",
        help="Travel profile: budget | luxury | adventure | foodie | default"
    )

    parser.add_argument(
        "--budget",
        type=float,
        default=None,
        help="Max total budget for trip"
    )

    return parser.parse_args(argv)
def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    print(f"Profile: {args.profile}")
    print(f"Destination: {args.destination}")

    constraints = TripConstraints(
        max_budget=args.budget,
        max_days=args.days
    )

    builder = ItineraryBuilder(profile=args.profile)

    itinerary = builder.build(
        args.destination,
        constraints=constraints
    )

    print(format_itinerary(itinerary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

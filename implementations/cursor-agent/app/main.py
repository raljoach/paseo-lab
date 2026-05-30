#!/usr/bin/env python3
import sys
from pathlib import Path

# Allow imports from project root when running as a script.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from composition.itinerary_builder import ItineraryBuilder
from commands.parser import parse_command
from models.itinerary import FastItinerary


def format_itinerary(itinerary: FastItinerary) -> str:
    lines = [
        f"Paseo FAST Itinerary — {itinerary.destination}",
        "=" * 48,
        "",
        "Flights (F)",
        "-" * 20,
    ]

    if itinerary.flights:
        for item in itinerary.flights:
            lines.append(
                f"  • {item.airline}: {item.origin} → {item.destination} "
                f"({item.departure}–{item.arrival}) — ${item.price_usd:.0f}"
            )
    else:
        lines.append("  (none found)")

    lines.extend(["", "Activities (A)", "-" * 20])
    if itinerary.activities:
        for item in itinerary.activities:
            lines.append(
                f"  • {item.name} [{item.category}] — "
                f"{item.duration_hours:g}h — ${item.price_usd:.0f}"
            )
    else:
        lines.append("  (none found)")

    lines.extend(["", "Stays (S)", "-" * 20])
    if itinerary.stays:
        for item in itinerary.stays:
            total = item.nights * item.price_per_night_usd
            lines.append(
                f"  • {item.name} — {item.nights} night(s) @ "
                f"${item.price_per_night_usd:.0f}/night — "
                f"rating {item.rating:.1f} — est. ${total:.0f}"
            )
    else:
        lines.append("  (none found)")

    lines.extend(["", "Transportation (T)", "-" * 20])
    if itinerary.transportation:
        for item in itinerary.transportation:
            lines.append(
                f"  • {item.mode}: {item.route} — "
                f"{item.duration_minutes} min — ${item.price_usd:.0f}"
            )
    else:
        lines.append("  (none found)")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if not args:
        print('Usage: python app/main.py "Paseo Andorra"', file=sys.stderr)
        return 1

    command = " ".join(args)
    try:
        destination = parse_command(command)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    itinerary = ItineraryBuilder().build(destination)
    print(format_itinerary(itinerary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

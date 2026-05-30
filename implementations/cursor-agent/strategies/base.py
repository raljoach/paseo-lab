def normalize_destination(value: str) -> str:
    return value.strip().casefold()


def matches_destination(record: dict, destination: str) -> bool:
    record_destination = record.get("destination", "")
    return normalize_destination(str(record_destination)) == normalize_destination(
        destination
    )

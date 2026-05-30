import re
from .paseo_command import PaseoCommand

PASEO_PREFIX = re.compile(r"^\s*paseo\s+", re.IGNORECASE)


def parse_command(command: str) -> PaseoCommand:
    text = command.strip()
    if not text:
        raise ValueError("Command cannot be empty.")

    text = PASEO_PREFIX.sub("", text).strip()
    if not text:
        raise ValueError("Destination is required.")

    parts = text.split()

    # last token = profile (if exists)
    known_profiles = {"budget", "luxury", "foodie", "adventure"}

    if parts and parts[-1].lower() in known_profiles:
        profile = parts[-1].lower()
        destination = " ".join(parts[:-1])
    else:
        profile = "budget"
        destination = text

    return PaseoCommand(destination=destination, profile=profile)

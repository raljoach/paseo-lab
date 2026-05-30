import re

PASEO_PREFIX = re.compile(r"^\s*paseo\s+", re.IGNORECASE)


def parse_command(command: str) -> str:
    """
    Parse a user command such as 'Paseo Andorra' and return the destination.
    """
    text = command.strip()
    if not text:
        raise ValueError("Command cannot be empty.")

    destination = PASEO_PREFIX.sub("", text).strip()
    if not destination:
        raise ValueError("Destination is required. Example: Paseo Andorra")

    return destination

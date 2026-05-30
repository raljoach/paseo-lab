def apply_profile(weights: dict, profile: dict) -> dict:
    """
    Override base weights using profile weights.
    """
    updated = {}
    for section, base in weights.items():
        overrides = profile.get(section, {})
        updated[section] = {**base, **overrides}
    return updated
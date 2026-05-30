def apply_profile(weights: dict, profile: dict) -> dict:
    """
    Override base weights using profile weights.
    """
    updated = {}
    # print('--------------------------------')
    # print("Using profile-adjusted weights")
    # print(f"Initial weights: {weights}")
    # print(f"Profile overrides: {profile}")
    for section, base in weights.items():
        overrides = profile.get(section, {})
        updated[section] = {**base, **overrides}
    # print(f"Merged profile weights: {updated}")
    return updated
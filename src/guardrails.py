"""Validate user preferences before generating recommendations."""

from math import isfinite


def validate_preferences(preferences, k=5):
    """Return normalized preferences or raise a readable validation error."""
    if not isinstance(preferences, dict):
        raise ValueError("Preferences must be a dictionary.")

    cleaned = {}

    for feature in ("genre", "mood"):
        value = preferences.get(feature)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{feature} must be a nonempty string.")
        cleaned[feature] = value.strip().lower()

    energy = preferences.get("energy")
    if isinstance(energy, bool) or not isinstance(energy, (int, float)):
        raise ValueError("energy must be a number between 0 and 1.")

    if not isfinite(energy) or not 0 <= energy <= 1:
        raise ValueError("energy must be a finite number between 0 and 1.")

    cleaned["energy"] = float(energy)

    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer.")

    return cleaned

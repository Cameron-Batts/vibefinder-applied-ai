"""Validate user preferences before generating recommendations."""

from math import isfinite

from src.errors import ValidationError


def validate_preferences(preferences, k=5):
    """Return normalized preferences or raise a readable validation error."""
    if not isinstance(preferences, dict):
        raise ValidationError("Preferences must be a dictionary.")

    cleaned = {}

    for feature in ("genre", "mood"):
        value = preferences.get(feature)
        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"{feature} must be a nonempty string.")
        cleaned[feature] = value.strip().lower()

    energy = preferences.get("energy")
    if isinstance(energy, bool) or not isinstance(energy, (int, float)):
        raise ValidationError("energy must be a number between 0 and 1.")

    if not isfinite(energy) or not 0 <= energy <= 1:
        raise ValidationError("energy must be a finite number between 0 and 1.")

    cleaned["energy"] = float(energy)

    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValidationError("k must be a positive integer.")

    return cleaned


def validate_catalog(songs):
    """Raise a readable error if the song catalog cannot be scored safely."""
    if not songs:
        raise ValidationError("The song catalog is empty.")

    ids = set()
    for song in songs:
        if not isinstance(song, dict):
            raise ValidationError("Each catalog song must be a dictionary.")

        for field in ("title", "genre", "mood"):
            value = song.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValidationError(f"Catalog song has invalid {field}.")

        song_id = song.get("id")
        if type(song_id) is not int or song_id in ids:
            raise ValidationError("Catalog IDs must be unique integers.")
        ids.add(song_id)

        energy = song.get("energy")
        if (
            isinstance(energy, bool)
            or not isinstance(energy, (int, float))
            or not isfinite(energy)
            or not 0 <= energy <= 1
        ):
            raise ValidationError("Catalog energy must be between 0 and 1.")

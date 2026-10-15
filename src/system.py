"""Coordinate validation, recommendation, and runtime reliability checks."""

import logging
from math import isfinite

from src.guardrails import validate_preferences
from src.recommender import recommend_songs

logger = logging.getLogger(__name__)


def run_request(preferences, songs, k=5):
    """Return checked recommendations or a structured error response."""
    try:
        cleaned = validate_preferences(preferences, k)

        if not songs:
            raise ValueError("The song catalog is empty.")

        ids = set()
        for song in songs:
            for field in ("title", "genre", "mood"):
                value = song.get(field)
                if not isinstance(value, str) or not value.strip():
                    raise ValueError(f"Catalog song has invalid {field}.")

            song_id = song.get("id")
            if type(song_id) is not int or song_id in ids:
                raise ValueError("Catalog IDs must be unique integers.")
            ids.add(song_id)

            energy = song.get("energy")
            if (
                isinstance(energy, bool)
                or not isinstance(energy, (int, float))
                or not isfinite(energy)
                or not 0 <= energy <= 1
            ):
                raise ValueError("Catalog energy must be between 0 and 1.")

        warnings = []
        for feature in ("genre", "mood"):
            available = {song[feature].strip().lower() for song in songs}
            if cleaned[feature] not in available:
                warnings.append(
                    f"No catalog {feature} matches '{cleaned[feature]}'."
                )

        recommendations = recommend_songs(cleaned, songs, k)
        previous_score = float("inf")
        returned_ids = set()

        if len(recommendations) != min(k, len(songs)):
            raise RuntimeError("Unexpected recommendation count.")

        for song, score, explanation in recommendations:
            expected = (
                2.0 * (song["genre"].strip().lower() == cleaned["genre"])
                + 1.0 * (song["mood"].strip().lower() == cleaned["mood"])
                + 1.0 - abs(song["energy"] - cleaned["energy"])
            )
            if (
                song not in songs
                or song["id"] in returned_ids
                or not isfinite(score)
                or abs(score - expected) > 1e-9
                or score > previous_score
                or not isinstance(explanation, str)
                or not explanation.strip()
            ):
                raise RuntimeError("Recommendation verification failed.")
            returned_ids.add(song["id"])
            previous_score = score

        status = "needs_review" if warnings else "ok"
        logger.info("Request status=%s count=%d", status, len(recommendations))
        return {
            "status": status,
            "warnings": warnings,
            "verification": "passed",
            "recommendations": recommendations,
        }

    except (ValueError, TypeError, KeyError) as error:
        logger.warning("Request blocked: %s", error)
        return {
            "status": "blocked",
            "error": str(error),
            "recommendations": [],
        }
    except RuntimeError as error:
        logger.error("Output withheld: %s", error)
        return {
            "status": "verification_failed",
            "error": str(error),
            "recommendations": [],
        }

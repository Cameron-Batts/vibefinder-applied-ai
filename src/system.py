"""Coordinate validation, recommendation, and runtime reliability checks."""

import logging
from math import isfinite

from src import recommender as scoring
from src.errors import ValidationError, VerificationError
from src.guardrails import validate_catalog, validate_preferences
from src.recommender import recommend_songs

logger = logging.getLogger(__name__)


def check_coverage(cleaned, songs):
    """Return warnings for requested labels that no catalog song has."""
    warnings = []
    for feature in ("genre", "mood"):
        available = {song[feature].strip().lower() for song in songs}
        if cleaned[feature] not in available:
            warnings.append(f"No catalog {feature} matches '{cleaned[feature]}'.")
    return warnings


def expected_score(cleaned, song):
    """Recompute a song's score from the shared scoring weights."""
    return (
        scoring.GENRE_WEIGHT * (song["genre"].strip().lower() == cleaned["genre"])
        + scoring.MOOD_WEIGHT * (song["mood"].strip().lower() == cleaned["mood"])
        + scoring.ENERGY_WEIGHT * (1.0 - abs(song["energy"] - cleaned["energy"]))
    )


def verify_recommendations(recommendations, cleaned, songs, k):
    """Raise VerificationError if the ranked output is inconsistent."""
    if len(recommendations) != min(k, len(songs)):
        raise VerificationError("Unexpected recommendation count.")

    previous_score = float("inf")
    returned_ids = set()

    for song, score, explanation in recommendations:
        if (
            song not in songs
            or song["id"] in returned_ids
            or not isfinite(score)
            or abs(score - expected_score(cleaned, song)) > 1e-9
            or score > previous_score
            or not isinstance(explanation, str)
            or not explanation.strip()
        ):
            raise VerificationError("Recommendation verification failed.")
        returned_ids.add(song["id"])
        previous_score = score


def run_request(preferences, songs, k=5, catalog_checked=False):
    """Return checked recommendations or a structured error response.

    Only ValidationError and VerificationError are turned into statuses.
    Any other exception is a bug and is allowed to surface. Pass
    catalog_checked=True when the catalog was already validated once.
    """
    try:
        cleaned = validate_preferences(preferences, k)
        if not catalog_checked:
            validate_catalog(songs)

        warnings = check_coverage(cleaned, songs)
        recommendations = recommend_songs(cleaned, songs, k)
        verify_recommendations(recommendations, cleaned, songs, k)

        status = "needs_review" if warnings else "ok"
        logger.info("Request status=%s count=%d", status, len(recommendations))
        return {
            "status": status,
            "warnings": warnings,
            "verification": "passed",
            "recommendations": recommendations,
        }

    except ValidationError as error:
        logger.warning("Request blocked: %s", error)
        return {
            "status": "blocked",
            "error": str(error),
            "recommendations": [],
        }
    except VerificationError as error:
        logger.error("Output withheld: %s", error)
        return {
            "status": "verification_failed",
            "error": str(error),
            "recommendations": [],
        }

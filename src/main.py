"""Run VibeFinder with integrated guardrails and result verification."""

import argparse
import csv
import logging
from pathlib import Path

from src.errors import ValidationError
from src.guardrails import validate_catalog
from src.recommender import load_songs
from src.system import run_request


def display_result(preferences, result):
    """Print the request, reliability status, and explained recommendations."""
    print(f"\nInput: {preferences}")
    print(f"Status: {result['status']}")
    if "verification" in result:
        print(f"Technical checks: {result['verification']}")
    for warning in result.get("warnings", []):
        print(f"WARNING: {warning}")
    if result["status"] == "needs_review":
        print("Review these partial matches or revise your preferences.")
    if "error" in result:
        print(f"ERROR: {result['error']}")

    for rank, (song, score, explanation) in enumerate(
        result["recommendations"], 1
    ):
        print(f"{rank}. {song['title']} | Score: {score:.2f}")
        print(f"   Because: {explanation}")


def print_guide(songs):
    """Show the energy scale, plus the genres and moods the catalog supports."""
    print("\nEnergy scale (0 = calm, 1 = intense). Bars show each song:")
    for song in sorted(songs, key=lambda item: item["energy"]):
        bar = "#" * round(song["energy"] * 20)
        print(f"  {song['energy']:.2f} {bar:<20} {song['title']}")
    genres = sorted({song["genre"] for song in songs})
    moods = sorted({song["mood"] for song in songs})
    print("\nValid genres: " + ", ".join(genres))
    print("Valid moods: " + ", ".join(moods))
    print("\nExample: python -m src.main --genre pop --mood happy --energy 0.8")


def main():
    """Process CLI requests through the validated recommendation pipeline."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--genre", default="pop")
    parser.add_argument("--mood", default="happy")
    parser.add_argument(
        "--energy", type=float, default=0.8,
        help="0 (calm) to 1 (intense). Run with --guide to see the scale.",
    )
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--demo", action="store_true")
    parser.add_argument(
        "--guide", action="store_true",
        help="Show the energy scale and valid genres and moods, then exit.",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
    try:
        songs = load_songs(path)
        validate_catalog(songs)
    except (OSError, ValueError, KeyError, csv.Error, ValidationError) as error:
        logging.error("Catalog could not be loaded: %s", error)
        print("ERROR: Check data/songs.csv before requesting recommendations.")
        return 2

    print(f"Loaded songs: {len(songs)}")

    if args.guide:
        print_guide(songs)
        return 0

    if args.demo:
        profiles = [
            {"genre": "pop", "mood": "happy", "energy": 0.8},
            {"genre": "lofi", "mood": "chill", "energy": 0.35},
            {"genre": "rock", "mood": "intense", "energy": 0.9},
            {"genre": "opera", "mood": "dramatic", "energy": 0.5},
            {"genre": "pop", "mood": "happy", "energy": 1.5},
        ]
        for preferences in profiles:
            result = run_request(preferences, songs, args.k, catalog_checked=True)
            display_result(preferences, result)
        return 0

    preferences = {
        "genre": args.genre,
        "mood": args.mood,
        "energy": args.energy,
    }
    result = run_request(preferences, songs, args.k, catalog_checked=True)
    display_result(preferences, result)
    return 0 if result["status"] in ("ok", "needs_review") else 2


if __name__ == "__main__":
    raise SystemExit(main())

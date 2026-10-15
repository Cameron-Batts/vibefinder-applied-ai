"""Run VibeFinder with integrated guardrails and result verification."""

import argparse
import csv
import logging
from pathlib import Path

from src.recommender import load_songs
from src.system import run_request


def display_result(preferences, result):
    """Print the request, reliability status, and explained recommendations."""
    print(f"\nInput: {preferences}")
    print(f"Status: {result['status']}")
    if "verification" in result:
        print(f"Output verification: {result['verification']}")
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


def main():
    """Process CLI requests through the validated recommendation pipeline."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--genre", default="pop")
    parser.add_argument("--mood", default="happy")
    parser.add_argument("--energy", type=float, default=0.8)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    path = Path(__file__).resolve().parents[1] / "data" / "songs.csv"
    try:
        songs = load_songs(path)
    except (OSError, ValueError, KeyError, csv.Error) as error:
        logging.error("Catalog could not be loaded: %s", error)
        print("ERROR: Check data/songs.csv before requesting recommendations.")
        return 2

    print(f"Loaded songs: {len(songs)}")

    if args.demo:
        profiles = [
            {"genre": "pop", "mood": "happy", "energy": 0.8},
            {"genre": "lofi", "mood": "chill", "energy": 0.35},
            {"genre": "rock", "mood": "intense", "energy": 0.9},
            {"genre": "opera", "mood": "dramatic", "energy": 0.5},
            {"genre": "pop", "mood": "happy", "energy": 1.5},
        ]
        for preferences in profiles:
            result = run_request(preferences, songs, args.k)
            display_result(preferences, result)
        return 0

    preferences = {
        "genre": args.genre,
        "mood": args.mood,
        "energy": args.energy,
    }
    result = run_request(preferences, songs, args.k)
    display_result(preferences, result)
    return 0 if result["status"] in ("ok", "needs_review") else 2


if __name__ == "__main__":
    raise SystemExit(main())

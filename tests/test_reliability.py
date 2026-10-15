"""Test validation, coverage warnings, and runtime result verification."""

from pathlib import Path
import subprocess
import sys

import pytest

from src.guardrails import validate_preferences
from src.recommender import load_songs
from src.system import run_request

ROOT = Path(__file__).resolve().parents[1]
PREFS = {"genre": "pop", "mood": "happy", "energy": 0.8}


@pytest.fixture
def songs():
    return load_songs(ROOT / "data" / "songs.csv")


def test_normalizes_preferences():
    result = validate_preferences(
        {"genre": " Pop ", "mood": "HAPPY", "energy": 0.8}
    )
    assert result == PREFS


@pytest.mark.parametrize("energy", [
    -0.1, 1.1, float("nan"), float("inf"), "high", True, None,
])
def test_invalid_energy_is_blocked(songs, energy):
    result = run_request(dict(PREFS, energy=energy), songs)
    assert result["status"] == "blocked"
    assert result["recommendations"] == []


@pytest.mark.parametrize("k", [0, -1, 1.5, True])
def test_invalid_k_is_blocked(songs, k):
    assert run_request(PREFS, songs, k)["status"] == "blocked"


@pytest.mark.parametrize("preferences", [
    {}, None, {"genre": "", "mood": "happy", "energy": 0.8},
])
def test_missing_preferences_are_blocked(songs, preferences):
    assert run_request(preferences, songs)["status"] == "blocked"


def test_valid_request_is_verified(songs):
    result = run_request(PREFS, songs)
    assert result["status"] == "ok"
    assert result["verification"] == "passed"
    assert len(result["recommendations"]) == 5
    song, score, explanation = result["recommendations"][0]
    assert song["title"] == "Sunrise City"
    assert score == pytest.approx(3.98)
    assert "genre match" in explanation


def test_unknown_labels_require_review(songs):
    result = run_request(
        {"genre": "opera", "mood": "dramatic", "energy": 0.5},
        songs,
    )
    assert result["status"] == "needs_review"
    assert len(result["warnings"]) == 2
    assert result["verification"] == "passed"


def test_empty_catalog_is_blocked():
    assert run_request(PREFS, [])["status"] == "blocked"


def test_bad_catalog_energy_is_blocked(songs):
    songs[0]["energy"] = 2.0
    assert run_request(PREFS, songs)["status"] == "blocked"


def test_duplicate_catalog_ids_are_blocked(songs):
    songs[1]["id"] = songs[0]["id"]
    assert run_request(PREFS, songs)["status"] == "blocked"


def test_wrong_score_is_withheld(songs, monkeypatch):
    def faulty_recommender(preferences, catalog, k):
        return [(catalog[0], 99.0, "Incorrect score")]

    monkeypatch.setattr("src.system.recommend_songs", faulty_recommender)
    result = run_request(PREFS, songs, k=1)
    assert result["status"] == "verification_failed"
    assert result["recommendations"] == []


def test_large_k_returns_available_songs(songs):
    result = run_request(PREFS, songs, k=100)
    assert result["status"] == "ok"
    assert len(result["recommendations"]) == len(songs)


def test_invalid_cli_request_exits_cleanly():
    result = subprocess.run(
        [sys.executable, "-m", "src.main", "--energy", "1.5"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert "Status: blocked" in result.stdout
    assert "Traceback" not in result.stderr

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Single source of truth for the scoring rule. The runtime verifier in
# src/system.py reads these same constants.
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.0

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """Recommend Song objects using the shared scoring functions."""

    def __init__(self, songs: List[Song]):
        """Store the song catalog."""
        self.songs = songs

    def _preferences(self, user: UserProfile) -> Dict:
        """Convert a user profile to scoring preferences."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return Song objects ranked by their relevance scores."""
        preferences = self._preferences(user)
        return sorted(
            self.songs,
            key=lambda song: score_song(preferences, vars(song))[0],
            reverse=True,
        )[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain the score using the shared scoring rule."""
        _, reasons = score_song(self._preferences(user), vars(song))
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load song dictionaries and convert numerical CSV values."""
    import csv

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            row["id"] = int(row["id"])
            for feature in (
                "energy", "tempo_bpm", "valence",
                "danceability", "acousticness"
            ):
                row[feature] = float(row[feature])
            songs.append(row)

    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song by genre, mood, and energy, with reasons."""
    score = 0.0
    reasons = []

    if song["genre"].strip().lower() == user_prefs["genre"].strip().lower():
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT:.2f})")

    if song["mood"].strip().lower() == user_prefs["mood"].strip().lower():
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT:.2f})")

    energy_gap = abs(song["energy"] - user_prefs["energy"])
    energy_points = ENERGY_WEIGHT * (1.0 - energy_gap)
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top k songs ranked by score, with explanations."""
    recommendations = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        recommendations.append((song, score, explanation))

    return sorted(
        recommendations,
        key=lambda item: item[1],
        reverse=True
    )[:k]

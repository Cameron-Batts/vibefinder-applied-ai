"""Streamlit front end for VibeFinder.

Uses the same checked pipeline as the command line, so every request is
validated, scored, and verified before results are shown.

Run with: streamlit run app.py
"""

from pathlib import Path

import streamlit as st

from src.guardrails import validate_catalog
from src.recommender import load_songs
from src.system import run_request

CSV_PATH = Path(__file__).resolve().parent / "data" / "songs.csv"
OTHER = "Other (type your own)"


@st.cache_data
def get_songs():
    """Load and validate the catalog once."""
    songs = load_songs(CSV_PATH)
    validate_catalog(songs)
    return songs


def pick(label, options, key):
    """Choose from the catalog's labels, or type one that may not exist."""
    choice = st.selectbox(label, options + [OTHER], key=key)
    if choice == OTHER:
        return st.text_input(f"Type a {label.lower()}", key=f"{key}_text")
    return choice


def show_status(result):
    """Show the request status the same way the command line does."""
    status = result["status"]
    if status == "ok":
        st.success("Status: ok. Technical checks passed.")
    elif status == "needs_review":
        st.warning(
            "Status: needs_review. Technical checks passed, but review "
            "these partial matches or change your preferences."
        )
        for warning in result["warnings"]:
            st.warning(warning)
    else:
        st.error(f"Status: {status}. {result['error']}")


st.set_page_config(page_title="VibeFinder", page_icon="🎵")
st.title("VibeFinder")
st.caption("A music recommender that checks its own work.")

songs = get_songs()
genres = sorted({song["genre"] for song in songs})
moods = sorted({song["mood"] for song in songs})

left, right = st.columns(2)
with left:
    genre = pick("Genre", genres, "genre")
with right:
    mood = pick("Mood", moods, "mood")

energy = st.slider("Energy (0 = calm, 1 = intense)", 0.0, 1.0, 0.8, 0.01)
count = st.slider("Number of songs", 1, 10, 5)
test_guardrail = st.checkbox("Test the guardrail: send an invalid energy of 1.5")
if test_guardrail:
    energy = 1.5

with st.expander("See the energy scale for every song"):
    scale = [
        {"Song": song["title"], "Energy": song["energy"]}
        for song in sorted(songs, key=lambda item: item["energy"])
    ]
    st.dataframe(
        scale,
        hide_index=True,
        column_config={
            "Energy": st.column_config.ProgressColumn(
                "Energy", min_value=0.0, max_value=1.0, format="%.2f"
            )
        },
    )

preferences = {"genre": genre, "mood": mood, "energy": energy}
result = run_request(preferences, songs, count, catalog_checked=True)

st.subheader("Recommendations")
show_status(result)

if result["recommendations"]:
    rows = [
        {
            "Rank": rank,
            "Title": song["title"],
            "Artist": song.get("artist", ""),
            "Score": round(score, 2),
            "Why": explanation,
        }
        for rank, (song, score, explanation) in enumerate(
            result["recommendations"], 1
        )
    ]
    st.dataframe(rows, hide_index=True)

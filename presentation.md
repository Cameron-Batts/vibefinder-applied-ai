# VibeFinder Applied AI: Presentation Guide

Target length: 6 minutes. Rehearse with the live commands and adjust the wording to match your experience.

## 0:00–0:45 — Problem and Original Project

Show the README.

My original Module 3 project recommended songs using genre, mood, and energy. It worked for the sample profiles, but returning a ranked list did not tell the user whether the request was valid or the catalog could actually meet it.

This extension adds a reliability system around that recommender. The goal is to show useful results while making errors and limitations visible.

## 0:45–1:30 — Architecture

Show the diagram in the README.

The CLI loads the catalog and passes requests into the system pipeline. The pipeline validates preferences and catalog data, checks whether the requested categories exist, generates recommendations, and checks the returned results.

Invalid input is blocked. Results that fail technical checks are withheld. Missing categories generate warnings so the user can review partial matches or change the request.

## 1:30–2:15 — Normal Recommendation Demo

Run:
python -m src.main --genre pop --mood happy --energy 0.8 --k 3

Explain Sunrise City's score:
- Two points for pop.
- One point for happy.
- Energy 0.82 is 0.02 away from the target.
- Energy similarity contributes 0.98.
- The total is 3.98.

The technical-check label means the checked scoring and structural conditions passed. It does not mean the listener will enjoy the song.

## 2:15–3:00 — Missing Coverage Demo

Run:
python -m src.main --genre opera --mood dramatic --energy 0.5 --k 3

Point out needs_review and both warnings.

The catalog contains neither opera nor dramatic labels. The system can still rank songs by energy, but it identifies them as partial matches. The user can revise the request; review is advisory rather than an enforced approval step.

## 3:00–3:45 — Invalid Input Demo

Run:
python -m src.main --genre pop --mood happy --energy 1.5

Point out blocked status and the error.

Energy must be between zero and one. This request produces no recommendations and returns exit code 2. Rejecting the input prevents misleading scores rather than trying to guess what the user meant.

## 3:45–4:45 — Reliability Testing

Run:
python -m pytest -q

Show tests/test_reliability.py, especially test_wrong_score_is_withheld.

All 25 tests passed in the recorded run. They cover invalid preferences, catalog problems, coverage warnings, valid recommendations, and CLI behavior.

One test deliberately substitutes a score of 99.0. The verifier detects that the math is wrong and withholds the result. This tests the failure path rather than only successful examples.

Passing tests demonstrates specific checked behavior, not complete correctness.

## 4:45–5:30 — Limitations and Responsible Design

Show model_card.md.

The catalog has only 18 songs, and genre-heavy scoring can create filter bubbles. Exact labels do not recognize related genres. A technically valid recommendation can still be a poor musical match.

The current verifier does not prove that the returned subset contains the true best songs across the entire catalog. It also checks that explanations are nonempty rather than verifying every explanation claim.

No listening history or API credentials are needed.

## 5:30–6:00 — AI Collaboration and Next Steps

AI helped draft the code, tests, diagram, and documentation. I ran the commands locally and shared actual results during development.

An accepted suggestion was to integrate reliability checks into the application pipeline. An earlier label, Output verification, was revised to Technical checks to avoid overstating what was established.

Next steps are checking global top-k correctness, verifying explanation contributions, and collecting listener feedback to evaluate usefulness.

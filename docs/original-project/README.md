# VibeFinder: Music Recommender Simulation

## Project Summary

VibeFinder is a CLI-first Python recommender. It compares 18 songs with a user's preferred genre, mood, and energy, then returns five recommendations with explanations. It uses fixed rules rather than a trained machine-learning model.

## How The System Works

Collaborative filtering uses patterns in other users' behavior, such as listening histories, likes, skips, and playlists. Content-based filtering compares song attributes with a user's preferences. This project uses content-based filtering without listening histories or comparisons between users.

Background sources:
- https://support.google.com/youtube/answer/16089387?hl=en
- https://research.google/pubs/content-based-related-video-recommendations/

### Features and profiles

Song stores id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. The current scoring rule uses genre, mood, and energy.

UserProfile stores favorite_genre, favorite_mood, target_energy, and likes_acoustic. Acoustic preference is unused in this version. The CLI uses dictionaries containing genre, mood, and energy.

The catalog contains the original 10 songs plus 8 AI-generated fictional additions. The added values are illustrative rather than measurements of actual recordings.

### Algorithm Recipe

- Add 2 points for a genre match.
- Add 1 point for a mood match.
- Add energy similarity: 1 - abs(song_energy - target_energy).
- Sort every song by total score, highest first.
- Return the top five with explanations.

Sunrise City scores 2 + 1 + 0.98 = 3.98 for the pop/happy/0.8 profile. Closer energy earns more points. Valid energy values range from zero to one, producing total scores from zero to four.

Scoring judges one song; ranking orders all scored songs. sorted() creates a new list, while .sort() changes a list in place and returns None. Exact score ties retain catalog order.

Data flow: CSV and user preferences → score each song → rank songs → top five with reasons.

The larger genre weight may favor familiar genres over better mood matches, creating a filter bubble.

## Getting Started

Run these commands from the project folder:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.main
```

## Testing

Run: python -m pytest -q

Both starter tests passed. They check a preferred song's ranking and a nonempty explanation.

## Experiments You Tried

Genre weight was halved from 2 to 1 and energy weight doubled from 1 to 2. Mood stayed at 1. Rooftop Lights rose from fourth to second for pop. Gym Hero rose from third to second for rock. The lofi ordering stayed unchanged.

These are ranking changes; listener feedback would be needed to establish better accuracy. Baseline code was restored afterward.

Two edge cases tested sad high-energy pop and unavailable opera/dramatic labels. The opera profile received energy-only matches because neither category was present.

## Limitations and Risks

The catalog is small and unevenly distributed. Exact matching treats pop and indie pop as different genres. Genre weight can put sad pop above happy indie pop for a happy-pop profile. Lyrics, language, listening history, and changing taste are ignored. Scores are relevance points rather than probabilities of enjoyment.

## Reflection

See model_card.md for evaluation and personal reflection. The personal reflection is included in the model card.


## Sample Recommendation Output

Baseline results for three user profiles.

```text
Loaded songs: 18

Profile: High-Energy Pop
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}

1. Sunrise City | Score: 3.98
   Because: genre match (+2.00); mood match (+1.00); energy similarity (+0.98)
2. Neon Heartbreak | Score: 2.94
   Because: genre match (+2.00); energy similarity (+0.94)
3. Gym Hero | Score: 2.87
   Because: genre match (+2.00); energy similarity (+0.87)
4. Rooftop Lights | Score: 1.96
   Because: mood match (+1.00); energy similarity (+0.96)
5. Midnight Verse | Score: 0.99
   Because: energy similarity (+0.99)

Profile: Chill Lofi
Preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}

1. Library Rain | Score: 4.00
   Because: genre match (+2.00); mood match (+1.00); energy similarity (+1.00)
2. Midnight Coding | Score: 3.93
   Because: genre match (+2.00); mood match (+1.00); energy similarity (+0.93)
3. Focus Flow | Score: 2.95
   Because: genre match (+2.00); energy similarity (+0.95)
4. Spacewalk Thoughts | Score: 1.93
   Because: mood match (+1.00); energy similarity (+0.93)
5. Coffee Shop Stories | Score: 0.98
   Because: energy similarity (+0.98)

Profile: Deep Intense Rock
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}

1. Storm Runner | Score: 3.99
   Because: genre match (+2.00); mood match (+1.00); energy similarity (+0.99)
2. Electric Grief | Score: 2.96
   Because: genre match (+2.00); energy similarity (+0.96)
3. Gym Hero | Score: 1.97
   Because: mood match (+1.00); energy similarity (+0.97)
4. Brass Parade | Score: 0.98
   Because: energy similarity (+0.98)
5. Neon Heartbreak | Score: 0.96
   Because: energy similarity (+0.96)
```

## Weight Experiment Results

Genre weight changed from 2 to 1; energy weight changed from 1 to 2. Mood stayed at 1.

```text
Loaded songs: 18

Profile: High-Energy Pop
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}

1. Sunrise City | Score: 3.96
   Because: genre match (+1.00); mood match (+1.00); energy similarity (+1.96)
2. Rooftop Lights | Score: 2.92
   Because: mood match (+1.00); energy similarity (+1.92)
3. Neon Heartbreak | Score: 2.88
   Because: genre match (+1.00); energy similarity (+1.88)
4. Gym Hero | Score: 2.74
   Because: genre match (+1.00); energy similarity (+1.74)
5. Midnight Verse | Score: 1.98
   Because: energy similarity (+1.98)

Profile: Chill Lofi
Preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}

1. Library Rain | Score: 4.00
   Because: genre match (+1.00); mood match (+1.00); energy similarity (+2.00)
2. Midnight Coding | Score: 3.86
   Because: genre match (+1.00); mood match (+1.00); energy similarity (+1.86)
3. Focus Flow | Score: 2.90
   Because: genre match (+1.00); energy similarity (+1.90)
4. Spacewalk Thoughts | Score: 2.86
   Because: mood match (+1.00); energy similarity (+1.86)
5. Coffee Shop Stories | Score: 1.96
   Because: energy similarity (+1.96)

Profile: Deep Intense Rock
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}

1. Storm Runner | Score: 3.98
   Because: genre match (+1.00); mood match (+1.00); energy similarity (+1.98)
2. Gym Hero | Score: 2.94
   Because: mood match (+1.00); energy similarity (+1.94)
3. Electric Grief | Score: 2.92
   Because: genre match (+1.00); energy similarity (+1.92)
4. Brass Parade | Score: 1.96
   Because: energy similarity (+1.96)
5. Neon Heartbreak | Score: 1.92
   Because: energy similarity (+1.92)
```

## Edge Case Results

```text

Profile: Sad High-Energy Pop
Preferences: {'genre': 'pop', 'mood': 'sad', 'energy': 0.95}

1. Neon Heartbreak | Score: 3.91
   Because: genre match (+2.00); mood match (+1.00); energy similarity (+0.91)
2. Gym Hero | Score: 2.98
   Because: genre match (+2.00); energy similarity (+0.98)
3. Sunrise City | Score: 2.87
   Because: genre match (+2.00); energy similarity (+0.87)
4. Electric Grief | Score: 1.99
   Because: mood match (+1.00); energy similarity (+0.99)
5. Storm Runner | Score: 0.96
   Because: energy similarity (+0.96)

Profile: Unknown Genre and Mood
Preferences: {'genre': 'opera', 'mood': 'dramatic', 'energy': 0.5}

1. Island Afternoon | Score: 0.98
   Because: energy similarity (+0.98)
2. Porchlight Home | Score: 0.95
   Because: energy similarity (+0.95)
3. Midnight Coding | Score: 0.92
   Because: energy similarity (+0.92)
4. Focus Flow | Score: 0.90
   Because: energy similarity (+0.90)
5. Coffee Shop Stories | Score: 0.87
   Because: energy similarity (+0.87)
```

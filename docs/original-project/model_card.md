# Model Card: VibeFinder 1.0

## 1. Model Name

VibeFinder 1.0.

## 2. Intended Use

VibeFinder suggests songs based on a preferred genre, mood, and energy level. Its goal is to demonstrate how song features become scores and ranked recommendations.

It is designed for classroom exploration. It assumes one genre, one mood, and one energy target describe the user's current preferences.

It is not intended for production music recommendations or reliable predictions of listener enjoyment. A score is not a probability.

## 3. How the Model Works

A matching genre earns two points. A matching mood earns one point. Energy earns up to one point, with closer matches receiving more points.

The program scores every song, sorts the scores from highest to lowest, and returns five songs with explanations.

The starter placeholders were replaced with CSV loading, scoring, ranking, and explanations. The dictionary functions and Recommender class share the same scoring rule.

## 4. Data

The catalog contains 18 songs: the original 10 and eight AI-generated fictional additions.

Each song has an ID, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. Only genre, mood, and energy currently affect scores.

The additions include country, ska, classical, reggae, afrobeat, and hip hop. Their values are illustrative rather than measured from recordings.

The dataset has no listening histories, user ratings, or ground truth showing which songs a listener actually enjoys.

## 5. Strengths

The three main profiles produce different winners. Sunrise City leads High-Energy Pop with 3.98. Library Rain leads Chill Lofi with 4.00. Storm Runner leads Deep Intense Rock with 3.99.

These winners match the profiles' genre and mood and closely match their energy targets. The explanations make each score easy to inspect.

This demonstrates consistency with the scoring recipe. It does not establish real-world recommendation accuracy.

## 6. Limitations and Bias

Genre has more weight than mood, so sad Neon Heartbreak outranks happy Rooftop Lights for the happy-pop profile. Exact matching also treats pop and indie pop as unrelated genres. The small, uneven catalog gives some genres more choices than others and can reinforce a filter bubble. Users requesting unavailable labels, such as opera and dramatic, receive energy-only matches. The system ignores lyrics, language, listening history, and changes in a person's taste.

## 7. Evaluation

### Profiles tested

- High-Energy Pop: pop, happy, energy 0.80.
- Chill Lofi: lofi, chill, energy 0.35.
- Deep Intense Rock: rock, intense, energy 0.90.
- Sad High-Energy Pop: pop, sad, energy 0.95.
- Unknown Genre and Mood: opera, dramatic, energy 0.50.

Actual top-five output is saved in README.md under Sample Recommendation Output, Weight Experiment Results, and Edge Case Results.

### Comparing the three main profiles

Pop versus lofi: Sunrise City leads pop, while Library Rain leads lofi. The lofi profile rewards lower energy and chill music rather than happy pop.

Pop versus rock: Storm Runner leads rock because it matches rock and intense with energy close to 0.90. Gym Hero appears in both lists because its genre helps it for pop, while its mood helps it for rock.

Lofi versus rock: Their baseline top-five lists have no songs in common. Their preferred genres, moods, and energy levels differ substantially.

### Explaining a winning score

Sunrise City earns two points for pop, one for happy, and 0.98 for energy similarity. Its energy is 0.82 against a target of 0.80, producing a total of 3.98.

### Weight experiment

Genre weight was halved from two to one, and energy weight was doubled from one to two. Mood stayed at one.

Rooftop Lights rose from fourth to second for pop because its happy mood and close energy became more competitive with exact genre matches. Gym Hero rose from third to second for rock, overtaking Electric Grief. The lofi order stayed unchanged.

The experiment changed rankings but did not establish better accuracy. That would require listener feedback. The baseline scoring code was restored afterward.

### Edge cases

Sad High-Energy Pop ranks Neon Heartbreak first at 3.91. Sadness and high energy can coexist, so these preferences are not inherently contradictory.

The opera/dramatic profile ranks Island Afternoon first at 0.98 based only on energy. This exposes a coverage limitation rather than a successful opera recommendation.

### Tests

Both starter tests passed using python -m pytest -q. They check a preferred song's ranking in a small catalog and a nonempty explanation. They do not measure listener satisfaction or comprehensively validate the system.

## 8. Future Work

- Support multiple favorite genres and partial matches between related genres.
- Expand and balance the catalog, with explicit preferences for tempo or valence.
- Collect listener ratings to evaluate recommendation quality against ground truth.

## 9. Personal Reflection

The biggest thing I learned was how a few simple rules can turn song data into recommendations. Breaking down Sunrise City's score of 3.98 helped me understand what each feature contributes. Changing the weights also showed me how much the results depend on the choices made when designing the system. For a happy-pop profile, it makes more sense to me for happy indie pop to rank above sad pop, so seeing Rooftop Lights move up during the experiment was useful.

AI helped me build the functions and understand how the pieces connect. I ran the commands in VS Code, checked the scores and explanations, and ran the starter tests instead of assuming everything worked. I also had to separate terminal commands from example output after accidentally pasting output as commands. What surprised me was that fixed rules could produce different lists that felt personalized without learning from anyone's listening history. Next, I would add more songs and let users choose multiple genres so the recommendations would have more variety.

# Model Card: VibeFinder Applied AI

## 1. Model Name and Goal

VibeFinder Applied AI extends the Module 3 Music Recommender Simulation with an integrated reliability system.

It recommends songs using stated genre, mood, and energy preferences while checking input validity, catalog coverage, and output consistency.

## 2. Intended and Non-Intended Use

The system is intended for classroom demonstrations and portfolio review. It helps users explore explainable content-based recommendations and shows how reliability checks change application behavior.

It is not intended to predict enjoyment with calibrated confidence, infer someone's personality, or make decisions about people. It is not a production streaming service.

## 3. Data and Scoring

The catalog contains 18 songs: ten original starter rows and eight AI-generated fictional additions. The added metadata is illustrative, not measured from recordings.

Genre, mood, and energy determine scores. A genre match earns two points, mood earns one, and energy similarity earns up to one. Other metadata is retained but does not affect ranking.

There are no listener ratings or ground-truth enjoyment labels. This is a rule-based system without an LLM, RAG, fine-tuning, or autonomous planning.

## 4. Integrated Reliability Feature

The CLI sends requests through run_request in src/system.py.

Input guardrails normalize text and reject missing preferences, invalid energy, and invalid recommendation counts. Catalog checks reject invalid required fields, duplicate IDs, and invalid energy values.

Unavailable genre or mood labels produce needs_review warnings. Runtime checks verify returned count, membership, unique IDs, score math, ordering, and nonempty explanations. Failed output checks withhold recommendations.

Logging records statuses and errors in the terminal. Human review is advisory: users can inspect warnings and revise their requests, but approval is not enforced.

## 5. Evaluation and Observed Results

All 25 automated tests passed. The suite includes the two original tests and new cases covering normalization, invalid inputs, catalog problems, partial matches, score corruption, and CLI error handling.

The normal pop request returned Sunrise City first at 3.98. The lofi request returned Library Rain first at 4.00. The opera/dramatic request produced coverage warnings and energy-based partial matches. Energy 1.5 was blocked with no recommendations and CLI exit code 2.

A test deliberately substituted a score of 99.0. The system returned verification_failed and withheld recommendations.

Reproducible commands, example inputs, actual outputs, and test results appear in README.md.

## 6. Limitations and Biases

The catalog is small and unevenly distributed across genres. Genre receives more weight than mood, which can reinforce familiar genres and create filter bubbles. Exact matching treats related labels such as pop and indie pop as different categories.

A needs_review result may still be a poor musical match. Even an ok result only means requested labels exist somewhere in the catalog; it does not guarantee a song matches every requested attribute.

Technical checks do not establish listener satisfaction, completeness of testing, or the truth of every explanation. The verifier does not prove that no omitted song deserved a higher rank. It checks required scoring fields rather than every metadata field.

Direct calls to the original scoring functions bypass the pipeline. The CLI uses the guarded path. Unexpected programmer errors may still raise exceptions.

## 7. Potential Misuse and Prevention

Someone could present relevance scores as probabilities or claim that recommendations reveal personal traits. The documentation explicitly limits these interpretations and avoids confidence percentages.

Someone could also hide missing catalog coverage and present weak matches as personalized successes. The app displays needs_review warnings when requested categories are unavailable.

The system uses fictional catalog data and explicit preferences rather than collecting listening histories. If deployed publicly, it would need additional request limits, privacy controls, and broader testing.

## 8. What Surprised Me During Reliability Testing

The opera request showed that a program can return mathematically valid scores while failing to match the kind of music requested. This separates technical correctness from usefulness.

The deliberately incorrect score test also showed why checking outputs matters. Valid input alone does not guarantee a valid result.

## 9. Collaboration With AI

AI helped draft modular Python code, terminal commands, tests, the architecture diagram, and documentation. I ran the commands in VS Code and shared the actual output so the next steps could be based on observed results.

An accepted suggestion was to put validation and runtime checks in the main request pipeline. This made the reliability feature affect application behavior rather than exist only as a separate test script.

A suggestion revised during development was the output label "Output verification: passed." It was changed to "Technical checks: passed" because the broader wording could imply that musical quality or every property of the result had been verified.

The project uses AI-assisted code and documentation. Passing tests supports the specific behaviors tested; it does not replace reviewing assumptions or evaluating real listener feedback.

## 10. Future Improvements

- Check that returned songs are the true top k across the entire catalog.
- Verify explanation contributions and expand malformed-output tests.
- Add related-genre matching and listener feedback to evaluate usefulness.

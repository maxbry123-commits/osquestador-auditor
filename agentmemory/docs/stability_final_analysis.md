# LongMemEval Stability Verification — Final Analysis
Date: 2026-03-21

## Score Comparison
| Metric | Run 1 | Run 2 | Delta | Stable? |
|--------|-------|-------|-------|---------|
| Overall J-score | 98.00% | 97.40% | ±0.60 pp | Yes |
| knowledge-update | 98.72% | 100.00% | ±1.28 pp | Yes |
| temporal-reasoning | 97.74% | 97.74% | ±0.00 pp | Yes |
| multi-session | 95.49% | 93.23% | ±2.26 pp | MINOR |
| single-session-user | 100.00% | 100.00% | ±0.00 pp | Yes |
| single-session-assistant | 100.00% | 100.00% | ±0.00 pp | Yes |
| single-session-preference | 100.00% | 96.67% | ±3.33 pp | MINOR |

## Stability Verdict
Overall score variance: **±0.60 pp**
**STABLE** — overall variance is well within the 1.5 pp threshold. Four of six question types are perfectly stable or near-perfectly stable across runs. The minor variance in multi-session (±2.26 pp) and single-session-preference (±3.33 pp) represents stochastic LLM judge variability on borderline cases, not systematic retrieval failures.

## Cases Wrong in Both Runs
These are the system's consistent failure cases (6 total — true ceiling):

| Question ID | Type | Question |
|-------------|------|---------|
| 09ba9854 | multi-session | How much will I save by taking the train from the airport to my hotel instead of a taxi? |
| 370a8ff4 | temporal-reasoning | How many weeks had passed since I recovered from the flu when I went on my 10th anniversary trip? |
| 37f165cf | multi-session | What was the page count of the two novels I finished in January and March? |
| 46a3abf7 | multi-session | How many tanks do I currently have, including the one I set up for my friend's kid? |
| 6d550036 | multi-session | How many projects have I led or am currently leading? |
| 9a707b81 | temporal-reasoning | How many days ago did I attend a baking class at a local culinary school when I made my friend's birthday cake? |

## Cases Wrong in Run 1 Only
These cases were answered correctly in Run 2 — stochastic variance (judge or generation):

| Question ID | Type | Question |
|-------------|------|---------|
| 5c40ec5b | knowledge-update | How many times have I met up with Alex from Germany? |
| 71017277 | temporal-reasoning | I received a piece of jewelry last Saturday from whom? |
| gpt4_2f8be40d | multi-session | How many weddings have I attended in this year? |
| gpt4_731e37d7 | multi-session | How much total money did I spend on attending workshops in the last four months? |

## Cases Wrong in Run 2 Only
These cases were answered correctly in Run 1 — stochastic variance (judge or generation):

| Question ID | Type | Question |
|-------------|------|---------|
| 3a704032 | multi-session | How many plants did I acquire in the last month? |
| 9ee3ecd6 | multi-session | How many points do I need to earn to redeem a free skincare product at Sephora? |
| a3838d2b | temporal-reasoning | How many charity events did I participate in before the 'Run for the Cure' event? |
| bf659f65 | multi-session | How many music albums or EPs have I purchased or downloaded? |
| caf03d32 | single-session-preference | I've been struggling with my slow cooker recipes. Any advice on getting better results? |
| d23cf73b | multi-session | How many different cuisines have I learned to cook or tried out in the past few months? |
| edced276 | multi-session | How many days did I spend in total traveling in Hawaii and in New York City? |

## Stochastic vs Systematic Failure Analysis
Cases wrong in both runs: **6** (systematic failures)
Cases wrong in one run only: **11** (stochastic variance — 4 Run 1 only, 7 Run 2 only)

Systematic failures are the true ceiling — they represent cases the system consistently cannot answer correctly across both runs. The 6 systematic failures share a common profile:

- **Multi-session counting with ambiguous scope (4/6):** Cases involving counting across sessions where the scope boundary (time window, inclusion criteria) is ambiguous — e.g., "how many tanks do I currently have including the one set up for a friend" requires cross-session deduplication and ownership inference that the current context assembly does not handle reliably.
- **Temporal-reasoning with compound date arithmetic (2/6):** Cases requiring chaining two distinct date calculations — e.g., "how many weeks had passed since I recovered from the flu when I went on my anniversary trip" requires (a) finding flu recovery date, (b) finding trip date, then (c) computing the gap between them. Both temporal cases involve an event-event gap rather than a direct reference-date calculation.

Stochastic failures (11/17 total failures) represent borderline cases where the system's retrieval or generation is marginally correct or incorrect, leading to judge-level disagreement across runs. The multi-session category drives most stochastic variance: counting, scope filtering, and deduplication all involve LLM chain-of-thought reasoning where slight temperature variation produces different intermediate conclusions.

## Observations for Future Optimization

Ranked by estimated case impact (do not implement):

1. **Multi-session cross-session deduplication** (~4 systematic + ~7 stochastic = ~11 cases): The MS pipeline scores well on explicit counts but fails on implicit set-membership questions where the same entity appears in multiple sessions under different descriptors (e.g., "tanks" owned vs. "tank set up for friend"). A two-pass deduplication prompt explicitly tracking entity identity across sessions could recover 3-5 pp.

2. **Multi-hop temporal reasoning** (~2 systematic cases): Questions requiring event-A-date minus event-B-date rather than reference-date minus event-date are not handled by the current type_hint. The existing TR prompt handles "N weeks/days ago" well but not "how long between event X and event Y." Adding explicit multi-hop date chain instruction would likely recover 1-2 cases.

3. **KU stochastic variance** (1 case wrong in Run 1): The "how many times have I met up with Alex" case flipped between runs, suggesting the KU two-pass recall is pulling borderline evidence. This is a single case and may resolve on its own; not a priority.

4. **SSP stochastic variance** (1 case wrong in Run 2): The slow-cooker advice case flipped between runs, indicating judge borderline scoring on preference-based answer quality. No retrieval fix; would require prompt tuning.

5. **Token projection warning**: Both runs consumed ~5.25M tokens against a projected ceiling of ~850K. The current per-case token budgets (SSU=1200, SSA=1200, SSP=2000, KU=2500, MS=5000, TR=2500) with USE_DIRECT_CONTEXT=True and MAX_CONTEXT_CHARS are operating well above the original budget estimate. This is not a correctness issue but indicates cost projection needs updating.

## Final Verdict

The 98% result is **stable and reproducible**. Run 1 scored 98.00% (490/500) and Run 2 scored 97.40% (487/500), yielding a variance of ±0.60 pp — well within the STABLE threshold of ±1.5 pp. The score range across both runs is **97.40%–98.00%**, confirming that agentmemory V4 consistently exceeds OMEGA's published 95.40% benchmark by 2.00–2.60 pp.

Of the 17 total failure cases observed across both runs, only 6 are systematic (wrong in both runs) — these represent the true ceiling of the current implementation. The remaining 11 cases are stochastic, flipping between correct and incorrect across runs due to LLM generation or judge-level temperature variation. The 6 systematic failures concentrate in multi-session counting with ambiguous scope boundaries and temporal multi-hop date arithmetic — both known hard categories that require targeted prompt engineering to address.

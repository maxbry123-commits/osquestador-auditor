# CAMPAIGN STATE — agentmemory V4 | Operation World Record
Updated: 2026-03-23

## Current Verified Score
**Baseline (USE_DIRECT_CONTEXT=False, gpt-4o judge): 82.0% (410/500)**
File: baseline_false_gpt4o.json (created 2026-03-22)

Code state: ITER-36 (most recent)

## Targeted Test Results (2026-03-23)
Testing wrong cases from baseline on current ITER-36 code:

| Category | Baseline | Recovered | Recovery % | Remaining Wrong |
|----------|----------|-----------|------------|----------------|
| KU       | 49/78 (62.8%) | +24 | 82.8% | 5 |
| TR       | 111/133 (83.5%) | +17 | 77.3% | 5 |
| MS       | 113/133 (85.0%) | +10 | 50.0% | 10 |
| SSP      | 21/30 (70.0%) | +5 | 55.6% | 4 |
| SSU      | 66/70 (94.3%) | +1 | 25.0% | 3 |
| SSA      | 50/56 (89.3%) | +1 | 16.7% | 5 |
| **TOTAL** | 410/500 (82%) | **+58** | 64.4% | 32 |

**Projected current score: ~468/500 = 93.6%** (assuming no regressions)
**Full run triggered** — +11.6pp improvement projection exceeds 5pp threshold.

## Gap Analysis

### RETRIEVAL-MISS (dominant KU pattern)
- Old values surfacing instead of updated values (mortgage $350k→$400k, Instagram 1250→1300)
- Fact stored but not retrieved (Rachel moved to suburbs, camera collecting duration)
- Root cause: Recency sort helps but not fully fixing all cases

### INGESTION-MISS (SSU, SSA, some KU)
- SSA: Long positional lists (27th parameter, 5th bottle, 7th job) — lists too long to store fully
- SSU: Specific attribution facts not stored (who gave birthday gift, where redeemed coupon)
- KU: Count facts not stored (bereavement sessions, Emma's recipes)

### AGGREGATION-FAIL (dominant MS pattern)
- Multi-session counting with complex deduplication
- The two-step enumerate+count approach helps but misses 10 cases
- Remaining failures: gaming hours, furniture count, baking count, cuisine count, etc.

### PROMPT-FAIL (TR, some SSP)
- Date arithmetic (Sunday mass to Ash Wednesday: 30 days)
- Complex event ordering (airline sequence, concert sequence)

## Top 5 Failure Hypotheses (post-targeted-tests)

1. **MS counting aggregation (10 cases)**: Two-step enumerate+count produces wrong totals.
   - Est recovery: 5+ cases with better counting prompt
   - Pattern: All "how many X" across sessions with no deduplication signals

2. **SSA positional lists (5 cases)**: Token budget 3500 insufficient for 100-item lists
   - Est recovery: 2-3 cases with higher budget or special list extraction
   - All are "what was the Nth item in the list you gave me?"

3. **KU old-value surfacing (2 cases)**: Recency sort not always working
   - Mortgage: assistant memory of $350k outweighs user's $400k update
   - Instagram: old count surfaces over new count
   - Est recovery: 2 cases with stronger assistant-role filtering for KU

4. **SSP preference retrieval (4 cases)**: Preference context not in top retrieved
   - Questions ask for personalized recommendations but relevant preferences not surfaced
   - Est recovery: 2-3 cases with preference-priority recall

5. **TR date arithmetic (5 cases)**: Complex multi-event date calculations
   - "Sunday mass to Ash Wednesday: 30 days" — model computes wrong
   - "Baking class 21 days ago" — model can't find the correct session
   - Est recovery: 2-3 cases with improved date arithmetic prompt rules

## Assessment of Primary Gap
- Primary: AGGREGATION-FAIL (MS) — 10 cases, requires better counting
- Secondary: INGESTION-MISS (SSA) — 5 cases, structural limitation
- Tertiary: RETRIEVAL-MISS (KU, SSP, SSU) — ~9 cases

## Single Highest-Leverage Next Action
Run full 500-case evaluation to establish verified current score, then:
→ Fix MS counting aggregation (biggest single category gap)

## Reference Info
- Direct-context run (94.4%, gpt-4o): longmemeval_4o_run1.json (but uses USE_DIRECT_CONTEXT=True)
- Stability runs (97.4-98%): USE gpt-4.1 judge — NOT comparable to OMEGA methodology
- Baseline real pipeline: baseline_false_gpt4o.json (82%, gpt-4o, USE_DIRECT_CONTEXT=False)
- OMEGA target: 95.4%
- Need: 477/500 (95.4%) to beat OMEGA

## Bugs/Misconfigs Spotted
- RESULTS_FILE/PROGRESS_FILE hardcoded to v36 names (will overwrite on each run unless renamed)
- Parallel processes safe (each case uses :memory: SQLite)
- fullrun_v2.log: aborted at 141 cases (was running concurrently with other tests)

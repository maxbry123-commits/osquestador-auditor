# Baseline Report — LongMemEval Real Pipeline
**Date**: 2026-03-22
**Run**: baseline_false_gpt4o
**Config**: USE_DIRECT_CONTEXT=False, judge=gpt-4o, model=gpt-4o
**Score**: 82.0% (410/500)
**Reference**: OMEGA published = 95.4% (USE_DIRECT_CONTEXT=True)
**Prior best (False)**: 84.2% (v3, gpt-4.1 judge — gpt-4o is stricter)

---

## Per-Type Breakdown

| Type | Correct | Total | Accuracy | Wrong |
|------|---------|-------|----------|-------|
| SSU (single-session-user) | 66 | 70 | 94.29% | 4 |
| SSA (single-session-assistant) | 50 | 56 | 89.29% | 6 |
| SSP (single-session-preference) | 21 | 30 | 70.00% | 9 |
| KU (knowledge-update) | 49 | 78 | 62.82% | 29 |
| MS (multi-session) | 113 | 133 | 84.96% | 20 |
| TR (temporal-reasoning) | 111 | 133 | 83.46% | 22 |
| **TOTAL** | **410** | **500** | **82.00%** | **90** |

*Note: 4 of 90 wrong are connection errors (TR type), not retrieval failures.*

---

## Root Cause Analysis

### TYPE-I: Ingestion Noise (assistant advice stored as memories)
Assistant turns are extracted and stored as memory nodes. These contain domain vocabulary
that scores high in BM25/semantic retrieval for related questions, crowding out user facts.

**Affected types**: KU (dominant), TR (secondary), MS (secondary)

### TYPE-A: Context Assembly Noise
Even when correct user fact IS at rank-1 in `top_recall`, the `async_build_context`
token budget fills with assistant-role nodes that score almost as high.

**Evidence from wrong case analysis**:
- `830ce83f`: top_recall="Rachel just moved back to the suburbs" (CORRECT) but context = Colorado travel tips
- `gpt4_5dcc0aab`: top_recall="Adidas sneakers last month" (CORRECT) but context = shoe care advice
- `6a1eabeb`: top_recall=correct 5K time but context = interval training fitness advice
- `852ce960`: Gold=$400K mortgage, context = advice referencing old $350K value

### TYPE-R: Retrieval Miss (correct fact not retrieved at all)
Correct user memory absent from top-k results.

**Affected types**: MS (multi-session counting), SSP (niche preferences)

### TYPE-P: Temporal Positioning Error
For KU, the updated value is in a LATER session but older value ranks higher due to:
- Temporal decay signal (Gaussian centered at question date) not penalizing old enough
- Assistant messages referencing the OLD value score high (reinforce old value)

---

## Wrong Cases by Priority

### KU Failures (highest recovery potential with ITER-1)

| Case# | Question (truncated) | Diagnosis |
|-------|---------------------|-----------|
| 126 | What was the amount I was pre-approved for when I got my mortgage? | KU: old value ($350K) in assistant advice, new value ($400K) buried |
| 123 | What was my personal best time in the charity 5K run? | KU: old 27:12 in assistant fitness advice, correct 25:50 in user msg |
| 327 | How long have I been collecting vintage cameras? | KU: duration updated, old duration in assistant text |
| ...plus ~14 more KU cases | | |

### TR Failures (4 connection errors + temporal ordering)

| Case# | Question (truncated) | Diagnosis |
|-------|---------------------|-----------|
| 6 | How many days between Sunday mass at St. Mary... | TR: date arithmetic, both events not retrieved |
| 24 | Which show did I start watching first, Crown or GoT? | TR: second show session not in context |
| 29 | Which event happened first, road trip or... | TR: assistant commentary drowns event dates |

### MS Failures (counting questions, session coverage)

| Case# | Question (truncated) | Diagnosis |
|-------|---------------------|-----------|
| 62 | How many projects have I led or am currently leading? | MS: partial session coverage |
| 76 | How many hours have I spent playing games in total? | MS: assistant game recommendations crowd hours-played facts |
| 79 | How many pieces of furniture did I buy, assemble, sell or fix? | MS: scattered across sessions |
| 80 | How many times did I bake something in the past two weeks? | MS: baking events in multiple sessions |

### SSP Failures (preference retrieval)

| Case# | Question (truncated) | Diagnosis |
|-------|---------------------|-----------|
| 150 | Do I go to the gym more frequently than I did previously? | SSP: frequency comparison, assistant advice retrieved instead |
| 175 | How much time do I dedicate to coding exercises each day? | SSP: user preference buried by advice |
| 179 | How much weight have I lost since I started going to gym? | SSP: weight value in user msg, assistant health advice retrieved |

---

## Planned Improvements

See `optimization_plan.md` for full ITER-1 through ITER-5 plan.

**Priority order**:
1. **ITER-1**: Filter assistant-role memories for KU+TR (est. +8-12pp on KU, +3-5pp on TR)
2. **ITER-2**: Extend ITER-1 filter to MS+SSP (est. +3-5pp)
3. **ITER-3**: KU focus-query limit 100→300 (est. +2-3pp)
4. **ITER-4**: TR session date header injection verification
5. **ITER-5**: MS per-session FTS fallback

**Projected score after ITER-1+2**: ~85-87%
**Projected score after all 5**: ~88-92%

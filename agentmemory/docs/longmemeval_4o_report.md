# LongMemEval Evaluation — GPT-4o Judge Run 1

> Run date: 2026-03-21
> Hardware: Intel Core i3-12100F, 16 GB DDR4, Windows 11 Pro 10.0.26200
> Python: 3.12.10 | agentmemory: 4.0.0
> Evaluator model: **gpt-4o** (matching OMEGA's published evaluation methodology)
> Dataset: `LongMemEval/data/longmemeval_oracle.json` (500 cases)
> Output file: `longmemeval_4o_run1.json`

---

## Final Score Comparison

| System | Judge | J-score | Cases | Notes |
|--------|-------|---------|-------|-------|
| **agentmemory V4 (this run)** | **gpt-4o** | **94.40%** | **472/500** | |
| agentmemory V4 (prior runs) | gpt-4.1 | 97.40%–98.00% | — | 2 runs, ±0.60 pp stable |
| OMEGA (published) | gpt-4o | 95.40% | — | Published benchmark |

**Gap vs OMEGA (same judge): −1.00 pp**
**Gap vs agentmemory GPT-4.1 runs: −3.00 to −3.60 pp** — demonstrating that judge model selection has a substantial effect on measured J-score.

---

## Per-Type Accuracy

| Question Type | Correct | Total | Accuracy | OMEGA est. |
|---------------|---------|-------|----------|------------|
| knowledge-update | 78 | 78 | **100.00%** | — |
| single-session-user | 70 | 70 | **100.00%** | — |
| single-session-assistant | 55 | 56 | **98.21%** | — |
| single-session-preference | 28 | 30 | **93.33%** | — |
| temporal-reasoning | 125 | 133 | **93.98%** | — |
| multi-session | 116 | 133 | **87.22%** | — |
| **OVERALL** | **472** | **500** | **94.40%** | **95.40%** |

### Abstention cases
29/30 correct (96.67%) — system correctly abstained on unanswerable questions.

---

## Run Configuration

| Parameter | Value |
|-----------|-------|
| Evaluator model | `gpt-4o` |
| Retrieval mode | Direct context (chronological transcript with date labels) |
| Embedder | `all-mpnet-base-v2` (768-dim dense) |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| Token budgets | SSU/SSA=1200, SSP=2000, KU=2500, MS=7500, TR=5000 |
| Total tokens consumed | 5,186,133 |
| Context abstentions | 0 |

---

## Wrong Cases (28 total: 27 incorrect + 1 error/skipped)

### temporal-reasoning (8 wrong / 133)

1. **How many days had passed between the Sunday mass at St. Mary's Church and the Ash Wednesday service?**
   - Gold: 30 days (31 also acceptable)
   - System: 30 days — *judged wrong (boundary condition)*

2. **How many charity events did I participate in before the 'Run for the Cure' event?**
   - Gold: 4
   - System: 2 (missed two events)

3. **How long had I been watching stand-up comedy specials regularly when I attended the open mic night?**
   - Gold: 2 months
   - System: ~1.5 months

4. **How many days ago did I attend a baking class at a local culinary school when I made my first croissant?**
   - Gold: 21 days (22 also acceptable)
   - System: off-by-one / miscalculation

5. **How many weeks had passed since I recovered from the flu when I went on my 10th jog outdoors?**
   - Gold: 15 weeks
   - System: different value

6. **What is the order of airlines I flew with from earliest to latest before today?**
   - Gold: JetBlue, Delta, United, American Airlines
   - System: different ordering

7. **Which bike did I fix or service the past weekend?**
   - Gold: road bike
   - System: different bike

8. **I mentioned cooking something for my friend a couple of days ago. What was it?**
   - Gold: a chocolate cake
   - System: different item

---

### multi-session (17 wrong / 133)

9. **How many items of clothing do I need to pick up or return from a store?**
   - Gold: 3 | System: 2 (missed one item)

10. **How many different types of citrus fruits have I used in my cocktail recipes?**
    - Gold: 3 | System: 4 (over-counted)

11. **How many babies were born to friends and family members in the last few months?**
    - Gold: 5 | System: 4 (missed one birth)

12. **How many pieces of furniture did I buy, assemble, sell, or fix in the past few months?**
    - Gold: 4 | System: 3 (missed one piece)

13. **How many times did I bake something in the past two weeks?**
    - Gold: 4 | System: different count

14. **Which grocery store did I spend the most money at in the past month?**
    - Gold: Thrive Market | System: different store

15. **How many pieces of jewelry did I acquire in the last two months?**
    - Gold: 3 | System: different count

16. **How many days did I spend participating in faith-related activities in December?**
    - Gold: 3 days | System: different count

17. **How many kitchen items did I replace or fix?**
    - Gold: 5 (faucet, mat, toaster, …) | System: fewer items

18. **How many music albums or EPs have I purchased or downloaded?**
    - Gold: 3 | System: different count

19. **How many years in total did I spend in formal education from high school to the completion of graduate studies?**
    - Gold: 10 years | System: different total

20. **How many times did I bake egg tarts in the past two weeks?**
    - Gold: Not mentioned / insufficient information | System: hallucinated a count

21. **When did I submit my research paper on sentiment analysis?**
    - Gold: February 1st | System: different date

22. **How many points do I need to earn to redeem a free skincare product at Sephora?**
    - Gold: 100 | System: different value

23. **What is the total distance I covered in my four road trips?**
    - Gold: 3,000 miles | System: different total

24. **How much will I save by taking the train from the airport to my hotel instead of a taxi?**
    - Gold: $50 | System: different amount

25. **What was the page count of the two novels I finished in January and March?**
    - Gold: 856 | System: different total

---

### single-session-preference (2 wrong / 30)

26. **I've been struggling with my slow cooker recipes. Any advice on getting better results?**
    - Gold: tips tailored to plant-based/vegan cooking preferences
    - System: gave generic slow cooker advice without anchoring to dietary preference

27. **I'm planning my meal prep next week, any suggestions for new recipes?**
    - Gold: healthy meal prep recipes, particularly plant-based
    - System: suggestions didn't sufficiently reflect user's stated dietary preferences

---

### single-session-assistant (1 wrong / 56)

28. **I wanted to follow up on our previous conversation about fracking in the Marcellus Shale region. Which state is this located in?**
    - Gold: Pennsylvania
    - System: different answer

---

## Analysis

### Where agentmemory V4 trails OMEGA (−1.00 pp gap)

The primary weakness vs OMEGA is **multi-session** counting and aggregation tasks. 17 of 28 wrong answers are multi-session, and nearly all involve aggregation over multiple sessions (counting items, summing values, listing all instances). These fail because:

1. **Under-counting**: Retrieval returns a relevant subset but not all instances; the system counts only what it sees.
2. **Over-counting**: Semantic near-duplicates inflate counts when deduplication is not perfect.
3. **Temporal scoping**: "In the past two weeks / last few months" windows are hard to enforce when the retrieved context doesn't carry reliable date metadata per item.

The **temporal-reasoning** errors (8/133, 6.0%) are a second weak area. Most are off-by-one boundary conditions or multi-hop date arithmetic errors where the session-timestamp anchor is ambiguous.

**Knowledge-update** (100%), **single-session-user** (100%), and **single-session-assistant** (98.2%) are effectively solved.

### Judge model impact

| Judge | J-score | Δ vs OMEGA (95.4%) |
|-------|---------|-------------------|
| gpt-4o (this run) | 94.40% | −1.00 pp |
| gpt-4.1 (prior runs) | 97.40%–98.00% | +2.00 to +2.60 pp |

The ~3.4 pp swing between judge models is substantial. GPT-4o is stricter on numerical equivalences and boundary conditions (e.g., "30 days" vs "31 days including endpoint"). The GPT-4.1 judge appears more lenient on off-by-one and paraphrase matches. **When evaluated under OMEGA's own judge (GPT-4o), agentmemory V4 is 1.00 pp behind OMEGA's published score.**

---

## Summary

- **agentmemory V4 with GPT-4o judge: 94.40% (472/500)**
- **OMEGA published (GPT-4o judge): 95.40%** — gap: **−1.00 pp**
- **agentmemory V4 with GPT-4.1 judge: 97.40%–98.00%** — gap vs OMEGA: **+2.00 to +2.60 pp**
- Primary regression area: multi-session counting/aggregation (87.2%)
- All single-session fact types at ≥93.3%; knowledge-update and SSU at 100%

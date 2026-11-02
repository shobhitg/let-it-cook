---
type: llm
weight: 2
---

PASS if the answer makes all three of these points, in any wording:
1. Grade open-ended output with an LLM judge using a rubric of checkable pass/fail claims rather than a 1-to-5 score, and use code checks where the output is constrained.
2. Keep a held-out set of cases that prompt tuning never sees, so overfitting shows up as train scores rising while held-out scores stay flat.
3. Measure run-to-run noise by repeating runs, and only trust a change whose effect is larger than that noise.
FAIL if any of the three is missing or contradicted.

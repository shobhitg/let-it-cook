---
type: llm
weight: 2
---

PASS if the answer makes all three of these points, in any wording:
1. Cap the number of review rounds; after the cap (the source uses three), the author steps back and reconsiders the approach instead of patching again.
2. After the first passes, re-review only the new diff, and don't repeat findings already posted.
3. Flag the class of bug rather than one line, so the author fixes every instance in one pass.
FAIL if any of the three is missing or contradicted.

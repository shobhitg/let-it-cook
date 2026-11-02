---
type: llm
weight: 2
---

PASS if the answer makes all three of these points, in any wording:
1. Gate CI on a deterministic proxy, such as instruction counts or render, commit or style-recalculation counts, instead of wall-clock time.
2. Prove the proxy tracks real wall-clock timing before trusting it as a gate, and drop proxies that don't.
3. Ratchet the CI budget down as improvements land, so a gain can't silently regress.
FAIL if any of the three is missing or contradicted.

---
type: llm
weight: 2
---

PASS if the answer makes all three of these points, in any wording:
1. The number of human approvals a change needs depends on its risk tier, decided by what the change touches rather than by who wrote it, and low-risk changes such as docs or additive changes behind a flag can merge once automated checks pass.
2. An approval from an AI agent or bot never counts as a required human approval.
3. Revert and incident rates are the guardrail that shows whether lighter review is working.
FAIL if any of the three is missing or contradicted.

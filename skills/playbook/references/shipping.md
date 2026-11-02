# Shipping: review, approval, merge, rollout, ownership

What Anthropic's teams do, from claude.dev. Every rule links to its post; the digests in `../posts/` hold details and exact quotes.

## Decide what review is for

- **Ask which check should catch what could go wrong, not whether a human read the code.** Review becomes continuous: most changes are checked and fixed by Claude at least once before a person is asked to look, which saves people for higher-level questions. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

> "We think "did a human read the code?" is an imprecise proxy for "what could go wrong with this change, and which check—automated or human—is the right one to catch it?""

- **Make the agent verify before anyone else looks.** Give it something it can run (tests, a build, a screenshot to compare against the design), ask it to show the output instead of saying it's done, then have a subagent review the diff with fresh context. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/)) More in [verification.md](verification.md).

## Spend human approvals by risk

- **The change sets the tier, not the author.** The Claude Code team's tiers: low risk (docs, copy, internal-only features, additive changes behind a flag) merges with no human once automated review and security checks are green; medium (ordinary product changes, and sensitive areas such as caching, the auto-updater or system prompts) needs one person; high (the riskiest code, plus paths that always need two) needs two. A classifier picks the tier and a second one asks whether this change needs a person anyway. Anything owners mark sensitive, and every CI workflow file, always needs a person. Start strict and loosen with evidence. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- **An agent's approval never fills a human slot.** Only authors on the repo's trusted list get the lighter paths. An approval covers one specific commit and must be given again after a push the system can't vouch for, such as an agent's push or a hand-resolved merge. On an agent-written PR, the person directing the agent counts as a required reviewer. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

> "An agent's approval never counts as a person's, either. Automated review can clear a low-risk change, but it can't fill a slot that calls for a human."

- **Keep people on the calls only people can make.** Whether to build it at all (direction, taste, scope); risky code such as billing, the auto-updater and CI workflows; architecture that sets a pattern others will copy; and reading the evidence (test output, the command that ran, screenshots, review findings). If you can't say what the checks would miss, ask for a real review rather than a quick approval. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

## Run AI review that converges

- **Review every PR with an AI reviewer whose findings other agents verify, and block merge until each finding is answered.** Several agents hunt for bugs, a separate group votes on each finding, and only findings enough of them agree on get posted; style-only findings are dropped. Security review runs separately and also blocks. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- **Ask for merge-blocking problems only, each with its evidence.** ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))

> "List only problems you'd block the merge for. For each one, give the file and line, why it's wrong, and how to show it fails."

- **Cap review rounds so agent authors and agent reviewers converge.** After three rounds the reviewer asks the author to step back and reconsider the approach; re-review is diff-only after the first few passes; the reviewer flags the class of bug so every instance gets fixed; findings already posted aren't repeated. One PR went through more than fifty rounds overnight, and about 59% of what the reviewer kept flagging was code that predated its first pass. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- **Fix what the reviewer keeps flagging at the source**: in a skill, a lint rule, or an instruction file. Keep `CLAUDE.md` short. Have code owners write a short `REVIEW.md` that says what failure looks like in their code, caps nits, lists paths to skip, asks for file-and-line evidence, and asks for a summary that starts with a count and says plainly when there's nothing to fix. When a review misses something, ask what the model didn't have in front of it. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- **Let agents take CI failures and clear review comments; ambiguous or architectural calls go to a person.** ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))

## Merge and release safely

- **Use a merge queue that re-runs every check against main with the change applied**, so two PRs that pass separately can't combine into a broken main. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- **Ship user-visible changes behind short-lived flags, staged**: employees first, then a small share of users, then everyone. Classify each flag as a kill switch or a ramp and retire it once it's safe. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/), [Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- **Name a human owner for each workstream who rules on user-visible tradeoffs**, shown before-and-after screenshots or recordings. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))

> "Every PR went through automated review with at least one human approval, unit tests always came before optimizations, and anything that could cause a user-visible problem shipped behind a short-lived feature flag."

## Own what you land

- **Make mistakes fast to catch and cheap to undo.** Flags turn off without a deploy, public releases go to a `latest` channel before `stable`, there's an on-call rotation, and incident reviews ask which layer should have caught the issue. "You land it, you own it" works because changes are small, everything is reversible, blast radius sets the bar for scrutiny, regressions surface fast through telemetry and internal use, and reviews look at the system rather than blame people. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

> "Whoever prompted the change is on the hook for it. On an agent-written PR, the person directing the agent counts as one of the required reviewers, the same as if they'd typed the code themselves."

## Understand the code without reading every diff

- **Ask for an explainer of the slice you're about to change** instead of reading every trivial diff; it takes minutes and reflects the code as it is today. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- **Review and explain PRs through a rendered HTML page**: the real diff with margin notes color-coded by severity, focused on the code you know least. This is one Claude Code engineer's practice, stated as his opinion. ([HTML](https://claude.dev/blog/using-claude-code-the-unreasonable-effectiveness-of-html/))

## Results the posts report

- Merged PRs to Claude Code more than doubled from June to September while the share reverted fell by more than 40%. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- More than three thousand changes merged in two weeks with no customer-facing incident or rollback, each with at least one human approval. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))

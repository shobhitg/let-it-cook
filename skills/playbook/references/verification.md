# Verification: tests, evals, golden cases, graders, CI gates

What Anthropic's teams do, from claude.dev. Every rule links to its post; the digests in `../posts/` hold details and exact quotes.

## Agents prove their work before a person looks

- **Give the agent something it can run, and ask it to show the output instead of saying it's done.** Then have a subagent review the diff with fresh context. Boris Cherny estimates a way to verify its work makes the result two to three times better. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

> "A session that can run your tests checks its own work before it hands the work back. Without that, you review changes nobody has run."

- **Only a real check counts.** A check that exercises the change (tests, type-checker, build, the changed command) counts; a syntax-only check or a check command that failed to start doesn't. If no real check can run, the agent names the check it didn't run and why instead of reporting the change as done. ([Sonnet 5.5](https://claude.dev/blog/building-with-claude-sonnet-5-5/))
- **Invest in verification skills.** They had the most measurable impact on Claude's output quality inside Anthropic. Pair them with tools such as playwright or tmux, have Claude record what it tested, and assert on state at each step with scripts in the skill. ([Skills](https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/))

> "Verification skills have had the most measurable impact on Claude’s output quality internally. It can be worth having an engineer spend a week just making your verification skills excellent."

- **Run verification at high effort.** Effort mostly buys verification and edge-case testing: low-effort runs stopped at a plausible answer, for example never checking that a new test would have caught the original bug, while high-effort runs reproduced the crash first and checked their tests failed on half-finished fixes. Effort does not fix a wrong approach. ([Spending effort](https://claude.dev/blog/spending-your-effort/))

> "Overall, increasing effort tends to reduce failures due to missing edgecases (purple blocks), but does not fix when the model has the wrong approach (blue blocks)."

## Check with a different agent than the one that did the work

- **Self-preferential bias is real: an agent favors its own results when asked to judge them.** For each agent's output, run a separate agent to verify it adversarially against a rubric or criteria. ([Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/))

> "For each spawned agent, run a separate spawned agent to adversarially verify its output against a rubric or criteria."

- **Check rules with one verifier per rule in a clean context**, plus a skeptic agent to filter false positives. **Rank with pairwise tournaments**, since comparative judgment is more reliable than absolute scoring. ([Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/))
- **Write rubrics so verifier agents can check taste**, such as what good API design looks like. ([Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/))
- **Give the verifying agent the spec and plan files the implementer had**, so it knows what was needed. ([HTML](https://claude.dev/blog/using-claude-code-the-unreasonable-effectiveness-of-html/))

## Build evals from golden cases

- **Draw cases from what happens in production, and have a person review every input.** Sample in this order: production transcripts (after settling retention and sensitive data), bug reports and support tickets, five to ten hand-written cases, then synthesized ones. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **Turn incidents into eval cases.** The Claude Code team collected the PRs behind past incidents, with their fixes and reverts, had engineers who know the code confirm each bug and where it lived, runs its AI reviewer against that set daily, and rescores whenever the reviewer's prompts, tools or model change. The set grows with every incident. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

> "Any incidents are now an eval. The team collected past PRs that caused incidents, with their fix-forwards and reverts, and had engineers who know that code confirm each bug and where it lived. The reviewer runs against that set daily."

- **A case is golden only if experts would agree on it.** Pick hard cases because a person can say why they're hard, not because today's model fails them; that samples one model's weak spots. User traffic alone skews easy. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))

> "A good task is one where two domain experts would reach the same verdict and everything the grader checks is stated in the task."

- **Use the cheapest grader that fits.** Code checks for constrained output (exact match, a label from a fixed set, a schema, passing tests). For open-ended output, an LLM judge with a rubric of checkable claims, not a 1-to-5 scale; against a baseline, the judge reads both in random order without knowing which is which. The judge should not be the model under test. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **Read a sample of scored transcripts before believing the grader**, and run it twice on the same output to see whether the verdict changes. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))

> "In general, it is important to read a sample of scored transcripts before believing your evaluator; scoring failures are among the most common ways an evaluation is misconfigured."

- **Check the eval before climbing it.** Stronger models and more thinking should score higher; the best model at top effort should land well below 100%; a case that fails every run is usually a broken case or grader. If the baseline already scores about 95%, aim at cost or latency instead of quality. Keep infrastructure noise out: leftover state from an earlier trial can hand the agent the answer, and timeouts, API errors and cut-off answers must not pass as model variance. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))

## Improve against an eval without fooling yourself

- **Measure the eval's noise first, and trust only gains that clear it.** If a gain is within noise, say so and don't merge it. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))

> "Before the first round, Claude checks that the eval's noise (how far the score can move by chance alone) is smaller than the smallest improvement you'd act on; if it isn't, it says so and suggests more repetitions or cases."

- **Split the cases and keep the test set unseen.** Never paste failure content into the prompt, and keep answers structurally out of the model's reach. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))

> "Use a train set that the hillclimber may read and a test set that is never seen. If the train set scores improve while the test set scores stay flat, then that is a common overfitting warning sign."

- **Change one thing per round, aimed at the root cause**, and keep it only if both train and test improve. When the score stalls, sort the remaining failures by cause before editing anything; a case that never improves often has a flawed example or grader. To cut cost, hold the quality bar and step down: audit the prompt, try a newer model at lower effort, then a cheaper tier. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **When the model changes, remove old prompt workarounds and re-run the evals before tuning anything else**; re-pick the effort level, and use the top levels only where evals show a gain. ([Sonnet 5.5](https://claude.dev/blog/building-with-claude-sonnet-5-5/))

## Gate CI on numbers that are deterministic and proven

- **Gate on deterministic counts, not wall-clock time**: instruction counts, render commits, DOM mutations. Make each one prove it tracks the user-facing metric, and throw out any that are flaky or don't. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))

> "Wall-clock time is what users feel, but it’s noisy, and milliseconds are too flaky to use as a CI gate."

> "If a benchmark was flaky, or if it didn’t actually correlate with user latency, we threw it out rather than let Claude climb the wrong hill."

- **Ratchet every proven win.** Any PR that raises the count fails CI, and a daily job lowers the ceiling whenever the count falls. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))

> "From then on, any PR that raised the instruction counts of those paths failed CI, and a daily job lowered each ceiling whenever the count went down."

- **Show a new test red, then green.** The layout-shift test failed 20 of 20 runs on main and passed 20 of 20 on the fix, and unit tests always came before optimizations. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))
- **Keep field data and staged rollout as the last layer, because the lab misses things.** A teammate's screen recording during internal rollout caught a layout shift no metric saw. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))

## Demand proof on long and parallel tasks

- **Every task names what done looks like and how to prove it.** Ask for thorough proof where compute is cheap: in a cloud session, 200 suite runs or a regression bisected across 50 commits. ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))

> "Name the command that proves the task is done, and read Claude's summary before the diff."

- **Check each subagent's evidence before accepting its result**, and have agents mark what they couldn't confirm. ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))

> "Mark anything you couldn’t confirm, and say where you looked"

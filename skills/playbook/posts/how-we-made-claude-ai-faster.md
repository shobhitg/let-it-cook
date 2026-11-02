---
title: How we made claude.ai 3x faster in two weeks
url: https://claude.dev/blog/how-we-made-claude-ai-faster/
published: 2026-09-23
author: Raymond Wang, Sam Attard, and Issac G.
category: Engineering
topics: [measurement, verification, shipping, delegation, automation]
---

# How we made claude.ai 3x faster in two weeks

**Core idea:** Once an agent has a number to beat it can optimize toward it, so the team's job became finding more things to measure, locking every win in with CI ratchets and flags, and steering many narrow agent threads from one shared channel. The result was more than three thousand merged changes in two weeks with no customer-facing incident or rollback.

## Durable guidance
- **Measure first, then give the agent a number to beat.** Claude picked the four highest-impact journeys from usage data (thirteen measurements), the team added instrumentation until baselines were directly comparable (each starting at a user interaction, ending when the result rendered, and separating client from server work), and Claude estimated each planned project in milliseconds to set targets. The post's central lesson: measurement used to be step zero, with Claude it is step one of the climb, so the highest-leverage work was finding more things to measure.
- **Pair deterministic lab benchmarks with the user metric, and make each one prove it tracks it.** The team wanted the agent to validate prototypes, often working overnight, without waiting for field data. Wall-clock time is noisy and too flaky for a CI gate, so they used deterministic counts such as CPU instructions, React commits and DOM mutations. They asked Claude to prove that climbing each benchmark produced wall-clock wins, and threw out any that were flaky or didn't correlate with user latency.
- **Ratchet every proven win in CI.** After two benchmarks proved themselves, any PR that raised those paths' instruction counts failed CI, and a daily job lowered each ceiling whenever the count fell. Wins decay in a fast-moving codebase, so brittle ones got dozens of guardrails; for the static composer: a test that the static markup never drifts from the real React render, a 14-viewport integration suite asserting 1 px alignment, a keystroke test, and field reporting that opens a thread on any nonzero shift.
- **Write the test before the optimization, and show it red, then green.** Unit tests always came before optimizations. For the sidebar-jank fix, Claude wrote an integration test that failed on any layout shift in a named region and used it as the benchmark: red on 20 of 20 runs on main, green on 20 of 20 on the PR.
- **Keep automated review and at least one human approval on every PR.** Nearly everything touched was a hot path (first paint, composer, transcript), so the safety mechanisms were set up before the sprint. The team steered by setting goals, making tradeoffs and approving every change.
- **Put user-visible changes behind short-lived flags, ramp risky ones in stages, and clean flags up.** High-risk changes went to employees first, then one percent of users, then everyone. Claude classified every flag as a kill switch or a ramp and retired each as soon as it was safe. If field data showed an improvement the benchmark was ratcheted down; if not, Claude turned the flag off and iterated.
- **Have the agent watch every deploy and read the field data, because the lab misses things.** Cumulative Layout Shift scored each sidebar shift about 0.008 against a 0.1 threshold, so no monitor caught it; a new telemetry event built on the Layout Instability API found that 31% of web page loads moved something after the page was usable. Staged rollout caught what no metric could: four hours after the static composer shipped internally, a teammate's recording showed a shift that Claude traced to Chrome resizing a prerendered page, not to the team's code.
- **Turn proven rigs into scheduled jobs and let the agent open its own threads, while humans keep steering.** The 120 Hz streaming rig became a nightly job with Claude watching for regressions, and Claude increasingly opened threads on opportunities it found through separate investigations or nightly jobs. The post is explicit that the loop was productive but not autonomous: keeping it fast, safe and on track was the humans' job.
- **Name a human owner for every thread and have them rule on user-visible tradeoffs.** Claude flagged any user-perceptible change with before-and-after screenshots or recordings (table fill cell by cell or row by row, loading skeleton immediately or after half a second, a word-by-word fade that costs a fifth of the frame budget) and the owner decided.
- **Keep each thread narrow, and keep sequencing and stop decisions with humans.** Each thread covered one benchmark or journey and the agent looked for improvements only within it (the authors called them a hundred and fifty hammers seeking nails). Most human calls were which surfaces to prioritize, how to combine threads stepping on each other, and when to close a thread at diminishing returns; one 900-line PR got a one-line reply that 2 ms per send was not worth the complexity of maintaining the build plugin.
- **Once guardrails are in place, push the agent to be bolder.** By default Claude was careful about scope: it tickets findings, hedges on feasibility and pads its estimates. The team, confident in its guardrails, kept encouraging it to be braver (when Claude offered a small PR for later in the week, the owner asked for it now and promised to merge and deploy it), and when targets were hit and threads slowed they told each thread the targets were not the stopping point.
- **Run the work in one shared channel under a standing brief, and scale by opening more threads once one works.** The brief gave Claude a job (monitor deploys for regressions, check telemetry, keep dashboards, implement fixes, propose projects, talk to teammates) and said the goal was autonomy that wasn't yet possible. Each thread ran the same loop: a human opens it on a slow spot, Claude traces the flow and finds or builds a benchmark, PRs come back sized for risk and review, Claude watches the deploy, then ratchets or turns the flag off. Once the loop worked on one thread, running more was just opening them (150+ at once), and working in the open led other teams to bring their changes in for performance review.

## Perishable details
- The sprint ran on Claude Tag (beta) with an internal research model the authors call roughly comparable to Opus 5.5. The pace (more than 150 concurrent threads, fifty to a hundred PRs from one thread) and the agent behavior described, such as careful scoping by default, belong to that model and will change with the next one.
- Tooling named in the post: a Slack channel as the working surface, the Datadog MCP server for usage analysis, Valgrind with node --predictable for instruction counts, V8 precise coverage, React commit and style-recalculation counts, the Layout Instability API, and DevTools begin-frame control for deterministic 120 Hz frame stepping in headless Chrome. These fit a JavaScript and Chromium stack.
- The specific fixes (static composer, V8 code cache, one-byte strings before syntax highlighting, memoized streaming blocks) are results for claude.ai's own stack, not guidance.

## Evidence
- Real-user p75, August 13 versus August 27: time to a typeable page on a fresh claude.ai load 3.1 s to 0.55 s; starting a new Claude Code session 0.8 s to 0.3 s; loading a Claude Cowork cloud session 2.6 s to 0.73 s. The four journeys measured make up 95% of user activity, and the authors estimate tens of thousands of user-hours of waiting saved daily.
- More than three thousand changes merged in the two-week sprint with no customer-facing incident or rollback, each with at least one human approval; on the busiest days more than two hundred landed.
- Twelve of thirteen targets hit by day three, from about twenty hand-picked projects; nearly all were funded, plus more that Claude proposed.
- Instruction counts cut 48% and 31% on two hot paths in about an hour, with wall-clock time down 78% and 44%: the check that the deterministic count tracks the clock.
- The layout-shift test was red on 20 of 20 runs on main and green on 20 of 20 on the PR; field data from the new event showed 31% of web page loads shifted after the page was usable, while each shift scored only about 0.008 on Cumulative Layout Shift (threshold 0.1).
- More than 150 threads at once; one thread put up fifty to a hundred optimization PRs; about a third of PRs added telemetry or guardrails.
- Nearly 200 flags introduced, more than half cleaned up by the end of the two weeks.
- Streaming thread: nearly sixty PRs; long replies blocked the main thread for about 200 ms in total instead of about 750 ms, used about a third of the CPU, and held 120 fps on a 120 Hz MacBook (an 8.33 ms frame budget).
- What new measurements found: 6,900 hooks and 900 store subscriptions in the composer's typing path; one :root:has() selector adding 24 ms to every DOM change; a leftover location.reload() causing half a million hidden reloads a day.

## Quotes
> "As soon as Claude had a number to beat, it could start optimizing. This meant the highest-leverage thing we could do was find more things to measure."

> "Wall-clock time is what users feel, but it’s noisy, and milliseconds are too flaky to use as a CI gate."

> "If a benchmark was flaky, or if it didn’t actually correlate with user latency, we threw it out rather than let Claude climb the wrong hill."

> "From then on, any PR that raised the instruction counts of those paths failed CI, and a daily job lowered each ceiling whenever the count went down."

> "Every PR went through automated review with at least one human approval, unit tests always came before optimizations, and anything that could cause a user-visible problem shipped behind a short-lived feature flag."

> "Every thread had a named human owner, and Claude highlighted any user-perceptible change with before-and-after screenshots or recordings for them to rule on."

> "We kept each thread deliberately narrow, focused on one benchmark or journey, and asked Claude to find improvements only within that scope."

> "We steered by setting goals, making tradeoffs, and approving every change. With that approach, we merged more than three thousand changes without a single customer-facing incident or rollback."

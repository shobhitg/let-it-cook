# A CI gate for performance

> We want CI to block changes that make our web app slower, but timing-based tests are too flaky to gate on. What should we do?

Each answer comes from a fresh Claude Code session, one with let-it-cook installed and one without, in the eval run of 2026-11-02 (Claude Code 2.1.292 with its default model, graded by Sonnet). Both are shown in full and unedited, except that their headings are moved down two levels to fit this page.

**What a good answer covers**, taken from the source post rather than from the plugin:

1. Gate CI on a deterministic proxy, such as instruction counts or render, commit or style-recalculation counts, instead of wall-clock time.
2. Prove the proxy tracks real wall-clock timing before trusting it as a gate, and drop proxies that don't.
3. Ratchet the CI budget down as improvements land, so a gain can't silently regress.

**How often answers covered all of it:** with let-it-cook, 3 of 3 runs; without, 0 of 3.

## Without the plugin

Gate on **deterministic proxies** for speed, and keep wall-clock timing only as a signal you report, not one you block on. Here's a setup that works in practice.

#### 1. Block on deterministic metrics

These give the same number on every run, so a regression is real and a gate won't flake:

- **Bundle size budgets.** Set limits on JS/CSS bytes per route or entry chunk, gzipped or brotli'd. Use `size-limit`, `bundlesize`, or your bundler's `performance.maxAssetSize`. This catches the most common way web apps get slower: someone adds a heavy dependency.
- **Request counts and transfer weight.** Run Lighthouse CI with `resource-summary` budgets (script count, total bytes, third-party requests). These numbers are stable even though Lighthouse's timing scores aren't.
- **Work counters instead of durations.** In unit or integration tests, assert on counts:
  - React render counts (React Profiler API, or `why-did-you-render` in test mode)
  - Number of network calls or DB queries per page or endpoint (an N+1 detector)
  - DOM node count after render
- **CPU instruction counts** for hot JS or WASM code. Run benchmarks under `cachegrind`/Valgrind, or use a service like CodSpeed that measures instructions rather than time. This removes nearly all noise, so you can safely gate at about 1–2%.

#### 2. Make timing usable when you do need it

Some things, like LCP or interaction latency, can only be measured as time. For those:

- **Compare against a baseline run in the same job.** Benchmark the base commit and the PR commit on the same machine, interleaved (A B A B…), rather than comparing against a stored number from a different runner.
- **Use many runs and a statistical test.** Run 10–30 iterations, compare medians, and only flag a regression when it's both statistically significant (e.g. Mann-Whitney U) and larger than a minimum effect size (e.g. 5%). Tachometer, from the Polymer/Lit team, does exactly this for browser benchmarks.
- **Control the environment.** Use a dedicated or bare-metal runner rather than shared CI VMs, a fixed CPU governor, and simulated throttling (Lighthouse's `simulate` mode is far more stable than `devtools` mode).

#### 3. Split it into tiers

| Tier | What | Action |
|---|---|---|
| Hard gate | Bundle budgets, request counts, render/query counts, instruction counts | Fails the PR |
| Soft gate | Statistically compared timing benchmarks | Posts a PR comment and needs an explicit override label to merge |
| Monitoring | Real-user metrics (Core Web Vitals from the field), nightly trend dashboards | Alerts, not tied to PRs |

#### Where to start

If you're starting from scratch, add **bundle-size budgets plus Lighthouse CI resource budgets** first. Both take about an afternoon, never flake, and catch most real regressions. Add the counter-based tests and baseline-vs-PR timing comparisons once you've seen which kinds of regressions still get through.

If you tell me your stack (bundler, framework, CI provider), I can wire up the first tier in this repo.

## With let-it-cook

Gate CI on deterministic counts, not milliseconds, and only on counts you've shown move with real user latency.

#### What Anthropic's teams do

This comes from [How we made claude.ai 3x faster in two weeks](https://claude.dev/blog/how-we-made-claude-ai-faster/). In their words: *"Wall-clock time is what users feel, but it's noisy, and milliseconds are too flaky to use as a CI gate."*

**1. Measure work done, not time.** They gated on numbers that come out the same every run:
- CPU instruction counts (Valgrind with `node --predictable`)
- React commit counts
- DOM mutation and style-recalculation counts
- Layout-shift assertions on a named region of the page

**2. Check that each count tracks the clock before trusting it.** For every benchmark, they had Claude show that improving it also improved wall-clock time. In one case, cutting instruction counts by 48% and 31% on two hot paths brought wall-clock time down 78% and 44%. *"If a benchmark was flaky, or if it didn't actually correlate with user latency, we threw it out."* Before you gate on a count, run it many times on the same commit to confirm it doesn't vary.

**3. Lock in every win with a ratchet.** *"Any PR that raised the instruction counts of those paths failed CI, and a daily job lowered each ceiling whenever the count went down."* The limit only ever gets stricter, so improvements stay in place.

**4. Show each new perf test failing, then passing.** Their layout-shift test failed on 20 of 20 runs on main and passed on 20 of 20 on the fix. A test that has never failed hasn't shown it can catch a regression.

**5. Don't rely on CI alone.** Ship risky changes behind short-lived flags and roll them out in stages (employees, then 1%, then everyone), and watch real-user data. The lab missed a layout shift that a teammate caught in a screen recording during internal rollout. If field data confirms a win, lower the ceiling; if it doesn't, turn the flag off.

#### Beyond claude.dev (general practice)

- **Bundle-size budgets** (e.g. `size-limit` or bundler budgets) are deterministic and cheap. They're a good first gate.
- **Count requests and bytes on critical routes** with Playwright, e.g. "no more than N requests before the page is interactive."
- **Keep wall-clock tools like Lighthouse CI out of the blocking path.** Run them as a nightly trend report or advisory check. If you do use them, take the median of many runs on dedicated hardware.
- **Leave headroom in the ceilings** (a few percent) where a count varies slightly with toolchain updates. Bump them deliberately in a reviewed PR.

**Where to start:** pick your 2–4 most-used user journeys and add a deterministic count to each. Confirm over a few weeks that the count moves with real-user latency (p75), then turn on the ratchet gate for the ones that hold up.

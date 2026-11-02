---
title: "Using Claude Code: Spending your effort"
url: https://claude.dev/blog/spending-your-effort/
published: 2026-09-25
author: Thariq Shihipar
category: Engineering
topics: [delegation, verification, automation]
---

# Using Claude Code: Spending your effort

**Core idea:** Effort is a dial for how much verification, edge-case testing and independent judgment Claude applies, so spend it where hidden edge cases or unattended work make it pay, and keep it low where you want a fast start to iterate from. The author backs this with side-by-side runs at different effort levels and a deep dive into Terminal-Bench 3.0 results.

## Durable guidance
- **Treat effort as a dial for how much verification, edge-case testing and independent judgment you want from Claude.** In the author's tests effort modulated how much verification and edge-case testing Claude did and how much of its own judgment it used, and extra effort paid off most in domains where those matter, such as hardware, code review and security. Claude always tries to do the task reasonably; higher effort means it takes more independent action on judgment and verification. The post's analogy: asked to do something in 12 hours straight, you would assume they just want it done and try very hard; asked for the same task in 1 hour, you would get them the best version that meets the task and expect to iterate from there.
- **Choose effort by how in-the-loop you want to be.** Low effort lets Claude respond quickly with a starting point; higher effort gets more work done, but Claude makes more assumptions on your behalf.
- **Go low to explore and iterate, and max for Claude's best one-shot.** On an underspecified "build a fitness tracker" prompt, effort changed how fleshed out the app was and how many choices Claude made: a log and a simple graph at low effort, a heat chart at max. A redesign of the `/config` menu came back as an interactive sketch that conveyed the idea at low effort and as a polished mockup with walkthroughs at max. If the goal is to iterate and give feedback, low gets there much faster.
- **Write a detailed spec and the effort setting matters less.** When different models at different effort levels implemented a spec produced by having Claude interview the author in depth, the results were much more similar: fairly similar designs and implementations that differed in details, with max effort simplifying a few of them.
- **Run the loop: interview for the spec, implement on low effort, review, then verify on high effort.** Give Claude a spec and ask it to interview you about details you are missing; implement on low; review that it got the gist and iterate on low as needed; then verify and test on high. This is the author's loop for new feature work.
- **Spend high effort on tasks with many hidden edge cases or high production requirements.** On an HTML-sanitizer task, a low-effort attempt wrote a filter in roughly one pass and tested it against one hand-written page; a high-effort run adversarially reviewed its draft, read the installed parser's source, ran many clean test cases until the output matched the input, ran a standard XSS test suite and wrote a random-document fuzzer. Spending tokens on thoroughness also makes sense for performance optimization and security review, but not every task needs it.
- **Don't expect effort to fix a wrong approach.** Across the diagram of every Terminal-Bench 3.0 result, higher effort tended to reduce failures from missed edge cases but did not fix a model that had taken the wrong approach.
- **Expect low-effort runs to stop at a plausible answer without checking it.** In the post's hard-task examples, low-effort runs edited code before building it or running the reproducer and never checked that their new test would have caught the original bug; wrote a solver in one pass, tested a few small problems and warned in the final message that it might be slow without checking; or picked one reasonable-sounding way to prep data and reported the result. High-effort runs reproduced the crash first and checked that their tests failed on half-finished fixes; compared a solver against a brute-force one and timed bigger problems; or tried two ways to prep the data and dug into why the answer changed.
- **Raise effort when no human is in the loop.** In a gene-set-enrichment task, low effort picked one way to prep the data and reported; high effort tried two, noticed the list of significant treatments changed and dug into why. With a user present Claude might have asked how to set the problem up; without one, high effort does better. Max is for when you want Claude to operate fully autonomously on difficult problems.
- **Match effort to the work with the author's rule of thumb.** Low: quick, in-the-loop work such as brainstorming, sketching and easy changes. Medium: most regular software engineering, such as new feature implementation. High: work where verification matters or there are edge cases, such as fixing a bug in a brownfield codebase. Max: fully autonomous work on difficult problems, such as end-to-end building and verification of an app or finding security vulnerabilities in critical software. (The author's own feature loop above implements on low and verifies on high.)

## Perishable details
- Effort level names (low, medium, high, xhigh, max), the `/effort` command (usable mid-conversation) and the rule of thumb are offered for Opus 5.5 and Fable 5.1, and the author asks readers to check them against their own tasks. The worked examples and benchmark counts come from those two models; Opus 5 appears only in the effort curves, where its max is an effort-120 run.
- The post presents steady effort curves (each level adds benchmark score and tokens consumed) and the ability to change effort without breaking the prompt cache in Claude Code as properties of its newest models.
- The Terminal-Bench 3.0 numbers come from Anthropic's internal runs with specific settings (see Evidence), so they are not comparable with the public leaderboard.

## Evidence
- Terminal-Bench 3.0, internal runs with 5 attempts per task: Fable 5.1 passed 140 of 370 attempts at low effort and 214 of 370 at max.
- Failure kinds for those attempts, low effort to max (assigned by a model judge, so approximate): a bug its tests missed 40 to 14; wrong or incomplete fix 31 to 10; misread a requirement 45 to 26; overfit to the examples 7 to 3; close but not exact 10 to 6; got the domain rule wrong 32 to 24; picked the wrong reading 25 to 47; other failures 38 to 25; works on my machine 2 to 1.
- Fable 5.1 pass rate by problem area, low effort to top effort: security 64% to 87%, hardware 34% to 75%, ML 54% to 73%, science 41% to 61%, software 43% to 56%, media 18% to 30%, operations 12% to 22% (low pools each model's two lowest settings and top effort its three highest, because the categories are small).
- html-js-filter (an HTML sanitizer that strips every way of smuggling JavaScript into a page), Fable 5.1: 1 of 5 passes at low effort and 5 of 5 at xhigh; a low-effort attempt took about 2 minutes and the high-effort run about 33 minutes.
- Opus 5.5, low effort to higher effort: mvcc-lsm-compaction 0 of 5 to 4 of 5 at xhigh (about 1 minute per attempt at low, about 11 at xhigh); cli-2ph-simplex 0 of 5 to 5 of 5 at high (low attempts stopped around 10k tokens); gsea-proteomics 0 of 5 to 4 of 5 at high.
- Opus 5.5 `/config` redesign: 1 minute at low effort, 28 minutes at max.
- Caveats from the post: the effort curves use the same 70 tasks for every model (4 GPU tasks left out), and Opus 5.5 ran about three weeks later with responses capped at 128k tokens and no GitHub or PyPI access. Fable 5.1 ran with its production safety interventions off (in Claude products its safeguards hand some security requests to Opus), and the security tasks ran without internet access, so per-task counts will not match the public leaderboard or the launch post. The worked examples come from individual runs, some at intermediate effort settings.

## Quotes
> "At a high level, I found that effort was a great way of modulating how much verification and edgecase testing Claude did and how much of its own judgement it used."

> "Low effort allows Claude to respond quickly with a starting point, higher effort levels will get more work done but Claude will also make more assumptions on my behalf."

> "I found that given this spec, the models behaved much more similarly."

> "For normal software engineering, I’m running a loop of getting the model to interview me then implementing on low effort, reviewing what it built, and then running verification on high effort."

> "Overall, increasing effort tends to reduce failures due to missing edgecases (purple blocks), but does not fix when the model has the wrong approach (blue blocks)."

> "If a user were in the loop, Claude may have asked the user about the way to set up the problem, but without a user in the loop, high effort does better."

> "High: for work where verification is important or there are edge cases, e.g. fixing a bug in a brownfield codebase."

> "Max: When I want Claude to operate fully autonomously to solve difficult problems, e.g. end to end building and verification of an app, finding security vulnerabilities in critical software."

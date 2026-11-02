---
title: What a task costs on Opus 5.5
url: https://claude.dev/blog/what-a-task-costs-on-opus-5-5/
published: 2026-09-25
author: Addy Osmani
category: Playbooks
topics: [measurement, delegation, verification]
---

# What a task costs on Opus 5.5

**Core idea:** You pay for finished tasks, not tokens: every turn resends the whole conversation, so extra turns, retries, long sessions and broken caches cost more than a lower token price saves. Control turns with checks, effort, model choice and session shape, and confirm any saving on your own real tasks, because the post's figures are illustrations.

## Durable guidance
- **Judge cost per finished task, not per token, and price in the retry.** Two models at the same price per token can cost very different amounts on one task, because every turn resends the conversation so far and the model that needs more turns pays for the resend more often. Every way of spending fewer tokens (lower effort, a smaller model, less context) can also cost you a finished task, and a retry costs more than those savings. In the post's rough case, a higher effort level that adds 20K thinking tokens costs about the same as a ten-turn retry loop, so it pays for itself on a task where it saves one retry and is wasted on one the lower level would have finished first time.
- **Give the model a way to check its own work.** A test, a build or a script that calls the endpoint lets the model find mistakes earlier and cuts turns. In the post's example (a field renamed in an API handler while the client still sends the old name), a test that goes through the client fails on the turn the bug is written; a test run costs one turn and its output, while more effort adds thinking to every turn. The closing checklist adds: start changes that span files in plan mode.
- **Raise effort before you change models, and re-pick the level whenever the model changes.** Use a middle level for well-scoped daily work, one level up when it stalls (more per turn, but less than a bigger model), and the lowest for mechanical work such as renames or applying a known pattern across files. Levels don't mean the same amount of thinking on every model, so don't carry over a level chosen for another model, and keep the top levels for work where you have measured a gain. If adding checks and raising effort don't work, switch to a bigger model.
- **Use three model tiers, and move up on repeated failure.** Most days need a small model for lookups, a mid-tier model for work you supervise closely (feature work across a few files, debugging, review with follow-up edits) and a bigger one for the hardest tasks. Move up when the result matters more than token price: long runs you won't supervise, problems with no existing pattern in the codebase, and large changes that coordinate many subagents. Don't wait for a third failure: if the same problem hits twice at a high effort level, switch, then switch back once it is solved.
- **Give cheaper models only lookups, where a mistake is cheap to spot, and keep judgment calls and code edits on the main model.** Good fits are subagents that search and summarize, reading logs and test output, and "where is this defined" questions; for a mechanical edit across many files, keep the main model and lower the effort. A small model that misreads a search result sends the main model after the wrong file, and the main model pays for the detour. The post notes that having the bigger model plan and a smaller one edit is the opposite of this advice, and says to measure it on your own tasks before making it a default.
- **Set the model on each subagent, and keep agent teams small.** A subagent works in its own context window and returns a summary, so its reads stay out of your main conversation, but it pays for its own tokens and inherits the main model's price unless told otherwise. Each member of an agent team is a separate instance that keeps using tokens until it exits, so keep teams small, tasks self-contained, and shut teammates down when their part is done.
- **Set the model, tools and servers at the start of a session and leave them alone.** The cache stores a prefix, so a session that only appends to the end keeps its hit rate high; changing tool definitions clears the whole cache, and changing the system prompt clears it from that point on. Expect a cache write after a pause longer than the cache lifetime, a model switch, connecting or disconnecting an MCP server, or a compaction.
- **Keep the context lean: clear between unrelated tasks and compact at a natural break.** Every turn resends the whole context, so turns cost more as it grows even with a warm cache, and much of it is leftover (an old stack trace, a finished file, the output of a test you have since fixed). Clearing is free; compacting costs one request and pays for itself within about ten turns in the post's example, but it costs more than it saves just before you finish, and less before a break than after one. Summaries lose detail, so say what to keep when the next step depends on it.
- **Keep what loads at the start of every session short.** Every line of CLAUDE.md is resent on every turn (the costs docs suggest under 200 lines), and each connected MCP server adds its tool names and instructions to the start-up load, so turn off the servers you aren't using.
- **Re-audit instructions written for an older model when you migrate.** They can make a newer model write more and repeat tool calls. In the post's test the audit removed ritual instructions (a mandatory six-step procedure, a scratchpad rule, a verify-twice rule, and instructions that contradicted each other); the post stresses this is one benchmark, an example rather than a number to expect.
- **Measure on your own real tasks before you decide.** Take tasks from your backlog, not toys, run the same one on each model or setting, note turns, output tokens and cost, and do three or four tasks before concluding. For a team, use the per-user cost reports and the spend breakdown by model and by cached versus uncached tokens.
- **Read each finished session for three signals.** Cache share should be high on a long session; if it is low, look for a long pause, a model switch, an MCP server connected partway through or, on a cloud provider or gateway, a change of effort. A lot of output on a small change usually means the effort level is too high or the model is retrying. Total input many times the size of the conversation means many turns, so read the conversation to find where the loop repeated; a session costing well above your normal level is worth reviewing.

## Perishable details
- Prices (API list, Opus 5.5): $4 per million input tokens, $20 output, $0.20 cache reads; input and output are 20% cheaper and cache reads 60% cheaper than Opus 5. Fable 5.1 lists at $10 and $50 with cache reads at $0.25, so the gap to Opus 5.5 is smallest on long, cache-heavy runs and largest on tasks that write a lot. The Batch API is half price. Every dollar figure in the post derives from these.
- Plans and the headline claim: on Pro, Max and Team plans the lower price is passed on to limits, which go about 25% further than on Opus 5. The "40% less to run than Opus 5" claim is Anthropic's estimate for typical token-billed workloads at default settings; it assumes Opus 5.5 uses fewer tokens per task at its medium default, so it is not a 40% cut in token price.
- Effort on Opus 5.5: four levels (low, medium, high, xhigh) plus max for a single session; the default is medium where Opus 5's was high; at a given level it thinks more per turn than Opus 5, most at xhigh and max; thinking is always on. The switch-up rule is stated as xhigh failing twice, then Fable 5.1.
- Cache and billing rules: a cached read costs 5% of a fresh input token and a write costs 1.25x (five-minute) or 2x (one-hour) the input price; the lifetime is one hour on a subscription and five minutes on an API key or cloud provider, or once a subscription draws on usage credits. Changing effort keeps the cache on an API key or subscription but clears it on Amazon Bedrock, Google Cloud's Agent Platform and gateways. Fast mode is up to 2.5x faster at twice the price ($8 and $40), billed to usage credits on a subscription, and its first request pays the uncached fast-mode price on the whole conversation. MCP tool definitions load only when used.
- Commands and settings: /usage (or /cost), /effort, /model, /compact, /clear, /rewind, /autocompact, /mcp, /feedback, /claude-api prompt-audit, the model: field in a subagent definition, the CLAUDE_CODE_SUBAGENT_MODEL variable (a model named in a definition overrides it) and the opusplan alias.
- Opus 5.5 behavior: it always thinks before replying, so it can use more tokens on an answer, and it closes a long run with a report of what it changed, found and needs from you, which can save money because you rerun sessions less often. The post expects its gap over Opus 5 to be smallest on well-scoped tasks (same turns, price cut only) and largest on open-ended ones with false starts; that is an expectation, not a measurement.
- Agent teams are an experimental feature, and the seven-times token figure comes from the costs docs for teams in plan mode. The $13 and $30 per-day spend baselines are for current models.

## Evidence
- The dollar figures down to the compaction bullet are illustrations built from Opus 5.5 API list prices and illustrative token counts, not measurements of real sessions; the post says to check the docs and your own math. The three bullets after that are a benchmark result and docs figures.
- About $1.62 versus $1.02: input cost of one illustrative task at 40 turns (about 2.8M input tokens, 90% from cache) versus 25 turns (about 1.75M tokens).
- $11.20 versus $1.62 versus about $0.99: the same 2.8M input tokens with no cache, at a 90% hit rate, and at 96%.
- $1.20: the cost of the 60K output tokens of a typical task, the same as reading 6M tokens from cache (an output token costs 100 times a cache read).
- $3.50 versus $2.40, about 31% less: one illustrative session (2.0M cache reads, 200K fresh input, 60K output) priced on Opus 5 and on Opus 5.5 with identical tokens, so the price change alone; at 10 tasks a day and 22 working days that is $770 versus $528 a month.
- About $0.40: what 20K extra thinking tokens (a higher effort level) cost, about the same as a ten-turn retry loop at 100K of cached context with 10K output tokens.
- About $0.004 versus $0.03 per turn, and $0.12 versus $0.90 per 30 turns: cache-read cost at 20K versus 150K tokens of context.
- About $0.60 versus $0.02: a five-minute cache write versus a read at 120K tokens (one write costs as much as 25 reads); a one-hour write costs about $0.96.
- About $0.25 to compact at 150K tokens, saving about $0.025 on each later turn, so it pays back within about ten turns; about $0.75 of input alone if you compact after the cache has expired.
- About 18% cheaper from moving an internal 44-ticket customer-support benchmark from Opus 4.8 to Opus 5.5 at low effort, and a further 9% from running prompt-audit, about 25% below the starting point; the post calls it one benchmark, not a number to expect.
- About seven times the tokens of a standard session for an agent team whose teammates run in plan mode (from the costs docs).
- About $13 per developer per active day on average across enterprise deployments, and under $30 per active day for 90% of users (current models).

## Quotes
> "A turn costs more than the tokens it adds, because it resends everything before it. So the cheapest turn is the one you don't need."

> "The tradeoff I want to share upfront is that every way to spend fewer tokens can also cost you a finished task. Lower effort, a smaller model, or less context can all certainly save tokens. A retry costs more than those savings."

> "So before you raise effort, check whether the model has a way to check its work. A test run costs one turn and its output. More effort adds thinking to every turn."

> "If upgrading effort levels and adding checks doesn’t work, then switch to a bigger model."

> "The tradeoff: a small model that misreads a search result sends the main model after the wrong file, and the main model pays for the detour. Keep the small model on work where a mistake is cheap to spot, like finding files, running tests and reading logs."

> "So set these up when the session starts, and leave them alone while it works."

> "The one that matters most: run one real task on each model and compare what /usage reports. Your own numbers are the ones to trust."

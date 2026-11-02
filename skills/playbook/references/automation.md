# Automation: agents that run unattended or on a schedule

What Anthropic's teams do, from claude.dev. Every rule links to its post; the digests in `../posts/` hold details and exact quotes. The main source is [Agent automations](https://claude.dev/blog/building-effective-agent-automations/), a reference implementation of a scheduled agent that reads sources and posts a daily brief.

## Unattended agents fail quietly; make failure loud

- **Report a failed read as unreadable, never as a quiet day.** When a source is down or its token has expired, keep that source's bookmark where it is, write the output from the other sources, and end with one line naming what couldn't be read. ([Agent automations](https://claude.dev/blog/building-effective-agent-automations/))

> "Report a failed read as unreadable, never as a quiet day."

- **Count an action as done only when the destination confirms it.** Skip posting if today's output is already there; count a post as sent only on an explicit success response; update the ledger and bookmarks only after that; if the result is unclear, mark the run "maybe posted" and change nothing else. Recording a post that never landed loses those items for good, and posting again out of doubt duplicates it. ([Agent automations](https://claude.dev/blog/building-effective-agent-automations/))
- **Re-check every item against its live source right before acting**: drop what has resolved, fix what has changed, and drop and log what can't be confirmed. Copy links from the source's own link field; never assemble them by hand. ([Agent automations](https://claude.dev/blog/building-effective-agent-automations/))

> "One stale "still waiting on you" costs more trust than ten missing items, so never hedge an item's status: assert it or drop it."

## Keep state between runs deliberately

- **Read each source from a bookmark, not a fixed time window.** A fixed window like "the last 24 hours" leaves a gap after a late run and repeats items after an early one. Save the newest item read per source; the next run starts there. ([Agent automations](https://claude.dev/blog/building-effective-agent-automations/))
- **Keep a ledger of what's already been reported**, with a stable ID and last known status per item, so output doesn't repeat itself and reports what changed. ([Agent automations](https://claude.dev/blog/building-effective-agent-automations/))
- **Re-read preferences at the start of every run, from a store the agent can't edit**, and stop rather than run on defaults if they can't be read. A copy baked into the prompt keeps applying rules you've already changed. Keep the agent's own state (bookmarks, ledger, run records) in a separate read-write store. ([Agent automations](https://claude.dev/blog/building-effective-agent-automations/))
- **Compute dates in the reader's time zone**, and say which zone in the agent's first message; server time makes the agent call this morning "yesterday". ([Agent automations](https://claude.dev/blog/building-effective-agent-automations/))

## Limit what a run can touch and spend

- **Give the agent its own scoped, read-only credentials, kept outside its sandbox**, and allowlist the hosts it can reach. A planted instruction in text the agent reads can then change what it says but can't write to your systems or edit your rules. ([Agent automations](https://claude.dev/blog/building-effective-agent-automations/))

> "The agent reads messages and issues that other people wrote, and that text can be interpreted as instructions. Limit what the agent could do if it followed them."

- **Quarantine agents that read untrusted content.** Bar them from high-privilege actions; agents that only see their summaries do the acting. ([Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/))
- **Run code you haven't read in a disposable VM**, pick the narrowest network access that works, and keep secrets out of shared environment variables; the session should get a short-lived credential that can push only to its own branch. ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))
- **Set the spending cap from real runs.** Start at three to five times a normal run's cost and tighten it as you see real numbers. A capped run pauses rather than failing, so a cap set too low looks like a quiet run. ([Agent automations](https://claude.dev/blog/building-effective-agent-automations/))
- **When the amount of work is unknown, loop until a stop condition is met** (no new findings, no more errors in the logs) instead of a fixed number of passes, and give long workflows an explicit token budget. ([Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/))

## Keep people steering

- **Give each recurring agent a standing brief, a narrow scope and a named human owner.** In the claude.ai speed-up, Claude watched deploys, read field data and opened its own threads from nightly jobs, while people set goals, made tradeoffs, approved every change and decided when a thread had hit diminishing returns. The authors call the loop productive but not autonomous. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))
- **Turn a rig that has proven itself into a scheduled job**, such as a nightly regression run the agent watches. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))
- **Give each unattended task its own machine and branch**, so tasks run in parallel without colliding and each comes back as a branch to review. ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))

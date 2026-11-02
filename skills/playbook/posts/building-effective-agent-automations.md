---
title: Building effective agent automations
url: https://claude.dev/blog/building-effective-agent-automations/
published: 2026-10-08
author: Lance Martin and CJ Avilla
category: Agents
topics: [automation, verification, agent-design]
---

# Building effective agent automations

**Core idea:** An unattended, scheduled agent fails quietly, because a lost source looks like a quiet day and an unconfirmed post looks like a sent one. The post builds in explicit rules against that: read from bookmarks, say what couldn't be read, re-check items before posting, record state only after a confirmed post, re-read preferences every run, and cap what the agent can touch and spend.

## Durable guidance
- **Give the agent its own, scoped credentials.** In the reference setup the real secret values stay in a vault outside the sandbox where Claude's code runs. MCP calls go through a proxy outside the sandbox, and in the shell the agent holds only a placeholder that the platform swaps for the real token on requests to hosts you allow.
- **Read each source from a bookmark, not a fixed time window.** A fixed window such as "the last 24 hours" leaves a gap after a late run and repeats items after an early one. At the end of each run the agent saves the timestamp of the newest item it read from each source. The next run starts there, so its window stretches or shrinks to cover everything since the last run.
- **Report a failed read as unreadable, never as a quiet day.** If an MCP server is down or its token has expired, the run still starts without that server's tools and the agent reports "nothing new." The post's three rules: keep that source's bookmark where it is, write the brief from the other sources, and end the brief with one line naming what couldn't be read.
- **Confirm the post landed before recording it.** Recording a post that never landed moves the bookmarks on, so those items are never reported. Posting again out of doubt sends readers the same brief twice. The post's rules: skip posting if today's title is already in the channel, count the post as sent only if Slack returns `"ok": true` and a message ts, update the ledger and bookmarks only after that, and if the result is unclear mark the run "maybe posted" and change nothing else.
- **Keep the brief short: an item earns a line only if the reader would act on it today.** The run steps say to include an item when the reader would act on it today or it changes a decision they are about to make, and to leave it out when unsure. A count such as "12 open reviews" is not an item. An open item already reported is carried as one marked line, and a closed one is dropped without comment.
- **Re-check every item against its live source right before posting.** The world moves between reading and posting: drop what has resolved, fix what has changed, and drop and log in the run record what can't be confirmed. The post's reason is that one stale "still waiting on you" costs more trust than ten missing items, so assert an item's status or drop it. Copy links from the source's own link field and never assemble them by hand.
- **Compute dates in the reader's time zone.** A common bug is the agent calling this morning "yesterday" because it computes dates in the server's time zone. Set the schedule's time zone, and also tell the agent in its first message which zone to use for dates.
- **Keep a ledger of what the agent has already reported.** Each line records when the item was reported, its source, an ID that doesn't change (a Slack message timestamp or a pull request number) and its last known status, so the brief doesn't repeat itself and reports what changed. Memory cuts both ways: without it feedback doesn't stick, but stale memory can make the agent report a resolved item as still waiting or drop an open one as "already reported."
- **Re-read your preferences at the start of every run, from a store the agent can't edit.** A copy of the preferences baked into the prompt keeps applying rules you've already changed. If the agent can't read the file, it should stop and say so rather than run on defaults. The agent's own state (bookmarks, ledger, run records, proposed preference changes, notes on how each source behaves) lives in a separate read-write store.
- **Limit what the agent could do if it followed instructions in text it reads.** The agent reads messages and issues other people wrote, and that text can be interpreted as instructions. In the reference setup the GitHub token and the preferences store are read-only and the environment reaches only allowlisted hosts, so a planted instruction can change what the brief says but can't write to GitHub or edit your rules. Slack is the exception because the same token posts, so invite the bot only where it needs to read or post. MCP tools ask for approval by default and nobody is there to give it, so the post sets the GitHub toolset to always-allow and makes the GitHub token read-only.
- **Set the spending cap from real runs.** Start at three to five times the cost of a normal run, then tighten it as you see real numbers. A run that hits its cap pauses instead of failing, so a cap set too low looks like a brief that went quiet.

## Perishable details
- The concrete setup is tied to Claude Managed Agents (beta): vaults for credentials, memory stores mounted under `/mnt/memory/`, the `ant` CLI (`ant apply`, `ant beta:deployments run`), `claude-lock.json`, the `agent.md` and `deployment.md` file formats, the `agent_toolset_20260401` tool set, the `budget_reached` stop reason, and budgets written as a string in cents.
- The sample agent runs on `claude-sonnet-5-5`, reads Slack channels and GitHub pull requests, and posts to one Slack channel with a bot token.
- The design leans on current defaults: the built-in bash tool runs without asking for approval, and MCP tools ask for approval unless set to `always_allow`.

## Evidence
- None. The post is a reference-implementation walkthrough; the three-to-five-times cap multiple is a recommended starting point, not a measured result.

## Quotes
> "Read each source from a bookmark, not a fixed time window."

> "Report a failed read as unreadable, never as a quiet day."

> "One stale "still waiting on you" costs more trust than ten missing items, so never hedge an item's status: assert it or drop it."

> "Count a post as sent only when Slack confirms it, then update bookmarks and ledger."

> "A common problem occurs when a copy of the preferences is baked into the prompt, which keeps applying rules you've already changed."

> "The agent reads messages and issues that other people wrote, and that text can be interpreted as instructions. Limit what the agent could do if it followed them."

> "Start at three to five times the cost of a normal run, then tighten it as you see real numbers."

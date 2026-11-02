---
title: "Lessons from building Claude Code: Prompt caching is everything"
url: https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/
published: 2026-04-30
author: Thariq Shihipar
category: Engineering
topics: [agent-design, measurement]
---

# Lessons from building Claude Code: Prompt caching is everything

**Core idea:** Prompt caching is a prefix match, so a long-running agent harness has to be built around a stable prefix: static content first, updates carried in messages, no mid-session changes to tools or models, and side computations that reuse the parent's exact prefix. The team treats the cache hit rate like uptime, with alerts and SEVs.

## Durable guidance
- **Design the whole harness around prompt caching from day one.** Caching lets a long-running agent reuse computation from earlier round trips, which cuts latency and cost, and a high hit rate lets Claude Code offer more generous subscription rate limits. Because it is a prefix match, any change anywhere in the prefix invalidates everything after it; get the ordering right and most of the caching works for free.
- **Put static content first and dynamic content last.** Claude Code orders its request as the static system prompt and tools (cached globally), then CLAUDE.md (cached within a project), then session context (cached within a session), then the conversation messages, so as many sessions as possible share cache hits.
- **Treat the prompt ordering as fragile.** The team has broken it before by putting an in-depth timestamp in the static system prompt, shuffling tool definitions non-deterministically, and updating tool parameters (such as which agents the Agent tool can call).
- **Send updates in messages instead of editing the system prompt.** When something goes stale, such as the time or a file the user changed, updating the prompt causes a cache miss that can be quite expensive; Claude Code instead adds a system-reminder tag to the next user message or tool result. The same goes for entering plan mode or changing the date.
- **Don't switch models mid-session; use a subagent to hand off.** Prompt caches are unique to models: 100k tokens into an Opus conversation, asking a fairly easy question of Haiku would cost more than letting Opus answer, because Haiku's cache must be rebuilt. If you need another model, deploy a subagent, for example one that has Opus prepare a hand-off message for the other model; Claude Code does this often with its Explore agents, which use Haiku.
- **Never add or remove tools mid-session; model state changes as tools.** The tool set is part of the cached prefix, so changing it invalidates the cache for the entire conversation, even though giving the model only the tools it needs right now seems intuitive. Plan mode keeps every tool in the request and makes EnterPlanMode and ExitPlanMode tools themselves, with a message explaining the mode when it is toggled; the model can then enter plan mode on its own without a cache break.
- **Defer tool loading instead of removing tools.** With dozens of MCP tools loaded, sending all of them is expensive and removing them mid-conversation breaks the cache. Send lightweight stubs (just the tool name, flagged to defer loading) that the model discovers through tool search; full schemas load only when selected, and the same stubs sit in the same order every time, so the prefix stays stable.
- **Make compaction and other forked work reuse the parent's exact prefix.** A separate summarization call with its own system prompt and no tools diverges from the cached prefix at the first token, so you pay the full uncached rate for the entire conversation, and the longer the conversation, the costlier the call. Cache-safe forking uses the same system prompt, user context, system context and tool definitions, prepends the parent's messages and appends the compaction prompt as a new user message, so only the compaction prompt is new; reserve a compaction buffer so there is room for that message and the summary output. The same applies to any side computation, such as summarization or skill execution.
- **Monitor the cache hit rate like uptime and treat cache breaks as incidents.** Claude Code runs alerts on its hit rate and declares SEVs when it is too low, because a few percentage points of miss rate can dramatically affect cost and latency.

## Perishable details
- API and harness mechanics named in the post: cache_control breakpoints (the API caches everything from the start of the request up to each breakpoint), the defer_loading flag with the tool search tool, compaction built into the API, the system-reminder tag convention, and the EnterPlanMode and ExitPlanMode tools.
- Claude Code's current layout of the cached prefix (global static system prompt and tools, per-project CLAUDE.md, per-session context), its use of Haiku for Explore agents, and the Opus-to-Haiku example depend on today's model-specific caches and pricing.

## Evidence
- None.

## Quotes
> "Prompt caching is a prefix match. Any change anywhere in the prefix invalidates everything after it. Design your entire system around this constraint."

> "The best way to do this is static content first, dynamic content last."

> "Changing the tool set in the middle of a conversation is one of the most common ways people break prompt caching."

> "Use tools to model state transitions (like plan mode) rather than changing the tool set. Defer tool loading instead of removing tools."

> "Fork operations need to share the parent's prefix. If you need to run a side computation (compaction, summarization, skill execution), use identical cache-safe parameters so you get cache hits on the parent's prefix."

> "Monitor your cache hit rate like you monitor uptime. We alert on cache breaks and treat them as incidents."

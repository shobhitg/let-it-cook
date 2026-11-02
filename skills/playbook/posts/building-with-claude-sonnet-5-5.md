---
title: Building with Claude Sonnet 5.5
url: https://claude.dev/blog/building-with-claude-sonnet-5-5/
published: 2026-09-28
author: Addy Osmani
category: Playbooks
topics: [delegation, verification, measurement]
---

# Building with Claude Sonnet 5.5

**Core idea:** Sonnet 5.5 is pitched as the default for well-scoped everyday work with a clear spec and a checkable result, with Opus 5.5 kept for complex, long-horizon work. The reusable lessons are about process (choose effort with evals, re-sweep when the model changes, drop old prompt workarounds, demand real checks); the rest of the post is specific to this release.

## Durable guidance
- **Use Sonnet for well-scoped work with a clear spec and a way to check the result, and Opus for complex work that needs careful judgment.** Sonnet 5.5 is listed for everyday coding (fixing bugs, quickly iterating on features, verifying against requirements), high-volume development, polished documents, slides and spreadsheets, and well-defined agent tasks you run repeatedly such as investigation, review and drafting. Opus 5.5 is listed for long-horizon agentic coding and knowledge work that needs careful judgment, and for the hardest problems.
- **Start at the default effort level, evaluate, and then pick the level your workload needs.** The Claude API defaults to `high` so you start from strong results.
- **Use the highest effort levels only where your evals show a quality gain.** At `xhigh` or `max`, Sonnet 5.5 thinks longer and costs more, and on some tasks you may lose what makes Sonnet useful, its balance of quality, speed and cost; in that case the post says to consider Opus 5.5.
- **Re-run your effort sweep when you change models.** Effort levels are recalibrated, so a level doesn't produce the same amount of thinking as it did on Sonnet 5 and your old setting won't carry over.
- **Remove prompt workarounds when you upgrade a model, and re-run your evals before tuning anything else.** Existing Sonnet 5 prompts should perform well without changes; workarounds such as refusal steering, tool-call retry shims or "do not be lazy" should come out.
- **Tell the agent that only a real check counts before it reports a change done.** Sonnet 5.5 generally checks its work, but at `low` effort it sometimes skips a check that exercises the change. If you see changes reported as done without test or build output, the prompting guide recommends a system-prompt paragraph that says to run the project's tests, type-checker, build or the changed command; that a syntax-only check, or a check command that failed to start, does not count; that missing declared dependencies are installed with the project's own package manager and lockfile, never via sudo or the system package manager, unless told not to; and that if no real check can run, the agent names the check it did not run and why instead of reporting the change as done.
- **Expect the bill to follow tokens per task, not the per-token price.** Sonnet 5.5's per-token price matches Sonnet 5's, but it typically needs far fewer tokens to do the same work, so the post says it costs up to 30% less for most work.

## Perishable details
- Model facts: ID `claude-sonnet-5-5` (`anthropic.claude-sonnet-5-5` on Amazon Bedrock); 1M-token context window; 128k max output (up to 300k on the Message Batches API with a beta header); knowledge cutoff June 2026; thinking on by default (adaptive); effort levels `low`, `medium`, `high`, `xhigh` and `max`; same tokenizer as Sonnet 5.
- Prices per million tokens (Sonnet 5.5 / Opus 5.5): input $2 / $4, output $10 / $20, cache write for 5 minutes $2.50 / $5, cache write for 1 hour $4 / $8, cache read $0.20 / $0.20. Sonnet 5.5 prices match Sonnet 5's; US-only inference costs 1.1 times the standard price; a 2000×1500 image costs about 2.5 times the tokens it did on Sonnet 4.6, Sonnet 4.5 or Haiku 4.5.
- Effort defaults and starting points: `high` on the Claude API and `medium` in Claude Code. Start with `high` unless the workload is agentic or latency-sensitive; for agentic coding and multistep tool use start at `medium` for well-specified tasks and move to `high` for harder or longer ones; for chat and other latency-sensitive work start at `medium` or `low`. Thinking counts toward `max_tokens`, so for agentic coding set it to 128,000 and stream. To get less thinking, lower the effort level, because asking in the system prompt to think less doesn't reliably reduce it.
- Breaking changes from Sonnet 5: `thinking: {"type": "disabled"}` and forced `tool_choice` (`any` or `tool`) return 400 errors (use `between_tools`, or `auto` plus `strict: true` tools); computer use works only through `computer_toolset_20260801`; a Sonnet 5.5 executor rejects Opus 4.8, Opus 4.7 and Sonnet 5 as advisors, and advice comes back encrypted; progress notes between tool calls come back as `thinking` blocks, so read content blocks by type rather than `content[0].text`. `between_tools` works only at `low`, `medium` and `high` effort, takes no other field and can't change effort mid-conversation. Thinking blocks are tied to the model and conversation, so keep conversations append-only. `/claude-api migrate this project to claude-sonnet-5-5` runs the migration in Claude Code.
- Prompt caching: the minimum cacheable prompt is 512 tokens (1,024 on Sonnet 5); a cache read costs a tenth of the input price; changing the top-level effort between requests invalidates the cache, and per-message effort (beta) keeps it.
- Reasoning and refusals: don't ask the model to write out its reasoning in the response, because that invites `reasoning_extraction` declines; read summarized thinking instead (`display: "summarized"`, or `"updates"` in beta). A declined request returns HTTP 200 with `stop_reason: "refusal"` and one of five `stop_details` categories; server-side fallback (beta) retries only `cyber` and `frontier_llm` declines on Sonnet 5. Sonnet 5.5 is the first Sonnet with cybersecurity safeguards similar to those on the most capable models.
- Claude Code: from v2.1.284 the `sonnet` alias resolves to Sonnet 5.5 on the Claude API, at `medium` effort with the 1M window; thinking can't be turned off and there is no fast mode; the `default` model stays Opus 5.5, so switch with `/model sonnet` for well-scoped tasks.
- Availability: the Claude API, Amazon Bedrock, Claude Platform on AWS, Google Cloud and Microsoft Foundry (Global Standard deployments only).

## Evidence
- Sonnet 5.5 is described as 30% faster than Sonnet 5 and, at an unchanged per-token price, as costing up to 30% less for most work because it typically needs far fewer tokens for the same work (vendor claims; the post gives no method or task set).
- Epic Games (Daniel Vogel, COO), in early testing: Sonnet 5.5 cleared the same quality bar expected of a higher-tier model on a system design audit and a data-flow review, managed tens of thousands of lines of code for gameplay system architecture, handled multi-hour tasks and needed less prescriptive prompting (a customer testimonial, no numbers).
- On Anthropic's automated behavioral audit, Sonnet 5.5 improves on or matches Sonnet 5 on most measures of alignment and honesty (no scores given).
- A code-to-painting demo by Lance Martin shows Sonnet 5, Sonnet 5.5 and Opus 5.5 each writing code that repaints the same photograph; the text gives no scores.

## Quotes
> "Sonnet 5.5 fits best when the task has a clear spec and a way to check the result."

> "Start there, evaluate, and then pick the effort level your workload needs."

> "Use `xhigh` or `max` only where your evals show a quality gain."

> "Effort levels are recalibrated, so a level doesn't produce the same amount of thinking as it did on Sonnet 5, and your old setting won't carry over."

> "If your prompts carry workarounds such as refusal steering, tool-call retry shims, or "do not be lazy," remove them and re-run your evals before tuning anything else."

> "Sonnet 5.5 generally checks its work before reporting a change as done, but at `low` effort it sometimes skips a check that exercises the change."

> "While the per-token price doesn't change, the overall bill will change because, as previously mentioned, Sonnet 5.5 typically uses fewer tokens per task than Sonnet 5."

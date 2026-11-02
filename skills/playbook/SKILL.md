---
name: playbook
description: Use when deciding how a software team should work, especially once AI agents write much of the code. Covers how changes get reviewed, approved, merged and rolled out; how to test or verify work, including evals, golden datasets and LLM graders; how to write tasks, CLAUDE.md or REVIEW.md for agents and pick effort or session type; how to run agents unattended or on a schedule; how to design an agent's tools and context; and how to measure engineering cost and quality. Also use when asked how Anthropic or the Claude Code team does any of these.
---

# claude.dev-first engineering playbook

Anthropic's teams publish how they build software with agents on [claude.dev](https://claude.dev/blog/). This skill carries that guidance, digested post by post. **Current through 2026-10-15 (16 posts).**

## How to answer

1. Find the question's topic in the table below and read that reference file before answering. Open a post's digest in `posts/` when you need its details or exact words.
2. Shape the answer like this:
   - **What Anthropic's teams do:** the guidance that applies, each point linked to its post as `https://claude.dev/blog/<slug>/`.
   - **Beyond claude.dev:** anything the posts don't cover, answered from general practice and labeled as such. Leave this part out when the posts cover the whole question.
3. Quote only from the digests in `posts/`, never from memory.
4. A digest's "Perishable details" (model names, prices, effort defaults) hold only for the model or version they name. Check what's current before repeating one.
5. If the user asks for the newest guidance, or the question concerns something after the date above, read <https://claude.dev/rss.xml> and any post newer than that date before answering.

## Topics

| The question is about | Read |
|---|---|
| Code review, approvals, merging, flags, rollout, rollback, who owns a change | [references/shipping.md](references/shipping.md) |
| Tests, evals, golden cases, graders, benchmarks, CI gates, agents checking their own work | [references/verification.md](references/verification.md) |
| Handing work to agents: task specs, CLAUDE.md, effort, model choice, local or cloud sessions, subagents, skills, output formats | [references/delegation.md](references/delegation.md) |
| Agents running unattended or on a schedule: state between runs, credentials, budgets, guardrails | [references/automation.md](references/automation.md) |
| Building agents: tools, context, prompt caching, workflows | [references/agent-design.md](references/agent-design.md) |
| Cost per task, human time per change, reverts, incidents | [references/measurement.md](references/measurement.md) |

## Core rules

1. **Name the finish line and the check that proves it, then let it cook.** ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/), [Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))
2. **No claim without evidence.** Agents run real checks and show the output before a person looks, and a different agent does the verifying. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/), [Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/))
3. **Ask which check should catch a problem, not whether a human read the code.** Human approvals scale with risk, the change sets the tier, and an agent's approval never counts as a person's. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
4. **Judge the system by human time per change, with reverts and incidents as the guardrail.** ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
5. **Golden cases come from reality, and two experts would agree on each verdict.** Turn incidents into eval cases, and read graded transcripts before trusting a grader. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/), [Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
6. **Trust only gains that beat the noise on cases the tuner never saw.** ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
7. **Give agents a number to beat that is proven to track the real outcome, and ratchet every win in CI.** ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))
8. **Make mistakes cheap to undo**: a merge queue, short-lived flags, staged rollout, fast rollback, and a named owner for every change. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/), [claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))
9. **Unattended agents fail loudly**: a failed read is never a quiet day, and nothing counts as done until the destination confirms it. ([Agent automations](https://claude.dev/blog/building-effective-agent-automations/))
10. **Keep context lean and let the agent find the rest; delete rules as models improve.** ([Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/), [Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))
11. **Pay for finished tasks, not tokens**: a check is cheaper than more effort, and a retry costs more than any saving. ([Task cost](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/))

## Sources

| Published | Post |
|---|---|
| 2026-10-15 | [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) |
| 2026-10-08 | [Building effective agent automations](https://claude.dev/blog/building-effective-agent-automations/) |
| 2026-10-06 | [Claude Code in the cloud: a field guide to cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/) |
| 2026-10-01 | [Getting started with Claude Code mods](https://claude.dev/blog/getting-started-with-claude-code-mods/) |
| 2026-09-28 | [Building with Claude Sonnet 5.5](https://claude.dev/blog/building-with-claude-sonnet-5-5/) |
| 2026-09-28 | [Automating eval design and hillclimbing with Claude](https://claude.dev/blog/automating-eval-design-and-hillclimbing/) |
| 2026-09-25 | [What a task costs on Opus 5.5](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/) |
| 2026-09-25 | [Using Claude Code: Spending your effort](https://claude.dev/blog/spending-your-effort/) |
| 2026-09-23 | [How we made claude.ai 3x faster in two weeks](https://claude.dev/blog/how-we-made-claude-ai-faster/) |
| 2026-09-22 | [Getting the most out of Opus 5.5 in Claude and Claude Code](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/) |
| 2026-07-24 | [The new rules of context engineering for Claude 5 generation models](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/) |
| 2026-06-03 | [Lessons from building Claude Code: How we use skills](https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/) |
| 2026-06-02 | [A harness for every task: dynamic workflows in Claude Code](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/) |
| 2026-05-20 | [Using Claude Code: The unreasonable effectiveness of HTML](https://claude.dev/blog/using-claude-code-the-unreasonable-effectiveness-of-html/) |
| 2026-04-30 | [Lessons from building Claude Code: Prompt caching is everything](https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/) |
| 2026-04-10 | [Seeing like an agent: how we design tools in Claude Code](https://claude.dev/blog/seeing-like-an-agent/) |

# Agent design: tools, context, caching, harnesses

What Anthropic's teams do when building agents such as Claude Code, from claude.dev. Every rule links to its post; the digests in `../posts/` hold details and exact quotes.

## Tools

- **Shape tools to the model's abilities, and learn those abilities by reading its outputs.** ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))

> "You want to give it tools that are shaped to its own abilities."

- **Keep a high bar for adding a tool.** Claude Code has about 20 and the team keeps asking whether it needs them all. ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))

> "The bar to add a new tool is high, because this gives the model one more option to think about."

- **Ask for structured output through a tool, not a text format**; a markdown format worked usually but not reliably. Don't make one tool ask for two things at once, and check that the model understands how to call each tool. ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))
- **Design the interface instead of adding examples**: with the newest models, examples narrow what the model explores, while an expressive parameter (an enum of statuses) plus one instruction defines the behavior. Put usage instructions once, in the tool description. ([Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/))
- **Revisit tools as models improve, and retire the ones that now constrain the model.** ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))

> "As model capabilities increase, the tools that your models once needed might now be constraining them. It’s important to constantly revisit previous assumptions on what tools are needed."

## Context

- **Let the agent find its own context.** Claude Code moved from handing Claude retrieved snippets to letting it search the codebase itself. ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))
- **Add capability through progressive disclosure instead of new tools**: skills that reference other files, and deferred tools whose full definitions load only when searched for. ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/), [Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/))

> "Progressive disclosure is now a common technique we use to add new functionality without adding a tool."

- **Put a subagent between the main agent and bulky reference material.** It searches in its own context and returns only the answer. Keep rarely needed knowledge out of the system prompt. ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))

> "The subagent does the doc-searching in its own context, follows detailed instructions on how to search and what to extract, and hands back only the answer. The main agent's context stays clean."

- **Delete constraints the model no longer needs, and simplify as models improve.** If you build your own harness, spend your effort on the system prompt, which carries the product context. ([Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/))

## Prompt caching

- **Design the whole harness around caching from day one.** ([Prompt caching](https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/))

> "Prompt caching is a prefix match. Any change anywhere in the prefix invalidates everything after it. Design your entire system around this constraint."

- **Put static content first and dynamic content last**, and send updates (time, changed files, mode switches) in messages rather than by editing the system prompt. ([Prompt caching](https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/))
- **Never change the model or the tool set mid-session.** Hand off to another model through a subagent; model state changes such as plan mode as tools; defer tool loading instead of removing tools. ([Prompt caching](https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/))

> "Use tools to model state transitions (like plan mode) rather than changing the tool set. Defer tool loading instead of removing tools."

- **Make compaction and other side computations reuse the parent's exact prefix**, and monitor the hit rate like uptime. ([Prompt caching](https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/))

## Multi-agent harnesses

- **Give long, parallel, structured or adversarial work separate contexts.** A single context suffers agentic laziness (declaring done after partial progress), self-preferential bias (favoring its own results) and goal drift (losing the objective across compactions). ([Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/))

> "Creating a workflow helps combat these by orchestrating separate Claude subagents with their own context windows and focused, isolated goals."

- **Patterns that work**: an adversarial verifier per output; independent root-cause hypotheses from disjoint evidence, each facing verifiers and refuters; pairwise tournaments for ranking; one verifier per rule plus a skeptic; migrations as many small isolated fixes in worktrees with adversarial review; a classifier agent that routes each task to a model; loops that run until a stop condition such as "no new findings". ([Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/))
- **Quarantine agents that read untrusted content** from high-privilege actions. ([Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/))

> "A useful pattern for triage workflows is quarantine. This involves barring the agents that read untrusted public content from taking high-privilege actions, which are instead done by the agents in charge of acting on the information."

- **Reserve workflows for complex, high-value tasks and cap their tokens**; parallelism and specialization have to earn their coordination cost. ([Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/))

For agents that run unattended, see [automation.md](automation.md); for packaging know-how as skills, see [delegation.md](delegation.md).

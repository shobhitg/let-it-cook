---
title: "A harness for every task: dynamic workflows in Claude Code"
url: https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/
published: 2026-06-02
author: Thariq Shihipar and Sid Bidasaria
category: Agents
topics: [agent-design, verification, delegation, automation]
---

# A harness for every task: dynamic workflows in Claude Code

**Core idea:** On long, parallel or adversarial tasks a single context window tends to quit early, drift from the goal and favor its own results, so Claude can write a task-specific harness that spawns subagents with their own contexts and combines patterns such as fan-out, adversarial verification, tournaments and quarantine. The authors say this costs more tokens and belongs on complex, high-value tasks.

## Durable guidance
- **Split long-running, massively parallel, highly structured or adversarial work across separate subagents, each with its own context window and a focused goal.** The default harness plans and executes in one context window, and the longer it works on a complex task the more it suffers three failure modes. Agentic laziness is stopping after partial progress and declaring the job done, such as 35 of 50 items. Self-preferential bias is favoring its own results when asked to verify or judge them. Goal drift is losing fidelity to the original objective across many turns, especially after compaction, because each summarization step is lossy. For many small steps, give each its own clean context so they don't cross-contaminate, then merge the structured outputs in a final synthesize step.
- **Verify with a separate agent, not the one that did the work.** For each spawned agent, run another agent to adversarially check its output against a rubric or criteria. To check a report, have one agent identify every factual claim and spin off a subagent to check each in detail, optionally with another agent auditing the quality of each source.
- **Investigate root causes from independent hypotheses built on disjoint evidence.** Debugging works best with several independent hypotheses, but a single context window can run into self-preferential bias. Separate agents for logs, files and data generate the hypotheses, and each one faces a panel of verifiers and refuters. The post says this works beyond code, for example sales drops, pipeline failures and post-mortems.
- **Sort or rank large lists with pairwise tournaments, not one prompt.** Sorting 1000+ rows in one prompt degrades quality and won't fit in context. Run a tournament of pairwise-comparison agents (comparative judgment is more reliable than absolute scoring), or bucket-rank in parallel and then merge. Each comparison is its own agent, so only the running order stays in context.
- **Check rules with one verifier per rule, then filter the flags with a skeptic.** For rules Claude misses even when they are in CLAUDE.md, run one verifier per rule in a clean context, plus a skeptic persona subagent to avoid too many false positives. In reverse, mine recent sessions and code review comments for corrections you keep making, cluster them with parallel agents, adversarially check each candidate (would this rule have prevented a real mistake?), and distill the survivors into CLAUDE.md.
- **Run migrations and refactors as many small, isolated fixes.** Break the task into units such as callsites, failing tests or modules, spin off a subagent per fix in a worktree, have another agent adversarially review, then merge. Consider telling agents not to use resource-intensive commands so you can parallelize without running out of resources on your machine.
- **Quarantine agents that read untrusted content.** In a triage workflow (classify each item, dedupe against what is already tracked, then attempt a fix or escalate to a human), bar the agents that read untrusted public content from high-privilege actions. Those actions are done by the agents in charge of acting, which only see the readers' summaries.
- **Give a review agent a rubric for taste-based work and for lightweight evals.** For design or naming, have agents explore many solutions and let a review agent holding a rubric decide when the criteria are met, or pick by tournament on the rubric. For lightweight evals, run agents in separate worktrees and have comparison agents grade the outputs against a rubric, for example to evaluate and refine a skill.
- **Route each task to a model with a classifier agent.** When a task involves many tool calls, a classifier tuned to your tasks can do the research first and choose the model. For example, for "explain how the auth module works" the classifier checks how many files the auth module has and the shape of the codebase, then routes to a model by the task's expected complexity.
- **When the amount of work is unknown, loop until a stop condition is met instead of running a fixed number of passes.** Example stop conditions are no new findings, or no more errors in the logs.
- **Reserve workflows for complex, high-value tasks and cap their token use.** Dynamic workflows often use more tokens. For regular coding tasks, ask whether the task really needs more compute, since most do not need a panel of 5 reviewers. The same logic applies to multi-agent versus single-agent architecture: parallelism and specialization have to earn their coordination cost. An explicit token budget, such as prompting "use 10k tokens", sets a cap.

## Perishable details
- Dynamic workflows were released the week before this post (late May 2026). A workflow is a JavaScript file that spawns and coordinates subagents with `agent()`, `parallel()` and `pipeline()` plus standard JSON, Math and Array functions. It can choose each agent's model and whether it runs in its own worktree, and an interrupted workflow resumes when the session is resumed.
- Controls named in the post: pair repeatable workflows (triage, research, verification) with `/loop` for regular intervals and `/goal` for a hard completion requirement; set a token budget by prompting for one; save a workflow by checking it into `~/.claude/workflows` or sharing it through a skill, and prompt Claude to treat a skill's workflow as a template rather than a script to run verbatim; the `/deep-research` skill is built on workflows.
- The claim that Claude can now write a harness tailored to the task, where static `claude -p` or Agent SDK harnesses must handle every edge case and so end up generic, is tied to "Claude Opus 4.8 and dynamic workflows."
- The authors say best practices are still developing and that workflows currently use significantly more tokens.
- The routing example names Sonnet and Opus, and the migration example is Bun's rewrite from Zig to Rust.

## Evidence
- Bun was rewritten from Zig to Rust using workflows. The post cites this as a use case and links to a thread and a write-up on million-line migrations, with no figures.
- No benchmarks or measured comparisons. The figures in the text are illustrations or claims: an agent stopping at 35 of 50 security-review items; sorting 1000+ rows in one prompt degrading and not fitting in context; a panel of 5 reviewers being unnecessary for most ordinary coding tasks.

## Quotes
> "Agentic laziness refers to when Claude stops before finishing a particularly complex, multi-part task and declares the job done after partial progress, for example addressing 35 of the 50 items in a security review."

> "Self-preferential bias refers to Claude’s tendency to prefer its own results or findings, especially when asked to verify or judge them against a rubric."

> "Creating a workflow helps combat these by orchestrating separate Claude subagents with their own context windows and focused, isolated goals."

> "For each spawned agent, run a separate spawned agent to adversarially verify its output against a rubric or criteria."

> "Instead run a tournament, a pipeline of pairwise-comparison agents (comparative judgment is more reliable than absolute scoring), or bucket-rank in parallel then merge."

> "A useful pattern for triage workflows is quarantine. This involves barring the agents that read untrusted public content from taking high-privilege actions, which are instead done by the agents in charge of acting on the information."

> "For tasks with an unknown amount of work, loop spawning agents until a stop condition is met (no new findings, or no more errors in the logs) instead of a fixed number of passes."

> "For regular coding tasks, try and ask yourself: does it really need more compute? For example, most traditional coding tasks do not need a panel of 5 reviewers."

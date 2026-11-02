---
title: "Seeing like an agent: how we design tools in Claude Code"
url: https://claude.dev/blog/seeing-like-an-agent/
published: 2026-04-10
author: Thariq Shihipar
category: Agents
topics: [agent-design, delegation]
---

# Seeing like an agent: how we design tools in Claude Code

**Core idea:** Design an agent's tools from the model's point of view: fit them to what the model can actually do, which you learn by reading its outputs, keep the set small, retire tools as the model outgrows them, and let the agent find its own context rather than feeding it. Bulky lookups go to a subagent so the main context stays clean.

## Durable guidance
- **Shape the agent's tools to its abilities, and learn those abilities by reading its outputs and experimenting.** The post's analogy is a hard math problem: paper, a calculator or a computer help only as far as you know how to use them, so the tools should match the model's skills, and you find those out by paying attention.
- **Keep the bar for adding a tool high.** Each added tool gives the model one more option to think about. Claude Code has about 20 tools and the team frequently revisits whether it needs all of them.
- **Ask for structured output through a tool, not through a text format.** Asking Claude to emit a slightly modified markdown format for questions usually worked but not reliably: it appended extra sentences, dropped options or abandoned the structure. A tool Claude can call at any point (AskUserQuestion), which shows a modal and blocks the loop until the user answers, gave structured output and made sure the user got multiple options. It could also be composed, for example called from the Agent SDK or referenced in skills.
- **Don't have one tool ask the model for two things at once.** Adding an array of questions to the plan-exit tool confused Claude, because it was asked for a plan and for questions about the plan at once. What if the user's answers conflicted with the plan, and would Claude have to call the tool twice?
- **Check that the model understands how to call a tool.** Even the best designed tool doesn't work if Claude doesn't understand how to call it. For AskUserQuestion, the post counts it as most important that Claude seemed to like calling the tool and that its outputs worked well.
- **Revisit your tools as models improve, and drop the ones that now constrain the model.** Early on, a todo tool plus a system reminder every 5 turns kept Claude on track. As models improved, the reminders made Claude think it had to stick to the list instead of changing course, and the team asked how subagents could coordinate on a shared todo list. The Task tool replaced it: tasks help agents communicate, and can carry dependencies, share updates across subagents and be altered or deleted by the model.
- **Support a small set of models with similar capability profiles.** That makes it easier to keep revisiting which tools the models still need.
- **Let the agent find its own context instead of handing it context.** The first approach was RAG: a pre-indexed vector database whose snippets the harness handed to Claude before each response. It was powerful and fast, but needed indexing and setup, could be fragile across environments and, most importantly, gave Claude context instead of letting it find the context itself. A Grep tool let Claude search the codebase and build context on its own, and the post says Claude gets increasingly good at building its context as it gets smarter, when given the right tools.
- **Use progressive disclosure to add new functionality without adding a tool.** With Agent Skills, Claude reads a skill file that references other files, which it can read recursively; a common use is teaching Claude to use an API or query a database. Over a year Claude went from not really being able to build its own context to nested search across several layers of files.
- **Keep rarely needed knowledge out of the system prompt.** Information on how to use Claude Code could have gone there, but users rarely asked about it, so it would have added context rot and interfered with the main job of writing code.
- **Put a subagent between the main agent and bulky reference material.** Giving Claude a link to its docs worked, but it pulled large chunks of documentation into context to find an answer the user could have had in one sentence. The Claude Code Guide subagent searches the docs in its own context, follows detailed instructions on how to search and what to extract, and hands back only the answer. It isn't perfect: Claude can still get confused when asked how to set itself up.
- **Treat tool design as an art: experiment often, read your outputs, try new things.** What works depends heavily on the model you're using, the goal of the agent and the environment it operates in.

## Perishable details
- Tool inventory as of April 2026: Claude Code has about 20 tools, and the team keeps asking whether each is needed.
- The todo tool (with its reminder every 5 turns) was replaced by the Task tool; the shift was driven by models finding todo lists limiting and by Opus 4.5 getting much better at using subagents.
- AskUserQuestion (a modal that blocks the loop, particularly prompted in plan mode) is the current form of elicitation, and the authors doubt it is final.
- The Claude Code Guide subagent is the current answer for questions about Claude Code itself, and the authors call it imperfect.
- The RAG-to-Grep story and the year-long gain in nested search describe model capability at the time; the post says tool design "depends heavily on the model you're using".

## Evidence
- The post reports no benchmarks or measured rates; its evidence is the team's account of what they tried and what Claude did.
- Markdown question format: Claude "could usually produce this format, but not reliably", appending extra sentences, dropping options or abandoning the structure.
- Questions parameter on the plan-exit tool: abandoned because it confused Claude; no failure rate is given.
- AskUserQuestion tool: shipped; Claude seemed to like calling it and its outputs worked well (qualitative).
- Over the course of a year, Claude went from not really being able to build its own context to nested search across several layers of files.
- Claude Code has about 20 tools, and the todo reminder ran every 5 turns.

## Quotes
> "You want to give it tools that are shaped to its own abilities."

> "The bar to add a new tool is high, because this gives the model one more option to think about."

> "As model capabilities increase, the tools that your models once needed might now be constraining them. It’s important to constantly revisit previous assumptions on what tools are needed."

> "Most importantly, Claude was given this context instead of finding the context itself."

> "Progressive disclosure is now a common technique we use to add new functionality without adding a tool."

> "Claude could usually produce this format, but not reliably. It would append extra sentences, drop options, or abandon the structure altogether."

> "The subagent does the doc-searching in its own context, follows detailed instructions on how to search and what to extract, and hands back only the answer. The main agent's context stays clean."

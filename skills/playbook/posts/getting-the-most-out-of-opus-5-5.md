---
title: Getting the most out of Opus 5.5 in Claude and Claude Code
url: https://claude.dev/blog/getting-the-most-out-of-opus-5-5/
published: 2026-09-22
author: Addy Osmani
category: Playbooks
topics: [delegation, verification, shipping]
---

# Getting the most out of Opus 5.5 in Claude and Claude Code

**Core idea:** A playbook for steering long Claude Code runs: give the whole task with a finish line, write the stop-and-ask rules into CLAUDE.md, fan big audits out to subagents whose evidence gets checked, keep the task list in a file, and read what the run needs from you first. A good share of the advice (thinking lines, safeguards, fast mode, Claude apps tips) is tied to the model release the post covers and will date.

## Durable guidance
- **Give the whole task in one message, say what "done" looks like and when to stop and ask, then let it work.** Name a finish line such as "the tests pass" or "every endpoint is migrated." With a clear finish line, the agent knows when it's done. The post's example prompt adds a stop condition: ask only if a test fails for a reason it can't explain.
- **Write down in CLAUDE.md when to keep going and when to stop and ask.** The post says the model sometimes stops to report instead of continuing: a summary that names the next step without taking it, an offer to continue, or a list of choices that don't block the work. It follows instructions that name these stops, so name the ones you want. The post's rule: keep going when a step doesn't need your input, put status notes in the same message as the next action, and stop only when it can't continue without you or before anything destructive. For pair programming, say the opposite instead: a one-line plan before it starts and a short recap at the end.
- **Keep your own check before anything risky or hard to undo.** A rule to keep going means fewer stops, so the post's rule ends with a stop before destructive actions (deleting data, force-pushing, changing anything outside the repository). Keep permission prompts on for destructive commands too.
- **Split big audits, migrations and reviews across subagents, and tell it to check each subagent's evidence before accepting the result.** The post's prompt gives each service to its own subagent and finishes with one table of service, affected yes or no, and the evidence.
- **Keep the task list in a file and read the file, not the scrollback.** A long run fills the context window and Claude Code then summarizes older turns. A list in a file survives that and shows at a glance what's done and what's left. The post's prompt: keep a checklist in TASKS.md, tick each item when done, and add anything new it finds.
- **When a long run ends, read what it needs from you first.** Look first for anything the agent is waiting on you for, such as a decision left open or a change it wants approved, then read the rest of the summary. To change the summary's format, say so in CLAUDE.md, for example "End every run with three headings: Blocked on me, Changed, Found."
- **Have the model review a diff or pull request before a person does.** The post's prompt asks it to list only problems it would block the merge for, each with the file and line, why it's wrong, and how to show it fails. The post's support is one early tester's comparison (see Evidence) and that the model explains its changes in plain language, so its pull request descriptions are easier to review.
- **For research and analysis, ask it to mark what it couldn't confirm and say where it looked.** "I couldn't find this" is worth reading, and asking for it makes it easy to find. For checking a long document, the post asks the model to quote each problem and say where it is.
- **For design work, name the specific patterns to leave out rather than giving a general instruction.** A general instruction like "avoid a generic look" mostly swaps one default for another, while a list of specific patterns works much better. Look at what it chose instead, add what you dislike to the list, and ask again.

## Perishable details
- Thinking: Opus 5.5 thinks before every reply and decides how much, so the post says to delete "think carefully" and "think step by step" lines from prompts and saved instructions, say "Answer directly" for a quick answer, and change effort in Claude Code to change how much it thinks.
- Comparisons with Opus 5 that will date: it keeps going on long multi-part work better, reports more clearly, reads charts and screenshots more accurately, pays more attention to detail, and makes spreadsheets and documents that need less editing.
- Observed Opus 5.5 behaviors behind some tips: it sometimes stops to report on long tasks, falls back on a few default design styles, and in long chats sometimes goes back over an earlier answer while thinking about a short follow-up. The post's fix for the last one is a project instruction to treat answered questions as settled, which it says to leave out of long-analysis projects.
- Safeguards: Opus 5.5 is the first Opus model to launch with Fable-level bio and cyber safeguards. In Claude apps and Claude Code most flagged messages move to an older model and the work goes on there. You can switch back, edit and retry, choose to be asked first, or report a wrong flag. The check covers everything in the conversation, including files and search results, and the authors say legitimate work can sometimes be flagged and they are tuning the safeguards. Requests to reproduce its internal reasoning in the reply can be declined (a flag category), so ask for an explanation instead, such as "Explain why you chose this approach in three sentences."
- Product features: add to a running task by typing a follow-up and pressing Enter while Claude works, since a restart costs more on longer runs. `/fast` was a research preview at launch for back-and-forth work where you read each reply before sending the next message; it gives the same model with text arriving sooner, needs extra usage turned on, and costs more per token than standard mode.
- Claude apps tips tied to Opus 5.5 strengths: attach the chart or screenshot instead of retyping numbers, ask for the finished spreadsheet or document rather than an outline, and ask it to check a long deck or plan for contradictions.

## Evidence
- Early testers had Opus 5.5 run long coding tasks for hours with little oversight, and coordinate parallel subagents on long audits and migrations with little oversight (testers' reports; no figures given).
- One early tester said Opus 5.5 at its lowest effort caught more bugs than Opus 5 at high effort, with fewer false alarms (code review; a single anecdote).
- In the authors' testing in a chat product, removing a "think carefully" line made replies start sooner with no clear drop in quality (reply latency; qualitative).
- In the authors' testing, Opus 5.5 caught a date that fell on the wrong weekday in a long planning thread and a chart that didn't match the numbers in a deck (attention to detail; two examples).
- The post says Opus 5.5's biggest gains over prior Opus models are on multi-step work, such as carrying a change through a large repository until the tests pass; it gives no benchmark numbers.

## Quotes
> "With a clear finish line, it knows when it’s done."

> "Stop and ask only when you can't continue without me, or before anything destructive: deleting data, force-pushing, or changing anything outside this repository."

> "A rule to keep going means fewer stops, so keep your own check before anything risky or hard to undo."

> "Give each service to its own subagent. When a subagent reports back, check its evidence before you accept it."

> "A long run fills the context window, and Claude Code then summarizes older turns. A list in a file survives that, and it shows you at a glance what’s done and what’s left."

> "When a long run ends, look first for anything Claude is waiting on you for, like a decision it left open or a change it wants you to approve."

> "List only problems you'd block the merge for. For each one, give the file and line, why it's wrong, and how to show it fails."

> "Mark anything you couldn’t confirm, and say where you looked"

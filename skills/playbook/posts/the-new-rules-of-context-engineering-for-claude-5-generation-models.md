---
title: The new rules of context engineering for Claude 5 generation models
url: https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/
published: 2026-07-24
author: Thariq Shihipar
category: Engineering
topics: [delegation, agent-design, verification]
---

# The new rules of context engineering for Claude 5 generation models

**Core idea:** Context that older models needed as guardrails (strict rules, examples, repeated instructions, everything upfront) now over-constrains newer ones, so Anthropic removed over 80% of Claude Code's system prompt with no measurable loss on its coding evaluations. Keep the context you hand an agent lean: judgement over rules, expressive interfaces over examples, progressive disclosure, and rich references in code.

## Durable guidance
- **Delete rules that over-constrain the model and let it use surrounding context and judgement.** The team found it was overconstraining Claude Code through its system prompt, CLAUDE.md files and skills; transcripts showed conflicting messages in one request (for example "leave documentation as appropriate" next to "DO NOT add comments") that the model had to think harder to reconcile. The constraints were once needed to avoid worst cases but can be wrong for a subset of prompts, and many can now be deleted: a default-to-no-comments rule became one line telling the model to match the surrounding code's comment density, naming and idiom.
- **Design the tool interface instead of adding examples.** With the newest models, examples constrain them to a certain exploration space. Ask what parameters the model has and how they can be more expressive: in the Todo tool, listing status as an enumeration of pending, in_progress and completed hints at how to use it, and one instruction (keep one item in_progress) defines the requested behavior.
- **Load context progressively instead of putting it all upfront.** Verification and code review moved out of the system prompt into skills the agent calls selectively, and some tools are deferred so the agent must search for their full definitions before using them, which allows more tools that take no context until needed. Don't make CLAUDE.md and skill files a central repository for every known practice; use a tree of files that load at the right time.
- **Put tool-usage instructions in the tool description, once.** Earlier models sometimes needed repeated instructions or listened more to the end of their context, so the system prompt repeated what the tool descriptions said; the team deleted the repeats and kept the instructions in the tool descriptions.
- **Give rich references, preferably in code, rather than simple prose specs.** Code is high-fidelity instruction in a language the model knows well: a spec can be a detailed test suite or a function in another codebase to port, and an HTML mockup generally produces better results than a description of the design or a screenshot. Files can be @-mentioned as references: specs, mockups, even entire codebases.
- **Write rubrics so verifier agents can check your taste.** Rubrics let the model try to verify taste in a field (such as what good API design looks like) by using dynamic workflows and spinning up verifier agents with those rubrics.
- **Keep CLAUDE.md lightweight and spend its tokens on gotchas.** Say briefly what the repo is for, then record non-obvious facts about the codebase (for example, that types live in one monolithic file and nowhere else), and skip the obvious things the model can learn from the file system. If you have several unique instructions for verifying work, create a verification skill and reference it from CLAUDE.md.
- **Write skills as lightweight guides that encode your own opinions.** Avoid over-constraining them except in highly important areas, split long skills into many files for progressive disclosure, and put in the knowledge and best practices particular to you, your team or your product.
- **Spend your time on the system prompt if you build your own harness.** It is heavily tied to the product context, telling the model what product it is in and what it is doing; Claude Code users will likely never modify it.
- **Simplify your system prompt, skills and CLAUDE.md as models improve.** The team's own result is the evidence: over 80% of Claude Code's system prompt removed for Claude Opus 5 and Claude Fable 5 with no measurable loss on its coding evaluations; the post says you may need to simplify just like they did.

## Perishable details
- The advice is calibrated to the Claude 5 generation (the post names Claude Opus 5 and Claude Fable 5): it says older models needed strong rules, repeated instructions and examples, and that without those guardrails their comments would have been wrong in many cases. Expect the balance to keep shifting with each model generation.
- Memory and artifacts: the # hotkey that wrote to CLAUDE.md has given way to automatic memory, and HTML artifacts can replace markdown plan files as references; the post notes that memory, artifacts and skills are new ways to load and share context across sessions.
- The claude doctor command (/doctor in Claude Code) packages these practices to rightsize skills and CLAUDE.md files; ToolSearch-based deferred loading and the Todo tool are the examples used.

## Evidence
- Over 80% of Claude Code's system prompt removed for models like Claude Opus 5 and Claude Fable 5, with no measurable loss on Anthropic's coding evaluations (what the removal cost in quality).
- Reading transcripts of internal Claude Code usage turned up conflicting messages within a single request, for example "leave documentation as appropriate" alongside "DO NOT add comments"; the post gives no counts.

## Quotes
> "We removed over 80% of Claude Code’s system prompt for models like Claude Opus 5 and Claude Fable 5 with no measurable loss on our coding evaluations."

> "And while these constraints were once needed to avoid worst case scenarios, we have since found we can delete many of them and let the model use surrounding context and judgement instead."

> "With our newest models, we’ve found that giving examples actually constrains them to a certain exploration space."

> "A common myth is that you want to make these a central repository for every known practice that you might run into, because Claude would not find it otherwise. Instead, consider having a tree of files that can be loaded at the right time."

> "Keep your CLAUDE.md lightweight and briefly describe what your repo is for, but spend most of the tokens on gotchas inside of the codebase."

> "Generally you should prefer files that are in code as it provides clear, high-fidelity instructions to Claude in a language it knows very well."

> "Rubrics allow Claude to try and verify your taste in a particular field (e.g. what does a good API design look like) by using dynamic workflows and spinning up verifier agents with those rubrics."

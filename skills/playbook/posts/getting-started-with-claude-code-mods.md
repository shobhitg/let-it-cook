---
title: Getting started with Claude Code mods
url: https://claude.dev/blog/getting-started-with-claude-code-mods/
published: 2026-10-01
author: Addy Osmani
category: Tutorials
topics: [delegation, automation]
---

# Getting started with Claude Code mods

**Core idea:** A mod is a small plugin that can watch, rewrite or refuse what Claude Code does and draw its own interface, so a team can shape the tool around its own habits, and Claude can write one from a plain description of what you want to see. The post builds a context-window readout and tours a pre-run guard for destructive commands and a step-through of the last turn's edits, warning that such a guard is a safety net rather than a permission system.

## Durable guidance
- **Start each customization from one concrete question you keep asking.** The post's three mods each came from one question: how full is my context, what is this command about to delete, and what did Claude just change. It pitches mods as a way to fit Claude Code to how you work: a readout you check all the time, a guard in front of commands that make you nervous, a review view for how you like to read changes. Other starting points it lists: a cost or rate-limit meter, a prompt hook that adds your team's conventions to every prompt, a pane of the files Claude has read this session, a toast when a long turn finishes, and a tool-call guard tuned to your stack, such as production kubectl contexts or `terraform apply`.
- **Describe what you want to see and let Claude write the mod.** Claude Code knows how to write mods, and the post's shortcut prompt only says what the mod should show, so you don't need to know the API. With hot reload on you can keep asking for tweaks ("make Storm start at 70%", "add the dollar cost at the end") and watch them land.
- **Hold risky commands and show what they would change before they run.** Blast Radius catches `rm -rf`, `git reset --hard`, `git clean`, force pushes and database migrations. It builds its report from the tools' own dry-run commands (`git status --porcelain`, `git clean -n`, `git log HEAD..origin/main`, `showmigrations`), then offers Proceed or Cancel; Cancel gives Claude a refusal with the reason. Arguments go in as an argv array so nothing in a path is run as shell code.
- **Don't mistake a command-text guard for a permission system.** Blast Radius reads the command text, so `$(…)`, aliases and scripts that call `rm` get past it. Use permission rules for a hard block.
- **Make an agent's edits easy to review with an observer that changes nothing.** Replay Theater records every Edit and Write call (the file plus the text before and after) and, when the turn ends, steps you through the edits one diff at a time. It never blocks or changes an edit; one replay covers one turn, and subagent turns are kept out of the grouping.
- **Vet a shared mod the way you would a package.** A mod runs inside Claude Code on your machine with the same access Claude Code has, and its publisher is not Anthropic. Read the repo first and install only from people you trust; nothing installs until you run the command.
- **Share a team's mods through an ordinary plugin marketplace.** A mod is a plugin, so a GitHub repo with a marketplace file becomes your marketplace; anyone can install from it and you update it with a normal push.

## Perishable details
- Version and API: mods need Claude Code 2.1.287 or later and are on by default. The post warns the API can change between releases; the type declarations Claude Code writes into the mod's `.claude-plugin/types/` folder each time it loads a mod are the authority for your version.
- Mechanics: a mod is a plugin whose `hooks/hooks.json` names one module exporting `register(on, options)`. Hooks added with `on(event, matcher?, hook)` form a chain and can observe, rewrite or answer (deny) an event. The events, the `$` API, the `AbovePrompt` component, props on `e.props`, the 10-second hook time limit (time inside `$` calls does not count) and the advice to use single-width symbols instead of emoji are all as of this release.
- Mods versus settings hooks: a settings hook runs a shell command per event with JSON over stdin and stdout; a mod is loaded once, keeps state, draws UI that updates as events happen and can call back into Claude Code. Some of Claude Code's own features, including AGENTS.md support and the `/diff` pane, are built as mods (source in the public anthropics/claude-code repository under `mods/`).
- Hot reload: every save re-runs `register` and `session.start`, so keep data in `$.state` (held by the host and declared in the plugin's types contract, or `claude plugin validate` errors) rather than in module variables. A mod made in a session loads only in that session and its folder is cleaned up later, so copy it out to keep it.
- Tooling: `claude --plugin-dir`, `claude plugin validate`, `claude plugin test` (hooks registered in a test run after the mod and stub what Claude Code would answer) and `claude --debug` (shows when a hook returned a tree that does not validate).
- Distribution: `/plugin marketplace add`, `/plugin install` and `/reload-plugins`; plugins that include mods can be submitted at claude.ai/directory/manage.

## Evidence
- None.

## Quotes
> "That makes mods a way to fit Claude Code to how you work. You can add a readout you check all the time, put a guard in front of the commands that make you nervous, or build a review view for how you like to read changes."

> "The three mods here came from one question each: how full is my context?, what is this command about to delete?, and what did Claude just change? Your questions will be different, and that's the point."

> "Notice that the prompt only describes what you want to see. You don't need to know the API to write one."

> "It's a safety net, not a permission system."

> "Use permission rules for a hard block."

> "So install mods the way you'd install a package: read the repo first and only install from people you trust."

> "Put the mod in a GitHub repo with a marketplace file and that repo becomes your marketplace. Anyone can install from it, and you can update it with a normal push."

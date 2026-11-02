# Handing Claude a long task

> I'm about to hand Claude Code a large migration and let it run for a few hours on its own. How should I write the task so it doesn't come back half-done or claim success it didn't earn?

Each answer comes from a fresh Claude Code session, one with let-it-cook installed and one without, in the eval run of 2026-11-02 (Claude Code 2.1.292 with its default model, graded by Sonnet). Both are shown in full and unedited, except that their headings are moved down two levels to fit this page.

**What a good answer covers**, taken from the source post rather than from the plugin:

1. State the finish line explicitly (what done means), together with a command or check that proves it is done.
2. Say when the agent should stop and ask, and when it should keep going.
3. Ask for evidence: the agent runs the real checks, shows their output, and marks anything it could not confirm.

**How often answers covered all of it:** with let-it-cook, 3 of 3 runs; without, 1 of 3.

## Without the plugin

Most failures on long autonomous runs come from three gaps: "done" isn't defined in a way it can check, nothing outside the session tracks progress, and no rule says what to do when it gets stuck. Close those three and most of the problem goes away.

#### 1. Define "done" as commands it can run
"Migrate X to Y" invites it to stop when the work *feels* finished. Give it completion criteria a machine can check:

- `rg 'oldApi\.' src/` returns nothing (or only the allowlisted exceptions you list)
- `npm run typecheck && npm test && npm run lint` exits 0
- Any project-specific check, such as the app booting or a smoke script passing

Tell it that it isn't done until every one of these passes, and that it must paste the actual final output in its report.

#### 2. Make it build an inventory first and keep it in a file
Have it start by listing every site that needs migrating into a checklist file (say `MIGRATION.md`), then tick items off as it goes. This does three things:
- You can see the real scope before it starts.
- Progress survives context compaction over a multi-hour run, because the file is the source of truth, not its memory.
- "Half-done" becomes obvious from the unchecked items instead of hidden.

#### 3. Forbid the usual shortcuts by name
Under pressure, agents make checks pass instead of making the code correct. Rule these out explicitly:
- No deleting, skipping or `.only`-ing tests, and no weakening assertions
- No `@ts-ignore`, `any`, `eslint-disable` or `# type: ignore` added to get past errors
- No stubbing or mocking the thing being migrated
- No changes to the verification config (test config, tsconfig strictness, CI)

Also tell it what to do when it's stuck: **"If you can't migrate something properly, leave it, record why in `MIGRATION.md` under Blocked, and move on."** Without that escape hatch, an agent that's stuck tends to fake a fix.

#### 4. Commit in small steps on a branch
Have it work on a branch or worktree and commit after each logical unit, with the checks passing at each commit. You can then review commit by commit, bisect if something breaks, and throw away a bad stretch without losing the rest.

#### 5. Ask for a final report that separates done from verified
Ask for:
- What was migrated, and the verification output
- What's blocked or skipped, and why
- Anything it changed that wasn't part of the migration
- What it's unsure about

Saying up front that an honest "70% done, here's what's left" beats a false "complete" makes a real difference to what you get back.

#### 6. Set things up so it can run unattended
- **Pilot first:** have it migrate one module while you watch, then review the approach. Fixing a bad pattern then is much cheaper than finding it repeated 400 times.
- **Permissions:** pre-allow the build, test and git commands it will need so it doesn't stall for hours waiting on an approval prompt. `/fewer-permission-prompts` can help here.
- **Stop hook (the strongest guarantee):** a hook that runs your verification command when Claude tries to finish, and blocks it from stopping if the checks fail. This turns "done" from a claim into something the harness enforces. I can set one up for you if you'd like.
- **Independent review at the end:** run `/code-review` or a fresh session on the diff, since the agent that wrote the code is the worst judge of it.

#### Prompt template

```
Migrate <X> to <Y> across this repo.

Context: <why, any constraints, non-goals, patterns to follow; link an
already-migrated example if you have one>

Process:
1. Inventory every usage of <X> into MIGRATION.md as a checklist before changing code.
2. Work on branch `migrate-y`. Commit after each module, with checks passing.
3. Update MIGRATION.md as you go; it is your source of truth if context is lost.

Done means ALL of these pass, and you paste their final output in your report:
- `rg '<old pattern>' src/` → no matches (except: <allowlist>)
- `<typecheck>`, `<test>`, `<lint>` → exit 0

Do not: delete/skip/weaken tests, add type/lint suppressions, mock out
<X>/<Y>, or modify test/CI/tsconfig settings.

If something can't be migrated properly, don't work around it: record it
under "Blocked" in MIGRATION.md with the reason and continue.

Final report: migrated / blocked (with reasons) / unrelated changes /
anything you're unsure about. An accurate partial report is far more useful
than an inaccurate "complete".
```

If you tell me the migration and your test and build commands, I can fill in the template and write the Stop hook for this repo.

## With let-it-cook

Two things cause most of these failures: the agent can't tell where "done" is, and nobody checks whether its success claims are true. Fix both in the task text.

#### What Anthropic's teams do

**1. Write it as one self-contained ticket with a finish line and the command that proves it.** Put the whole task in one message: what's wrong, what done looks like, and how to prove it. ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/), [Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))
> "Name the command that proves the task is done, and read Claude's summary before the diff."

For a migration, "done" should be something a machine can check. For example: `rg 'oldlib' src/` returns nothing, the full test suite and type-check pass, and the build succeeds. "Migrate to X" alone is not a finish line.

**2. Say what counts as evidence.** Only checks that actually exercise the change count: tests, the type-checker, the build. A syntax-only check doesn't count, and neither does a test command that never started. If a check can't run, the agent should name it and say why rather than report done. ([Sonnet 5.5](https://claude.dev/blog/building-with-claude-sonnet-5-5/)) Have it paste the real output instead of just saying it passed. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

**3. Have a different agent verify.** An agent tends to favor its own results when it judges them. Tell it to run a separate subagent that checks the work against your criteria, adversarially and in a fresh context. ([Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/)) Give that verifier the same spec and plan files the implementer had. ([HTML](https://claude.dev/blog/using-claude-code-the-unreasonable-effectiveness-of-html/)) For a large migration, split the work across subagents and check each one's evidence before accepting it. ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))

**4. Keep the task list in a file.** A file survives context summarization over a multi-hour run and shows what's done and what's left. ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/)) This is the main defense against a half-finished run.

**5. Say when to stop.** If you don't, it either stalls waiting for you or does something you didn't want:
> "Stop and ask only when you can't continue without me, or before anything destructive: deleting data, force-pushing, or changing anything outside this repository."

**6. Set the end-of-run report format,** for example "Blocked on me / Changed / Found", and ask it to "Mark anything you couldn't confirm, and say where you looked." Read that report before the diff. ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))

**7. Use high or max effort.** With no person in the loop, effort mostly buys verification and edge-case testing. Low-effort runs tend to stop at an answer that looks plausible. ([Spending effort](https://claude.dev/blog/spending-your-effort/)) Effort won't rescue a wrong approach, though, so agree on the approach with it interactively first and commit the plan. ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))

**8. Put the commands in the repo.** Test and build commands belong in CLAUDE.md or a verification skill, not only in your head or `~/.claude`. That way the agent and the verifier run the same checks. ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/), [Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/))

#### A template

```
Goal: Migrate <module/repo> from <old> to <new>.

Done means ALL of:
- `rg '<old-import-pattern>' src/` returns nothing
- `<test command>` passes (paste the summary line)
- `<typecheck>` and `<build>` pass (paste output)
- Behavior unchanged: <specific check, e.g. snapshot/golden tests, API contract tests>

Process:
- First, write MIGRATION_TODO.md listing every file/module to migrate; tick items off as you go.
- Commit after each module so progress is recoverable.
- When you think you're done, spawn a fresh subagent with this spec and
  MIGRATION_TODO.md to adversarially verify. Fix what it finds.
- If a check can't run, say which and why. Don't report it as passing.

Stop and ask only if you can't continue without me, or before deleting data,
force-pushing, or touching anything outside this repo.

Final report: Blocked on me / Changed / Found / Not verified (and where you looked).
```

#### Beyond claude.dev (general practice)

- **Lock down current behavior first.** If test coverage around the migrated code is thin, have it add characterization tests before changing anything. Otherwise "tests pass" can't prove behavior was preserved.
- **Work on a branch with a hard permission boundary.** Use permission rules to deny force-push and deploys, rather than relying only on the instructions.
- **Try one module first.** Do a short supervised run on a single module to find gotchas, add them to CLAUDE.md, then start the long run.

# Delegation: handing work to agents

What Anthropic's teams do, from claude.dev. Every rule links to its post; the digests in `../posts/` hold details and exact quotes.

## Write the task

- **Give the whole task in one message, name the finish line, then let it work.** ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))

> "With a clear finish line, it knows when it’s done."

- **Make it a self-contained ticket: what's wrong, what done looks like, and how to prove it.** ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))

> "Write each task as a self-contained ticket that states what's wrong, what done looks like, and how to prove it."

- **Say when to stop and ask, and keep your own check before anything risky.** Write the stops you want into CLAUDE.md: keep going when a step doesn't need you, and stop only when it can't continue without you or before something destructive. ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))

> "Stop and ask only when you can't continue without me, or before anything destructive: deleting data, force-pushing, or changing anything outside this repository."

- **Give rich references, preferably in code**: a test suite as the spec, a function to port, an HTML mockup instead of a description or screenshot. ([Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/))
- **Get a detailed spec by having the agent interview you.** With a detailed spec, different models and effort levels produced much more similar results. ([Spending effort](https://claude.dev/blog/spending-your-effort/))
- **For design work, list the specific patterns to leave out**; a general "avoid a generic look" just swaps one default for another. ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))

## Pick effort and model

- **Effort is a dial for verification, edge-case testing and independent judgment; set it by how in the loop you want to be.** Low gets a fast starting point to iterate on; higher effort does more but makes more assumptions on your behalf. ([Spending effort](https://claude.dev/blog/spending-your-effort/))
- **The author's rule of thumb**: low for brainstorming, sketching and easy changes; medium for most regular engineering; high where verification matters or there are edge cases; max for fully autonomous work on hard problems. Raise effort when no person is in the loop. ([Spending effort](https://claude.dev/blog/spending-your-effort/))

> "High: for work where verification is important or there are edge cases, e.g. fixing a bug in a brownfield codebase."

- **Run the loop: interview, implement on low, review, verify on high.** ([Spending effort](https://claude.dev/blog/spending-your-effort/))

> "For normal software engineering, I’m running a loop of getting the model to interview me then implementing on low effort, reviewing what it built, and then running verification on high effort."

- **Add a check before you add effort, and add effort before you switch to a bigger model.** Switch when the same problem fails twice at a high level, and re-pick the level whenever the model changes; levels don't carry over. ([Task cost](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/), [Sonnet 5.5](https://claude.dev/blog/building-with-claude-sonnet-5-5/))
- **Give cheaper models only lookups, where a mistake is cheap to spot**; keep judgment calls and code edits on the main model, and set the model on each subagent explicitly. ([Task cost](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/))

> "The tradeoff: a small model that misreads a search result sends the main model after the wrong file, and the main model pays for the detour. Keep the small model on work where a mistake is cheap to spot, like finding files, running tests and reading logs."

- **Put well-scoped work with a clear spec and a checkable result on the mid tier, and long-horizon work that needs careful judgment on the top tier.** ([Sonnet 5.5](https://claude.dev/blog/building-with-claude-sonnet-5-5/))

## Give the agent the right context

- **Keep CLAUDE.md light: what the repo is for, then the gotchas.** Skip what the model can learn from the file system, and put several verification steps into a verification skill referenced from CLAUDE.md. ([Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/))

> "Keep your CLAUDE.md lightweight and briefly describe what your repo is for, but spend most of the tokens on gotchas inside of the codebase."

- **Put commands and setup in the repository, not in personal config**: test commands in CLAUDE.md, shared skills under `.claude/`, install steps in a SessionStart hook, so they work the same locally and in the cloud. ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))

> "Your personal `~/.claude` doesn't reach the cloud VM. If Claude needs to know how to run the integration tests, the repository has to say so."

- **Use a tree of files that load when needed, not one central file of every practice.** ([Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/))
- **Delete rules that over-constrain the model, and simplify as models improve.** Anthropic removed over 80% of Claude Code's system prompt with no measurable loss on its coding evals. When you migrate, re-audit instructions written for the older model; they can make a newer one write more and repeat tool calls. ([Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/), [Task cost](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/))
- **Keep sessions stable and lean.** Set the model, tools and servers at the start and leave them alone; clear between unrelated tasks; compact at a natural break and say what to keep. ([Task cost](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/))

## Package know-how as skills

- **Keep each skill to one job.** Anthropic's internal skills fall into nine categories (library reference, product verification, data analysis, business process, scaffolding, code quality, CI/CD, runbooks, infrastructure operations); a skill that straddles several confuses the agent. ([Skills](https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/))
- **Write only what Claude wouldn't do by default, and grow a Gotchas section from real failures.** The best skills start as a few lines and one gotcha. ([Skills](https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/))

> "The highest-signal content in any skill is the Gotchas section. These sections should be built up from common failure points that Claude runs into when using your skill."

- **Write the description as a trigger, not a summary**; state goals and constraints rather than every step; make the skill a folder Claude reads as needed, with scripts carrying their gotchas in docstrings. ([Skills](https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/))

> "the description field is not a summary, it's a description of when to trigger this skill."

- **Check skills into the repo while small, move to an internal plugin marketplace as you grow, let skills earn their way in, and log usage to find undertriggering ones.** Ship strict guardrails as hooks that are active only while their skill runs. ([Skills](https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/))

## Split the work

- **One task, one session, one branch.** Split parallel tasks along file boundaries, merge in a sensible order, and expect one session to report problems another is already fixing. ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))
- **Fan big audits and migrations out to subagents, and check each one's evidence.** ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))
- **Use multi-agent workflows only for long, parallel or adversarial work.** A single context tends to stop early, favor its own results and drift from the goal. Most ordinary coding tasks don't need it; keep agent teams small and shut teammates down when done. ([Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/), [Task cost](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/))

> "For regular coding tasks, try and ask yourself: does it really need more compute? For example, most traditional coding tasks do not need a panel of 5 reviewers."

- **Settle the approach interactively, commit the plan, then hand it to a cloud session**; stay local only when the task needs something only your machine has (real local data, a VPN, a GPU, hardware, tight visual loops). ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))

## Run long tasks

- **Keep the task list in a file**, which survives context summarization and shows what's done and what's left. ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))
- **When a run ends, read what it needs from you first**, and set the summary format you want in CLAUDE.md, for example "Blocked on me, Changed, Found". ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))

## Stay in the loop

- **Use outputs people actually read.** One Claude Code engineer has the agent write specs, plans, reports and PR writeups as HTML (tabs, diagrams, annotated diffs), compares options side by side before committing, and builds throwaway editors that end with a "copy as prompt" export. He presents this as his own practice. ([HTML](https://claude.dev/blog/using-claude-code-the-unreasonable-effectiveness-of-html/))

> "As Claude takes on more, I'd noticed I was reading plans less closely, and I wanted a way to stay engaged with its choices rather than just hand them off."

- **Shape the tool around one question you keep asking**, such as "what is this command about to delete?", and let Claude write the mod. A guard that reads command text is a safety net, not a permission system; use permission rules for a hard block, and vet shared mods like packages. ([Mods](https://claude.dev/blog/getting-started-with-claude-code-mods/))

> "It's a safety net, not a permission system."

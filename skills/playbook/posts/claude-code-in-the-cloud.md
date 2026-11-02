---
title: "Claude Code in the cloud: a field guide to cloud sessions"
url: https://claude.dev/blog/claude-code-in-the-cloud/
published: 2026-10-06
author: Addy Osmani
category: Playbooks
topics: [delegation, verification, automation]
---

# Claude Code in the cloud: a field guide to cloud sessions

**Core idea:** Give each agent task its own machine and branch, so several tasks can run in parallel and unattended and each comes back as a branch to review. It works when every task is a self-contained ticket with a command that proves it is done, and when the repository itself tells the agent how to run its checks.

## Durable guidance
- **Write each task as a self-contained ticket that states what's wrong, what done looks like, and how to prove it.** The flaky-test prompt named its proof, running the suite at least 30 times in a row, and the session ran it 40 times.
- **Give each task its own session and branch.** Small, separate sessions are easier to review and cheaper to throw away. Each demo session had its own copy of the repository, its own processes and its own branch, so the docs and logger sessions could both start the API server without affecting each other, where two agents in one checkout would edit the same files and collide on a port unless each picked its own.
- **Split parallel tasks along file boundaries, merge the branches in a sensible order, and expect a session to report problems another session is already fixing.** The sessions don't know about each other: the logger session had no access to the cache fix the first session was making. When branches conflict, merge one, then send the next session a follow-up asking it to rebase on main and fix conflicts.
- **Give sessions what they need to check their own work, and ask for thorough proof.** A session that can run your tests checks its work before it hands it back; without that, you review changes nobody has run. Proof that needs the suite run again and again shouldn't tie up the machine you're working on, so ask for it in the cloud: 200 suite runs, a regression bisected across 50 commits, the slow integration tier, or the app started and hit with curl.
- **Ask for evidence, and read the agent's summary before the diff.** In the logger session the commit went in with one failing test. Claude reran the cache test eight times, saw five failures, traced them to the race the first session was fixing, left the cache alone because it was outside its task, and said in its summary that the suite wasn't clean.
- **Agree on the approach interactively, commit the plan, then hand it to a cloud session to execute.** For a larger change, settle the approach where back-and-forth is cheap. Your terminal stays free while the session builds, and you can pull the session down afterwards to finish by hand.
- **Put the commands and setup the agent needs in the repository, not in personal config.** Your personal `~/.claude` doesn't reach the cloud VM, while the repository's `CLAUDE.md`, rules, skills, agents and commands do, so commit shared skills and commands under `.claude/`, add project-scoped MCP servers to `.mcp.json`, and document test commands in `CLAUDE.md`. Put install steps in a SessionStart hook in the repository's `.claude/settings.json` so they run the same way locally and in the cloud.
- **Keep a task local when it needs something only your machine has; otherwise treat it as a cloud candidate.** Local fits a database with real local data, a service behind a VPN, a GPU, a phone simulator, hardware on your desk, and tight visual loops where you want to see each change in your own browser within seconds. Most people use both.
- **Pick the narrowest network access that works, and keep secrets out of shared variables.** Trusted covers the common registries; add a private registry with Custom, and use Full only when the task needs the open internet. Environment variables are visible to anyone who uses the environment. The session gets a short-lived credential that can push only to its own working branch, and your GitHub token stays in a proxy outside the VM.
- **Run code you haven't read in a disposable VM, not on your laptop.** A contributor's pull request, a new dependency's install script or a freshly cloned repository would otherwise run next to your SSH keys, cloud CLI sessions and browser profile. Even with network access set to None, requests to the Anthropic API still go out, so data can leave the VM that way, and the session can still push to its own branch.
- **Let the agent take CI failures and review comments, and keep ambiguous or architectural calls for a person.** Claude pushes clear fixes for failing checks and review comments and explains what it changed; it asks about anything ambiguous or architectural.
- **Watch your usage limits when you run sessions in parallel.** Parallel sessions draw on plan limits in parallel, so five sessions use them about five times as fast as one.

## Perishable details
- Surfaces and commands: sessions start from claude.ai/code, the mobile app, Desktop, Slack, or `claude --cloud` in a terminal (which clones your GitHub remote at your current branch, so push first). `claude --teleport` or `/teleport` pulls a session into your terminal and needs a clean working tree and a pushed branch. `claude -p "..." --cloud <session-id>` queues a follow-up into a running session.
- Plans and cost: cloud sessions need a claude.ai login on Pro, Max, Team or Enterprise (premium seat or Chat + Claude Code seat); a Console API key or third-party provider doesn't work, and Zero Data Retention turns them off. There is no separate compute charge and sessions draw on the plan's usage limits; routines have their own hourly caps and projects can start up to 200 new threads a day.
- Environment specifics: about 4 vCPUs, 16 GB of RAM and 30 GB of disk. The setup script runs as root before Claude Code starts, must exit 0, and should finish in about five minutes so the environment is cached; the cache rebuilds when the script or allowed hosts change and about every seven days, and it stores files, not running processes, so start services per session. Network changes reach running sessions within about a minute. Foreground commands time out at 2 minutes by default (10 at most) and then keep running in the background for up to 30 more; `BASH_DEFAULT_TIMEOUT_MS` and `BASH_MAX_TIMEOUT_MS` raise the defaults.
- Session lifecycle: idle VMs are reclaimed, and a reopened session gets a fresh VM with the conversation restored, so commit as you go on long tasks. Approval modes in the cloud are Auto, Accept edits or Plan, with no per-command mode.
- Early-stage features: routines (research preview; triggered by a schedule (hourly at the most frequent), an HTTP call or a GitHub event; no approval prompts; push to `claude/`-prefixed branches by default), projects (public beta for Pro and Max; a coordinator conversation that starts and tracks sessions), self-hosted environments (beta for Team and Enterprise), and Auto-fix on a PR.
- Auto-fix details: it needs the Claude GitHub App; replies on review threads post under your GitHub username, labeled as Claude Code; Claude isn't notified of merge conflicts with the base branch, so ask it to rebase; its comments can trigger comment-driven automation such as Atlantis.
- GitHub connection: private repositories need both a GitHub sign-in and the Claude GitHub App installed on the account or organization that owns them, with an owner's approval for organizations; `/web-setup` sends your `gh` token instead; a repository with no GitHub remote is uploaded as a bundle; sessions can't push back to GitLab or Bitbucket.
- Sharing and credentials: on Team and Enterprise a session's visibility can be set to Team, and commits from cloud sessions carry a `Claude-Session` trailer that links back to the transcript. On Pro and Max, an environment's API credentials attach a key to requests for named hosts outside the VM, so the key never sits in a variable.

## Evidence
- The demos are four real cloud sessions against a small, made-up sample repository (tidepool); the transcripts, diffs and timings come from those sessions, so they illustrate the workflow rather than measure it across teams.
- Three sessions started within 16 seconds of each other ran for 61, 65 and 72 seconds, and all were done 87 seconds after the first started (wall-clock time for three unrelated tasks in parallel; recreating the repository took roughly a third to just over half of each run).
- Flaky test: it failed about one run in four before the fix; after the cache change, `npm test` ran 40 times in a row with zero failures.
- Docs session: ran a curl against every endpoint and found five ways the old API doc was wrong.
- Logger session: added five tests, and the cache test failed in five of eight reruns, which the agent traced to the same race the first session was fixing.
- Phone session: a question about how the tide prediction could go wrong at the window edges led the agent to run code and find a real bug (the loop never examines the first or last sample, so a high tide exactly at the start of the window is missed).
- Parallel usage: five sessions use plan limits about five times as fast as one (stated as arithmetic, not measured).

## Quotes
> "Write each task as a self-contained ticket that states what's wrong, what done looks like, and how to prove it."

> "A session that can run your tests checks its own work before it hands the work back. Without that, you review changes nobody has run."

> "Split parallel tasks along file boundaries, merge the branches in a sensible order, and expect a session to report problems that another session is already fixing."

> "Stay local when the task needs something only your machine has."

> "Name the command that proves the task is done, and read Claude's summary before the diff."

> "Your personal `~/.claude` doesn't reach the cloud VM. If Claude needs to know how to run the integration tests, the repository has to say so."

> "Parallel sessions draw on your plan limits in parallel, so five sessions use them about five times as fast as one."

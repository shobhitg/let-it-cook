# An AI reviewer and a coding agent that won't stop

> Our coding agent and our AI code reviewer keep ping-ponging: one pull request went through 30 review rounds overnight. How do we stop that without dropping AI review?

Each answer comes from a fresh Claude Code session, one with let-it-cook installed and one without, in the eval run of 2026-11-02 (Claude Code 2.1.292 with its default model, graded by Sonnet). Both are shown in full and unedited, except that their headings are moved down two levels to fit this page.

**What a good answer covers**, taken from the source post rather than from the plugin:

1. Cap the number of review rounds; after the cap (the source uses three), the author steps back and reconsiders the approach instead of patching again.
2. After the first passes, re-review only the new diff, and don't repeat findings already posted.
3. Flag the class of bug rather than one line, so the author fixes every instance in one pass.

**How often answers covered all of it:** with let-it-cook, 3 of 3 runs; without, 0 of 3.

## Without the plugin

A 30-round loop means the system has no stopping condition. The reviewer finds something new on every pass, because LLM reviewers rarely return "nothing to add". The agent treats every comment as an order. Neither side is allowed to decide the PR is done. Here's how to fix that while keeping AI review.

#### 1. Cap the rounds and hand off to a human
This is the most important fix. Allow at most 2–3 automated fix/review cycles per PR. After that, the bot stops, adds a label such as `needs-human-review`, and posts a summary of the findings that are still open. Also set a time or cost budget so nothing runs unattended overnight without a limit.

#### 2. Only block on findings that matter
Make the reviewer tag each finding as **blocking** (correctness, security, data loss, broken contract) or **non-blocking** (style, naming, "consider…").
- The agent fixes blocking findings automatically.
- Non-blocking findings go into one comment that a human can act on or ignore. They never trigger another cycle.
- Move style nits to a formatter or linter. Those tools give the same answer every time, so they can't loop.

#### 3. After round 1, review only what changed
Most loops happen because each round re-reviews the whole PR from scratch and finds new things to say. From round 2 on:
- Pass the reviewer **only the diff since its last review**.
- Pass it the **earlier findings and how each was resolved**.
- Instruct it: *"Don't re-raise resolved or declined items. Only report problems introduced by the latest commit, and only blocking ones."*
- Raise the confidence bar each round. For example, report any finding in round 1, but only high-confidence bugs in round 2 and later.

#### 4. Let the agent push back
Give the coding agent a documented way to reply "won't fix: <reason>". The reviewer should accept that unless it's a correctness or security issue, in which case it escalates to a human instead of arguing. Without this, the agent keeps making changes and every change gives the reviewer new code to comment on.

#### 5. Detect when it isn't converging
Stop automatically when you see any of these:
- **Oscillation:** the same file or lines are rewritten back and forth, or a finding matches one from an earlier round. You can catch this by hashing findings on file, rule, and a normalized message.
- **No progress:** the number of findings isn't dropping, or the diff keeps growing.
- **Contradiction:** the reviewer asks to undo a change it requested earlier.

#### 6. Control when review runs
- Don't review on every push. Trigger on "ready for review", on a label, or on an explicit `/review` comment.
- Debounce, so a burst of agent commits gets one review.
- Use the same reviewer model, prompt and rubric on every round so results don't drift.

#### 7. Track it
Measure rounds per PR, the share of findings that got accepted versus declined, and how often PRs escalate to humans. A low acceptance rate means the reviewer is too noisy and its threshold should go up.

---

**Recommended minimum:** a round cap with human handoff (§1), blocking vs. non-blocking findings (§2), and incremental review with prior-findings context (§3). Together these usually stop the loop, and the reviewer still catches real bugs.

If you're using Claude Code's `/code-review`, it already has the controls for this: a lower effort level gives fewer, higher-confidence findings, and `--max-findings <n>` limits how many it reports.

If you tell me where this runs (GitHub Actions, a custom bot, etc.) and point me at the config or workflow files, I can add the round cap, the severity gating and the loop detection.

## With let-it-cook

Anthropic's Claude Code team hit this exact problem. One of their PRs went through **more than fifty** review-and-fix rounds overnight before its author stopped it. They kept AI review and changed how it re-reviews, so the loop ends. Everything below is from claude.dev unless marked otherwise.

#### What Anthropic's teams do

**Find out why it doesn't converge.** They ran git blame on what the reviewer kept flagging. About **59% was code that had been there since the reviewer's first pass**. The reviewer wasn't catching the agent's new mistakes. It was finding a few more old bugs each round. They also note that noise costs more when the author is an agent: "a person waves off a nit in seconds, while an agent fixes it, adding a commit and another round." ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

**The changes they made** ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/)):
1. **Cap at three rounds.** After round three, the reviewer stops posting findings and asks the author to step back and reconsider the approach.
2. **Re-review only the new diff** after the first few passes, so later rounds don't re-scan the whole PR.
3. **Flag the class of bug, not one instance.** The author then fixes every occurrence in one pass instead of one per round.
4. **Don't repeat findings already posted.**
5. **Track rounds-to-pass as a metric**, next to recall. Their stated priority is "real bugs first, review rounds second." Several rounds are fine on a risky change, but not on every PR.

**Cut what the reviewer flags in the first place:**
- Have it list only problems that would block the merge, each with evidence: *"List only problems you'd block the merge for. For each one, give the file and line, why it's wrong, and how to show it fails."* ([Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))
- Have several agents look for bugs, have a separate group vote on each finding, post only findings enough of them agree on, and drop style-only comments. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- Have code owners write a short `REVIEW.md`. It describes what failure looks like in their code, caps nits, lists paths to skip, requires file-and-line evidence, and asks for a summary that starts with a count and says plainly when there's nothing to fix.
- If the reviewer keeps flagging the same thing, fix it at the source: a lint rule, a skill, or an instruction file.
- Their product tags pre-existing problems separately ("Pre-existing") from new findings.

**Send hard calls to a person.** Agents can handle CI failures and clear review comments, but ambiguous or architectural questions go to a human. ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/)) On an agent-written PR, the person directing the agent counts as a required reviewer.

**Measure noise.** Sort each reviewer comment by what happened to it: fixed, said to be wrong, intentional, or didn't matter. Also run the reviewer on PRs you know are clean and count anything it flags there. Without this, you can't tell whether the cap is cutting real bugs or noise.

#### Beyond claude.dev (general practice, not from the posts)

- **Enforce the cap in your pipeline, not just in the prompt.** Count review rounds per PR in CI or the bot. At the limit, stop automatic fix cycles, add a label like `needs-human`, and notify the owner. A prompt-only cap can be ignored. A counter can't.
- **Give unattended runs a time or token budget** so a loop can't run all night unnoticed.
- **Don't let the agent fix pre-existing issues in the PR.** Have it file them as tickets instead. This takes away most of what kept the loop going.
- **Diagnose your own 30-round PR.** Run git blame on the reviewer's later comments. If most point at old code, the fixes above (diff-only re-review, pre-existing tagging, don't repeat findings) will remove most of the rounds.

The order that usually pays off fastest: a hard cap with escalation to a person, then diff-only re-review and pre-existing tagging, then a `REVIEW.md` limited to merge-blocking issues.

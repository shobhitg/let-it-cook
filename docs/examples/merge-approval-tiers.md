# Merge approvals when agents write the code

> Claude writes most of our code now, and requiring two human approvals on every pull request has become our bottleneck. How should we set up code review and merge approvals so we can move faster without breaking things?

Each answer comes from a fresh Claude Code session, one with let-it-cook installed and one without, in the eval run of 2026-11-02 (Claude Code 2.1.292 with its default model, graded by Sonnet). Both are shown in full and unedited, except that their headings are moved down two levels to fit this page.

**What a good answer covers**, taken from the source post rather than from the plugin:

1. The number of human approvals a change needs depends on its risk tier, decided by what the change touches rather than by who wrote it, and low-risk changes such as docs or additive changes behind a flag can merge once automated checks pass.
2. An approval from an AI agent or bot never counts as a required human approval.
3. Revert and incident rates are the guardrail that shows whether lighter review is working.

**How often answers covered all of it:** with let-it-cook, 3 of 3 runs; without, 1 of 3.

## Without the plugin

Going from two human approvals to one is reasonable. Going to zero is not. When Claude writes the code, the person who prompted it is effectively the author, so the reviewer is often the only human who checks the change with fresh eyes. The bottleneck usually isn't the number of approvals. It's that reviewers spend time on things machines could check, and every PR gets the same scrutiny whatever its risk.

#### Recommended setup

##### 1. Base rule: one human approval from someone other than the prompter
- Treat the human who drove the Claude session as the author. They can't approve their own PR, even if a bot account opened it.
- In GitHub rulesets: require 1 approval, dismiss stale approvals on new pushes, and require approval of the most recent push. That last setting stops someone pushing changes after the review.

##### 2. Tier the review by risk, not by who wrote the code
Use CODEOWNERS and path-based rulesets:

| Tier | Examples | Requirement |
|---|---|---|
| **High** | auth, payments, permissions, crypto, infra/IaC, DB migrations, CI config, CODEOWNERS itself | 2 humans, including a code owner |
| **Standard** | most product code | 1 human + green CI + AI review |
| **Low** | docs, copy, tests-only, dependency patch bumps with passing CI | 1 human (quick skim) or auto-merge for narrowly defined cases |

Two approvals then apply only to the 10–20% of PRs where they actually matter.

##### 3. Let automation do the first pass so humans review faster
- **AI review as a required check, never as the approver.** Run a separate review pass, such as `/code-review` or `/security-review`, in CI. Claude reviewing its own work catches real bugs, but it shares blind spots with the author, so it supplements human review and doesn't replace it.
- **Strong CI gates:** tests, type checks, lint, coverage on changed lines, SAST/secret scanning, dependency audit. If CI is weak, fix that before relaxing review. It's what makes fewer approvals safe.
- **PR template written by Claude:** what changed, why, how it was tested, and the risk areas. Reviewers should spend their time judging intent and design, not reconstructing what the diff does.

##### 4. Keep PRs small
Claude produces large diffs easily, and large diffs get rubber-stamped. Set a soft size limit (around 400 changed lines) and have Claude split work into stacked PRs. Small PRs take minutes to review, which does more for throughput than cutting approvers.

##### 5. Make mistakes cheap to undo
- Use feature flags for behavior changes so merging and releasing are separate steps.
- Use canary or staged rollouts with automatic rollback on error-rate alerts.
- Keep merge queues so main stays green.

This is what actually prevents "breaking things." Review will never catch everything, but fast detection and rollback limit the damage.

##### 6. Measure it
Track time-to-first-review, time-to-merge, change failure rate, and rollbacks. If failure rate stays flat after the switch, consider widening the low-risk tier. If it rises, tighten the specific paths where the failures happened.

#### What to avoid
- **Claude approving its own PRs, or a bot approval counting toward the required number.** This removes the human check without saying so, and many compliance frameworks (SOC 2, ISO 27001) expect human separation of duties.
- **Admin bypass as the routine fast path.** Allow it only for emergencies, and log and review every use.
- **Letting Claude edit CI, CODEOWNERS, or branch protection under the standard tier.** Those files control the gates, so they belong in the high-risk tier.

#### Rollout
1. Harden CI and add the AI review check (about one week).
2. Add CODEOWNERS for the high-risk paths.
3. Drop the default to 1 approval, keeping 2 for high-risk paths.
4. After a month of metrics, decide whether to allow auto-merge for the low tier.

If you tell me which platform you use (GitHub, GitLab, etc.) and share your repo layout, I can draft the CODEOWNERS file, the ruleset config, and a CI workflow that runs the AI review step.

## With let-it-cook

Stop asking "did two humans read this?" and start asking "what could go wrong with this change, and which check should catch it?" Anthropic's Claude Code team uses that framing ([code review post](https://claude.dev/blog/solving-code-review-at-anthropic/)):

> "We think "did a human read the code?" is an imprecise proxy for "what could go wrong with this change, and which check—automated or human—is the right one to catch it?""

In practice, the number of human approvals depends on how risky the change is, automation does most of the checking first, and mistakes are made cheap to undo.

#### What Anthropic's teams do

**1. Base approvals on risk.** The change decides the tier, not who wrote it. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

| Tier | Examples | Human approvals |
|---|---|---|
| Low | Docs, copy, internal-only features, additive changes behind a flag | **0**, once automated review and security checks pass |
| Medium | Ordinary product changes; sensitive areas like caching, auto-updater, system prompts | **1** |
| High | The riskiest code, plus paths owners say always need two | **2** |

- A classifier picks the tier. A second classifier asks whether this particular change needs a person anyway.
- Anything code owners mark as sensitive always needs a person, and so does every CI workflow file.
- Start strict and loosen the tiers only when you have evidence.

**2. Keep the human-approval rules strict.**
- An agent's approval never fills a human slot. Automated review can clear a low-risk change, but it can't replace a required person.
- Only authors on a trusted list get the lighter paths.
- An approval covers one specific commit. It has to be given again after any push the system can't vouch for, such as an agent's push or a merge conflict resolved by hand.
- On an agent-written PR, the person directing the agent counts as one of the required reviewers: "Whoever prompted the change is on the hook for it."

**3. Have the agent show evidence before anyone looks.** It runs tests, the build, or a screenshot against the design, and shows the output instead of just saying it's done. Then a subagent with fresh context reviews the diff. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

**4. Run an AI reviewer that blocks merges and settles quickly.** ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/), [Opus 5.5 playbook](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/))
- Several agents look for bugs and a separate group votes on each finding. Only findings with enough agreement get posted, and style-only findings are dropped. Every posted finding must be answered before merge. Security review runs separately and also blocks.
- Ask only for problems worth blocking a merge: "give the file and line, why it's wrong, and how to show it fails."
- Limit the review rounds. After three, the reviewer asks the author to rethink the approach. Later re-reviews look only at the new diff, and findings already posted aren't repeated. (One PR went through more than 50 rounds overnight, and about 59% of what kept getting flagged was code that existed before the PR.)
- When the reviewer keeps flagging the same thing, fix it at the source with a lint rule, a skill or an instruction file. Have code owners write a short `REVIEW.md` saying what failure looks like in their code.

**5. Make mistakes cheap to undo.** ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/), [claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))
- Use a merge queue that re-runs every check against main with the change applied, so two PRs that pass separately can't break main together.
- Put user-visible changes behind short-lived feature flags and roll them out in stages: employees, then a small share of users, then everyone. Flags should turn off without a deploy.
- Keep an on-call rotation, release to a `latest` channel before `stable`, and run blameless incident reviews that ask which layer should have caught the problem.

**6. Spend human attention where only people can decide:** whether to build the thing at all, risky code (billing, updaters, CI), architecture others will copy, and reading the evidence. If you can't say what the checks would miss, do a real review rather than a quick approval.

**Results they report:** Merged PRs to Claude Code more than doubled from June to September 2026, while the share of PRs that got reverted fell by more than 40%. A separate effort merged more than 3,000 changes in two weeks with no customer-facing incident or rollback, each with at least one human approval.

#### Beyond claude.dev (general practice)

A suggested rollout order:
1. **Measure first.** Track human time per change, time to merge, and the revert and incident rate. Speed is the goal, and reverts and incidents tell you if you've loosened too far.
2. **Add the safety net before removing approvals:** the merge queue, required CI, the AI reviewer as a required status check, and CODEOWNERS for sensitive paths and `.github/workflows/`.
3. **Drop to one human approval for medium-risk changes.** Keep two only for the high-risk paths in CODEOWNERS.
4. **Turn on zero-human merges for low-risk changes** (docs, flagged additive changes) only after a few weeks of clean revert data.

On GitHub, you can enforce most of this with rulesets: require approvals per path through CODEOWNERS, dismiss stale approvals on new pushes, require status checks, and use the merge queue. Risk-tier classification usually needs a small bot or workflow that applies a label, which the rules then read.

If you share your repo layout, I can draft the CODEOWNERS, ruleset and `REVIEW.md` for your setup.

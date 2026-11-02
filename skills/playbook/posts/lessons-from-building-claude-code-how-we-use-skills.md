---
title: "Lessons from building Claude Code: How we use skills"
url: https://claude.dev/blog/lessons-from-building-claude-code-how-we-use-skills/
published: 2026-06-03
author: Thariq Shihipar
category: Skills
topics: [delegation, agent-design, verification, automation, measurement]
---

# Lessons from building Claude Code: How we use skills

**Core idea:** Skills are folders of instructions, scripts and data that teach an agent your team's specific work, and the best ones are narrow, built from the failures Claude actually hits, and grown over time. From hundreds of internal skills the Claude Code team drew nine categories, found that verification skills had the most measurable impact, and describes how they share and measure skills.

## Durable guidance
- **Keep each skill inside one category, and use the nine categories to find gaps in your library.** Anthropic's internal skills cluster into: library and API reference; product verification; data fetching and analysis; business process and team automation; code scaffolding and templates; code quality and review (you may want to run these automatically in hooks or a GitHub Action); CI/CD and deployment (for example babysitting a PR, or a deploy with gradual traffic rollout, error-rate comparison and auto-rollback); runbooks (a symptom in, a multi-tool investigation, a structured report out); and infrastructure operations (destructive actions benefit from guardrails). The best skills fit cleanly into one; those that try to do too much straddle several and confuse the agent.
- **Invest in verification skills.** They have had the most measurable impact on Claude's output quality internally, and it can be worth an engineer spending a week just making them excellent. Pair them with tools like playwright or tmux, have Claude record a video of its output so you can see exactly what it tested, and enforce programmatic assertions on state at each step, often with scripts inside the skill.
- **Leave out what Claude already does by default.** A skill that restates it adds context without adding value. For a knowledge skill, focus on information that pushes Claude out of its normal way of thinking (the frontend design skill was built by iterating with customers to avoid classic patterns like the Inter font and purple gradients).
- **Build a Gotchas section from the failures Claude actually runs into, and keep adding to it.** It is the highest-signal content in any skill. Examples: an append-only table where the wanted row has the highest version, not the latest `created_at`; one value called `@request_id` in the API gateway and `trace_id` in billing; staging returning 200 when a Stripe webhook did not process. Most of the best skills began as a few lines and a single gotcha and improved as people added the edge cases Claude hit.
- **Treat a skill as a folder, and let Claude read files as it needs them.** Think of the file system as context engineering and progressive disclosure: tell Claude what files are in the skill (for example `references/api.md` for signatures, a template in `assets/`, a stuck-jobs.md for pending jobs). Also store scripts and helper libraries with the gotchas in their docstrings, so Claude spends its turns composing them into one-off scripts rather than reconstructing boilerplate.
- **State the goal and the constraints, not every step.** Skills are reused across many situations, so over-specific instructions railroad Claude; give it the information it needs and the flexibility to adapt.
- **Write each description as a trigger for the model, not a summary for humans.** At session start Claude builds a listing of every available skill with its description and scans it to decide whether a skill fits the request, so the description should say when to trigger the skill and include trigger words (for example "babysit").
- **Store setup and history in the skill's own files.** Put setup answers, such as the Slack channel for a standup post, in a config.json in the skill directory and have the agent ask the user when it is missing. Keep memory of past runs in an append-only log, JSON files or SQLite so the next run can read its own history (a standup log lets Claude say what changed since yesterday); for business-process skills, saved results help the model stay consistent and reflect on previous executions.
- **Bundle strict guardrails as on-demand hooks.** A hook inside a skill is active only when the skill is called and only for the session, so you can ship opinionated hooks you would not want always on: `/careful` blocks `rm -rf`, `DROP TABLE`, force-push and `kubectl delete` when you know you are touching prod, and `/freeze` blocks edits outside one directory while debugging.
- **Check skills into the repo while you are small, and move to an internal plugin marketplace as you scale.** For smaller teams across relatively few repos, checked-in skills (under `./.claude/skills`) work well, but every checked-in skill adds a little to the model's context. A marketplace lets people decide which skills to install and can include a setup flow.
- **Let useful skills earn their way into the marketplace.** Anthropic has no central team deciding; someone puts a skill in a sandbox folder in GitHub and points people to it in Slack or other forums, and once it has traction (the skill owner's call) opens a PR to move it into the marketplace.
- **Log skill usage to find popular and undertriggering skills.** A PreToolUse hook logs usage within the company, so you can compare how often skills fire against what you expected.

## Perishable details
- Mechanics named in the post: the `${CLAUDE_PLUGIN_DATA}` environment variable (a stable directory for persistent skill data), the AskUserQuestion tool (structured multiple-choice questions), the `./.claude/skills` path, the PreToolUse hook (used for both the `/careful` guard and usage logging), and skill configuration options such as dynamic hooks.
- Dependencies between skills are not natively built into marketplaces or skills yet; for now you reference other skills by name and the model invokes them if they are installed.
- The frontend design example (steering away from the Inter font and purple gradients) names Claude's design defaults at the time of writing.
- The post itself says skills best practices are still evolving.

## Evidence
- Hundreds of skills are in active use at Anthropic; cataloging them produced the nine categories (an observation, not a measurement).
- Verification skills had the most measurable impact on Claude's output quality internally; the post gives no figures.
- The post reports no other quantitative results, including none for skill usage.

## Quotes
> "The best skills fit cleanly into one; the ones that try to do too much straddle several and confuse the agent."

> "Verification skills have had the most measurable impact on Claude’s output quality internally. It can be worth having an engineer spend a week just making your verification skills excellent."

> "The highest-signal content in any skill is the Gotchas section. These sections should be built up from common failure points that Claude runs into when using your skill."

> "A skill that restates what Claude would do by default adds context without adding value."

> "the description field is not a summary, it's a description of when to trigger this skill."

> "But every skill that is checked in also adds a little bit to the context of the model."

> "Most of our best skills began as a few lines and a single gotcha, then got better because people kept adding to them as Claude hit new edge cases."

> "To understand how a skill is doing, we use a PreToolUse hook that lets us log skill usage within the company (example code here). This means we can find skills that are popular or are undertriggering compared to our expectations."

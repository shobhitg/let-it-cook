# let-it-cook

> Name the finish line. Then let it cook.

A claude.dev-first Claude Code plugin. The name comes from Anthropic's advice for long agent runs: give the whole task, say what done looks like, then let it work. The plugin answers "how should we do this?" questions about engineering with what Anthropic's own teams publish on [claude.dev](https://claude.dev/blog/): how code gets reviewed, approved and shipped; how to test and verify work, evals included; how to hand work to agents; how to run agents unattended; and how to measure the result. Every recommendation links to the post it came from.

## Install

In Claude Code:

```
/plugin marketplace add shobhitg/let-it-cook
/plugin install let-it-cook@let-it-cook
```

Then ask in plain words, for example "how should we gate merges now that agents write most of our code?" The `playbook` skill loads for questions about how a team builds software. You can also call it directly with `/let-it-cook:playbook`.

This is an independent project, not an Anthropic plugin; it summarizes and links to Anthropic's public posts.

## Keep it current

The skill knows the posts digested in `skills/playbook/posts/`. To pull in newer ones, open Claude Code in this repo and run:

```
/refresh
```

It reads the claude.dev RSS feed, digests each post it hasn't seen, folds new rules into the topic references, adds golden cases for them, runs the checks below, and opens a pull request for you to review. To run it without a terminal session: `claude -p "/refresh"`.

To have it run every week, create a routine from a Claude Code session in this repo with `/schedule`, a weekly time, and `/refresh` as the prompt. Each run pushes a branch for you to review and merge.

## Check it

```
python3 -I scripts/claude_dev.py fetch          # cache the source posts (gitignored)
python3 -I scripts/claude_dev.py check-quotes   # every quote appears in its post
claude plugin validate --strict .
claude plugin eval . --trust-plugin --no-publish --judge-model sonnet
```

The cases in `evals/` are golden cases: realistic questions, each graded against what its source post says, plus one ordinary coding request where the skill must stay out of the way. Each case runs with and without the plugin, so the report shows what the skill adds over the model's own knowledge.

## Layout

```
.claude-plugin/          plugin and marketplace manifests
skills/playbook/
  SKILL.md               the claude.dev-first rules and a map of topics
  references/            one file per topic, every rule linked to its post
  posts/                 one digest per claude.dev post (also the record of what's been read)
evals/                   golden cases for `claude plugin eval`
scripts/claude_dev.py    list, fetch and quote-check claude.dev posts (stdlib only)
.claude/skills/refresh/  the /refresh procedure
```

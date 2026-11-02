# let-it-cook

A Claude Code plugin with one skill, `playbook`, that answers how a team should ship, verify, hand work to agents, run agents unattended and measure the result, using Anthropic's claude.dev posts.

- `skills/playbook/SKILL.md` routes each question to `references/<topic>.md`. `posts/<slug>.md` holds one digest per claude.dev post; a digest's existence marks the post as read.
- New posts come in through `/refresh` (`.claude/skills/refresh/SKILL.md`). Follow it rather than editing digests by hand.
- Every rule in the skill traces to a post. Quotes are exact, each on its own line as `> "..."`.

## Checks

- `python3 -I scripts/claude_dev.py fetch` caches the source posts (gitignored), then `python3 -I scripts/claude_dev.py check-quotes` confirms every quote appears in its post.
- `claude plugin validate --strict .`
- `claude plugin eval . --trust-plugin --no-publish --judge-model sonnet` runs the golden cases in `evals/` with and without the plugin.

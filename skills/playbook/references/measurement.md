# Measurement: human time, reverts, incidents, cost

What Anthropic's teams do, from claude.dev. Every rule links to its post; the digests in `../posts/` hold details and exact quotes.

## Judge the engineering system by human time, guarded by reverts and incidents

- **Aim for the least human review time that doesn't raise reverts or incidents, and track both.** The Claude Code team's goal is that most PRs merge with at most one human in the loop. It tracks human approvals per PR (median and 95th percentile), human comments and how long a PR waits on a person. Human time includes fixing what bad code breaks, so a cut in review time that reappears as fixes saves nothing. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

> "Revert and incident rates are the guardrail: if they rise, we haven't saved human time, we've only moved it."

- **Measure an AI reviewer by what people do with its comments.** Sort every comment by whether the author fixed it, called it wrong, said it was intentional or decided it didn't matter; run the reviewer on PRs known to be clean and count reports that would have led to a harmful change; track rounds-to-pass alongside recall. The written priority is real bugs first, fewer review rounds second. Noise costs more when the author is an agent, because an agent fixes a nit a person would wave off. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- **Name the gap you haven't closed.** The team has no circuit breaker yet that tightens approval when revert or incident numbers move, and engineers want one before more code merges with no human. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

## Give agents a number to beat

- **Measure first; with an agent, measurement is the first step of the climb.** Pick the journeys that matter from usage data, instrument them until baselines are comparable, and have the agent estimate each planned project's gain to set targets. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))

> "As soon as Claude had a number to beat, it could start optimizing. This meant the highest-leverage thing we could do was find more things to measure."

- **Pair a deterministic lab benchmark with the user-facing metric, make it prove it tracks that metric, and ratchet it in CI.** Details in [verification.md](verification.md). ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))

## Pay for finished tasks, not tokens

- **Judge cost per finished task and price in the retry.** Every turn resends the conversation, so a model or setting that needs more turns costs more even at the same price per token, and any saving (lower effort, a smaller model, less context) that costs a finished task is lost to the retry. ([Task cost](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/))

> "A turn costs more than the tokens it adds, because it resends everything before it. So the cheapest turn is the one you don't need."

- **Give the model a way to check its work before you raise effort.** A test run costs one turn and its output; more effort adds thinking to every turn. Raise effort before switching to a bigger model, and switch when the same problem fails twice at a high level. ([Task cost](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/))
- **Measure on your own real tasks before deciding.** Run the same backlog task on each model or setting, note turns, output tokens and cost, and do three or four tasks before concluding. ([Task cost](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/))

> "The one that matters most: run one real task on each model and compare what /usage reports. Your own numbers are the ones to trust."

- **Read each finished session for three signals**: a low cache share on a long session (look for a long pause, a model switch or a tool server connected midway); a lot of output on a small change (effort too high, or retries); total input many times the conversation's size (a repeating loop). ([Task cost](https://claude.dev/blog/what-a-task-costs-on-opus-5-5/))
- **Expect the bill to follow tokens per task, not price per token**, when comparing model versions. ([Sonnet 5.5](https://claude.dev/blog/building-with-claude-sonnet-5-5/))
- **Remember parallel sessions draw on limits in parallel**: five sessions use them about five times as fast as one. ([Cloud sessions](https://claude.dev/blog/claude-code-in-the-cloud/))

## If you build agents: watch the cache like uptime

- **Alert on prompt-cache hit rate and treat cache breaks as incidents**; a few points of miss rate can change cost and latency dramatically. ([Prompt caching](https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/))

> "Monitor your cache hit rate like you monitor uptime. We alert on cache breaks and treat them as incidents."

## Results the posts report

- Merged PRs to Claude Code more than doubled from June to September while the share reverted fell by more than 40%. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))
- Real-user p75 time to a typeable claude.ai page fell from 3.1 s to 0.55 s over a two-week sprint. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))

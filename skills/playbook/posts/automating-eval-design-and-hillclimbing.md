---
title: Automating eval design and hillclimbing with Claude
url: https://claude.dev/blog/automating-eval-design-and-hillclimbing/
published: 2026-09-28
author: Lance Martin
category: Playbooks
topics: [verification, measurement, agent-design, delegation]
---

# Automating eval design and hillclimbing with Claude

**Core idea:** Build the eval from tasks that mirror production and a grader you have checked by reading scored output, then improve against it one change at a time, judging each change on held-out cases and against the eval's noise so you don't fool yourself. The post shows the claude-api skill automating both halves, with a customer-support hillclimb that raised held-out accuracy at about one fifth of the cost and a skill whose eval score rose from 66% to about 88%.

## Durable guidance
- **Draw eval tasks from what you do in production, and have a human review every input.** Tasks are sometimes picked because they are easy to generate or easy to grade, but the distribution has to represent what you actually care about. Sample in this order: production transcripts (after asking about retention and sensitive data), bug reports and support tickets, five to ten cases you write by hand, then cases synthesized from your codebase. Synthetic data can be generated from a few real examples you provide. The skill shows you every input on a page and waits until you confirm them, and you approve the grader too.
- **Pick hard cases because a human can say why they are hard, not because today's model fails them.** Cases chosen from one model's failures sample the valleys of one model's capability surface, so the eval ends up measuring that model's failure fingerprint rather than what is hard or valuable for your application. Include specific failures from production traffic, bug reports or tickets, but don't trust user traffic blindly: users try what they expect to work, so traffic alone may skew easy.
- **Use the cheapest grader that fits the output, and set up an LLM judge carefully.** Constrained outputs get code checks (exact match, a label from a fixed set, JSON that matches a schema, tests that pass). Open-ended outputs with clear quality criteria get an LLM judge that reads the input, the output and a rubric written as checkable claims, not a 1-to-5 scale, and returns a score with its reasoning. Against a baseline the judge reads both in random order without being told which is the baseline, and the judge should not be the model you are testing.
- **Read a sample of scored transcripts before you believe the grader.** Scoring failures are among the most common ways an evaluation is misconfigured. Grade a handful of cases and ask whether you would have scored any differently, and run the grader twice on the same output to see whether the verdict changes.
- **Check the eval itself before climbing it: stronger models should score higher, with headroom left.** If stronger models and more thinking don't score higher, ambiguous tasks or a miscalibrated grader are often the cause. The strongest model at top effort should land well below 100%, and the gap should not come from impossible or ambiguous tasks (a task that fails every run regardless of replicates is the tell). A good task is one where two domain experts would reach the same verdict and everything the grader checks is stated in the task. If the baseline already scores about 95% or higher, aim the hillclimb at cost or latency rather than quality.
- **Keep run-to-run variance low and infrastructure noise out of the scores.** High variance often comes from ambiguous tasks or a grader that gives different verdicts on identical output. It can also hide in configuration (effort not applied consistently) and in the environment: leftover state from an earlier trial, such as a file or git history, can hand the agent the answer. Check for timeouts, API errors and cut-off answers so infrastructure noise doesn't pass as model variance.
- **Hillclimb a surface that is cheap to change, attributable and well-scoped.** Text such as prompts and skills is easy to change and revert, while open-ended harness changes may need extensive code changes. The score should trace to the surface you edit (for skill triggering, the trigger rate is coupled to the skill description). An open-ended "improve performance" request on a near-saturated eval or a vague surface is more likely to stall. Cost is a generally strong objective: even on a saturated eval you can ask for lower cost at parity.
- **Split the cases and keep the test set unseen.** Give the hillclimber a train set it may read and a test set it never sees; train scores that rise while test scores stay flat are a common overfitting warning sign. Never paste failure content from transcripts into the prompt, and keep the answers structurally out of the model's reach, since models can "reward hack" by finding them. Harness additions that serve quirks of your eval examples (the post's example is an OCR tool added because one task benefits from it) raise the score without helping production.
- **Check the eval's noise first, and trust only gains that clear it.** Before the first round, confirm that the eval's noise (how far the score can move by chance alone) is smaller than the smallest improvement you would act on; if it isn't, add repetitions or cases. Report the test result against the baseline with confidence intervals, and if the gain is within noise, say so and recommend against merging.
- **Change one thing per round, aimed at the root cause, and revert what the test set does not confirm.** Each round proposes one patch that fixes the failing behavior at its root (rewrite the section that causes it, add a missing rule) rather than rewording a line, so its effect can show above the noise. Keep the patch only if train and test both improve; revert on a regression, or when train improves and test stays flat. Finish on the version that did best on the test set.
- **When the score stalls, sort the remaining failures by cause before editing anything.** After two or three stalled rounds, read each remaining train failure and bucket it by cause, with no edit; this surfaces ambiguous eval cases, harness errors and run-to-run variance, and only legitimate failures stay in later rounds. Start the same sorting early if no single fix could gain more than the noise. A task that never improves despite fixing the obvious content gaps is a tell that the example or grader is flawed.
- **To cut cost, hold the quality bar and step down.** Audit the prompt first (the post removed mandatory tool-call rituals, a scratchpad step and contradictory rules), then try a newer model at lower effort, then step down another tier to see whether a cheaper model also clears the bar. Cost drivers the skill considers include prompt caching, whether the prompt suits the selected model, and the choice of model and effort.

## Perishable details
- The `/claude-api build-eval` and `/claude-api hillclimb` commands belong to the claude-api skill, which ships inside Claude Code (run `claude update` first). The interview, approval pauses, local static results pages, baseline run with a confidence interval and diagnostic checks describe how they behaved when the post was written.
- The cost example ran on specific models: the baseline was Opus 4.8 at default (high) effort, then Opus 5.5 at low effort, then Sonnet 5 at low effort. Part of that saving was pricing: Opus 5.5 input and output tokens cost 20% less than Opus 4.8, and cache reads cost 60% less.
- The claude-api skill's own fixes reflect the API at the time: fixed-token-budget extended thinking, which the post says the API now rejects on recent Opus models, versus adaptive thinking; older versus current web search and web fetch tool versions; C# and Java type tables.

## Evidence
- Customer-support benchmark of 44 tickets (30 used for the search, 14 held out). The baseline, Opus 4.8 at default (high) effort, scored 74.4% decision accuracy on the search tickets at 4.6 cents per ticket.
- After a prompt audit, Opus 5.5 at low effort scored 87.8% at 1.9 cents per ticket (less than half the starting cost), and Sonnet 5 at low effort scored 88.9% at about 1 cent per ticket. Adding routing rules and a refund-cap cross-reference then brought Sonnet 5 to 98.9% at about the same cost.
- On the 14 held-out tickets that the search never saw, the final configuration scored 90.5% against the original setup's 78.6%, at about one fifth of the cost.
- claude-api skill eval, built from the documentation to test whether the skill leads to correct API code: 66% at the start; 74% after adding sections for eight missing features; 77% after fixing errors in the C# and Java type tables; 80% after adding a table near the top that maps older API forms to current ones and moving the fixed-budget-thinking warnings above the adaptive-thinking examples; about 88% after addressing a flawed task and a flawed grader (one task asked for code that catches one error type while its grader wanted a chain of at least three, and another grader's instructions contradicted the docs) plus more skill edits. The figure caption gives the endpoints as 66.1% to 87.9%.

## Quotes
> "A good task is one where two domain experts would reach the same verdict and everything the grader checks is stated in the task."

> "Pick hard cases because a human judged them hard: a useful test is to be able to say why a task is hard before you include it."

> "In general, it is important to read a sample of scored transcripts before believing your evaluator; scoring failures are among the most common ways an evaluation is misconfigured."

> "LLM-as-judge: It will default to this type of check if the output space is open-ended, with many valid answers but clear quality criteria. In this case, a second model reads the input, the output and a rubric written as checkable claims (not a 1-to-5 scale), and returns a score with its reasoning."

> "Use a train set that the hillclimber may read and a test set that is never seen. If the train set scores improve while the test set scores stay flat, then that is a common overfitting warning sign."

> "Before the first round, Claude checks that the eval's noise (how far the score can move by chance alone) is smaller than the smallest improvement you'd act on; if it isn't, it says so and suggests more repetitions or cases."

> "If the gain is within noise, it says so and recommends against merging."

> "On the 14 held-out tickets that the search never saw, the final configuration scored 90.5% against the original setup's 78.6%, at about one fifth of the cost."

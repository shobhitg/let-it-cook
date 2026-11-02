# Testing an LLM feature

> We're shipping an LLM feature that drafts replies to support tickets. How do we build tests that tell us whether a prompt change or a model upgrade made it better or worse?

Each answer comes from a fresh Claude Code session, one with let-it-cook installed and one without, in the eval run of 2026-11-02 (Claude Code 2.1.292 with its default model, graded by Sonnet). Both are shown in full and unedited, except that their headings are moved down two levels to fit this page.

**What a good answer covers**, taken from the source post rather than from the plugin:

1. Grade open-ended output with an LLM judge using a rubric of checkable pass/fail claims rather than a 1-to-5 score, and use code checks where the output is constrained.
2. Keep a held-out set of cases that prompt tuning never sees, so overfitting shows up as train scores rising while held-out scores stay flat.
3. Measure run-to-run noise by repeating runs, and only trust a change whose effect is larger than that noise.

**How often answers covered all of it:** with let-it-cook, 3 of 3 runs; without, 1 of 3.

## Without the plugin

You need an **offline eval harness**: a fixed set of real tickets, a way to score each draft, and a comparison between the current version (baseline) and the proposed one (candidate). Here's how I'd build it.

#### 1. Build the dataset from real tickets

- **Start with 100–300 real tickets**, de-identified, stratified by category: billing, bugs, how-to, refunds, angry customers, and multi-issue tickets. Weight it toward the cases that worry you, not just the common ones.
- **Store the context the model actually sees** with each ticket: retrieved KB articles, customer plan, order history. If retrieval runs live during evals, a retrieval change will look like a prompt change.
- **Attach a reference** where you can: the reply your agents actually sent and rated well, plus a few "must include / must not say" facts per ticket. These are more useful than one gold answer.
- **Add adversarial cases on purpose**: prompt injection inside the ticket body, requests for refunds the policy doesn't allow, legal threats, self-harm mentions, non-English tickets, and tickets with no answer in the KB.
- **Keep growing it.** Every bad draft found in production becomes a new test case. This matters more than anything else on the list.
- **Version the dataset** and hold back a slice you never look at while tuning prompts, so you don't overfit.

#### 2. Score in three layers, cheapest first

**a) Deterministic checks.** These are fast, free and never flaky:
- Valid format, length within bounds, correct language
- No leaked PII or internal notes, no forbidden phrases ("I guarantee", competitor names)
- Required elements present (greeting, ticket ID, the right macro or link)
- Doesn't promise things outside policy (regex or keyword lists for refund amounts, timelines)

**b) Rubric grading with an LLM judge.** Score one criterion at a time instead of asking for an overall quality score:
- **Correctness / grounding:** is every claim supported by the provided KB or context? Hallucinated policy is your highest-severity failure.
- **Resolution:** does it address *every* question in the ticket?
- **Policy compliance:** does it escalate when it should, and avoid offering what it shouldn't?
- **Tone:** empathetic, on-brand, not over-apologetic
- **Actionability:** does the customer know exactly what to do next?

Use pass/fail or a 1–4 scale with written anchors for each level, and have the judge write its reasoning before the score. Use a strong model as the judge, and keep the judge prompt and model **pinned** while you compare candidates. If the judge changes at the same time as the thing you're testing, the comparison means nothing.

**c) Pairwise comparison.** For "is B better than A?", show the judge both drafts side by side, randomize which one comes first, and run each pair in both orders. A judge detects relative differences much more reliably than it scores absolute quality.

#### 3. Validate the judge against humans

Before you trust the judge, have 2–3 support leads label about 100 drafts against the same rubric. Measure how often the judge agrees with them, per criterion. Where agreement is low (tone often is), tighten the rubric or add few-shot examples to the judge prompt. Recheck every quarter, and always after changing the judge model.

#### 4. Run it like a regression test

For every prompt or model change:
1. Generate drafts from baseline and candidate on the full set. Use temperature 0, or several samples per ticket if production uses sampling.
2. Report results **per criterion and per category**, not as one blended number. A model upgrade that raises tone scores and lowers policy compliance is a net loss.
3. **Check statistical significance.** With about 200 tickets, a 2-point swing is often noise. Use a paired bootstrap or sign test on the per-ticket differences.
4. **Gate on severity:**
   - Hard fail if any critical check regresses (hallucinated policy, PII leak, missed escalation).
   - Soft metrics need a significant win, or at least no significant loss.
5. **Diff individual drafts.** Have a human read every ticket where the two versions disagreed. Many judge errors only show up this way.

Also track cost, latency and output length. A model upgrade that writes 40% longer replies changes both agent experience and spend.

#### 5. Close the loop with production signals

Offline evals predict quality. Production tells you whether the prediction was right:
- **Edit distance** between the draft and the reply the agent actually sent. This is the best metric you have, and it's essentially free.
- Draft acceptance or discard rate, plus an explicit thumbs-down with a reason.
- Downstream outcomes: reopen rate, CSAT, escalations.
- Ship behind a flag or A/B split, so a "better" offline score is confirmed by lower edit distance before full rollout.

Feed discarded and heavily edited drafts back into the dataset (step 1).

#### Practical starting point

1. In week one, export 150 tickets with their sent replies and write about 10 deterministic checks.
2. Add a 4-criterion judge rubric and do one round of agreement checking against human labels.
3. Wire it into CI so any change to the prompt file or model config runs the eval and posts a per-category comparison table to the PR.

Promptfoo, Braintrust, LangSmith, Inspect, or a few hundred lines of Python with pytest will all do the job. The dataset and rubric matter far more than which tool you pick.

If you share your stack and how drafts are generated today, I can scaffold the harness in this repo: dataset schema, checks, judge prompt and comparison report.

## With let-it-cook

The short version: build a fixed set of real tickets that experts agree on, grade drafts with code checks where you can and a rubric-based LLM judge where you can't, measure how much scores move by chance, and only count a change as better or worse if it moves the score by more than that. The "What Anthropic's teams do" points come from posts on claude.dev. The "Beyond claude.dev" points are general practice, and I've labelled them.

#### What Anthropic's teams do

##### 1. Build the golden set from real tickets
- **Where cases come from, in order of priority:** production transcripts (once you've settled retention and PII rules), then bug reports and support escalations, then 5–10 hand-written cases, then synthetic ones. A person reviews every input. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **A case is golden only if two experts would agree on the verdict.** In the post's words: *"A good task is one where two domain experts would reach the same verdict and everything the grader checks is stated in the task."* For you, that means each case includes the facts the draft needs, such as account state, policy and order history. Don't grade a draft for knowing a refund rule it was never shown. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **Choose hard cases for reasons you can state** (angry customer, a policy edge case, a request the agent must refuse, several issues in one ticket). Don't choose them just because today's model fails them, because that only samples one model's weak spots. Real traffic alone also skews toward easy tickets. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **Turn every incident into a case.** A bad draft that reached a customer, or that an agent had to rewrite heavily, gets added once the right answer is confirmed. The Claude Code team does this with its AI reviewer and reruns the set whenever the prompt, tools or model change. ([Code review](https://claude.dev/blog/solving-code-review-at-anthropic/))

##### 2. Use the cheapest grader that works
- **Code checks for anything constrained:** the right macro or category label, required fields present, no banned phrases, a link to the correct help article, the right language, and length limits. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **An LLM judge for open-ended quality, scored against a checklist rather than a 1–5 scale.** Each item should be true or false: "states the refund amount correctly," "doesn't promise a timeline the policy doesn't allow," "answers every question the customer asked." The judge shouldn't be the model under test. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **Pairwise comparison for "is the new version better?"** Show the judge the old and new drafts in random order without saying which is which. Comparing two drafts is more reliable than scoring each one on its own. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/), [Dynamic workflows](https://claude.dev/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code/))
- **Check the judge before trusting it.** Read a sample of graded drafts yourself, and grade the same output twice to see whether the verdict changes. *"Scoring failures are among the most common ways an evaluation is misconfigured."* ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))

##### 3. Check the eval itself
- A stronger model or more thinking should score higher. The best setup should still land well below 100%. A case that fails on every run usually means the case or the grader is broken. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- Keep infrastructure failures out of the scores. Timeouts, API errors and truncated drafts must be counted as errors, not as worse model output. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- If your baseline already scores around 95%, quality is near the ceiling, so compare versions on cost or latency instead. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))

##### 4. Decide whether a change helped
- **Measure the noise first.** Run the same version several times and see how far the score moves by chance. If that's bigger than the smallest improvement you'd act on, add cases or repeats. A gain inside the noise isn't a gain, so don't ship it. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **Split the cases into a train set and a hidden test set.** Tune the prompt only against train. If train improves and test stays flat, you're overfitting. Never paste a failing ticket into the prompt to fix it. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **Change one thing per round**, and keep it only if both sets improve. ([Eval design](https://claude.dev/blog/automating-eval-design-and-hillclimbing/))
- **When upgrading the model, first remove workarounds written for the old model, then rerun the evals, then retune the effort level.** Old workarounds can hurt a newer model. ([Sonnet 5.5](https://claude.dev/blog/building-with-claude-sonnet-5-5/))

##### 5. Wire it into CI and rollout
- Put deterministic checks (policy violations, format, required content) in CI as hard gates. Once a metric improves, raise the minimum score CI accepts so a later change can't quietly undo the win. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))
- Keep a staged rollout as the last check, because offline evals miss things. ([claude.ai 3x faster](https://claude.dev/blog/how-we-made-claude-ai-faster/))

#### Beyond claude.dev (general practice)

- **Your best production signal is free: how much support agents edit a draft before sending it.** Track how often a draft is sent unchanged, how much of it changes when it is edited, and how often it's thrown away. Do this per version, behind a flag or A/B split. Use it to confirm the offline judge agrees with what agents actually accept.
- **Tag cases by category** (billing, bugs, account access, refunds, escalations, abuse) and report results per category. An upgrade can raise the average while making refunds worse, and an overall score would hide that.
- **Treat safety failures as automatic fails, not points off.** Leaking another customer's data, inventing policy, or promising refunds the policy doesn't allow should fail the case no matter how good the rest of the draft is.
- **Version everything together:** prompt, model ID, settings, retrieval/KB snapshot, judge prompt and dataset. Otherwise a change in knowledge-base content looks like a change in the model.
- **A practical starting point:** about 100–200 reviewed cases, 3 runs per case, pairwise judging against the current production version, and a pass rate per category with error bars. Grow it from there with incidents.

If you show me where the feature's code lives, I can set up the eval harness: case format, graders, a judge prompt, and a script that compares two versions.

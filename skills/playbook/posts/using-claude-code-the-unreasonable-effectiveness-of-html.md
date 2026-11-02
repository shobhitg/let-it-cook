---
title: "Using Claude Code: The unreasonable effectiveness of HTML"
url: https://claude.dev/blog/using-claude-code-the-unreasonable-effectiveness-of-html/
published: 2026-05-20
author: Thariq Shihipar
category: Playbooks
topics: [delegation, shipping, verification]
---

# Using Claude Code: The unreasonable effectiveness of HTML

**Core idea:** One Claude Code engineer has the agent write HTML instead of Markdown for specs, plans, PR explainers, reports and throwaway editors, because richer, shareable pages actually get read and keep him engaged with the agent's choices as it takes on more work. The post is explicitly his personal opinion and reports no measurements.

## Durable guidance
- **Have the agent write specs, plans, reports and PR writeups as HTML rather than Markdown.** The author says he doesn't read Markdown files past about 100 lines and can't get anyone else in his organization to. HTML can be organized with tabs, illustrations and links and can be mobile responsive, and he says the chance of someone reading a spec, report or PR writeup is much higher in HTML. An uploaded HTML file also shares as a link, while Markdown files often end up as attachments.
- **Use HTML when the content doesn't fit in prose.** It can carry tables, design data in CSS, SVG illustrations, code snippets, interactions, workflows, spatial data and images. Without it the model falls back on less efficient Markdown tricks such as ASCII diagrams or estimating colors with unicode characters.
- **Explore several options side by side before committing.** The author asks for several distinctly different approaches (varying layout, tone and density) in one HTML grid, each labeled with the tradeoff it makes. He then expands one into mockups and finally an implementation plan.
- **Give the implementing session and the verification agent the whole set of HTML files.** When he is happy with the plan he starts a new session and passes in all the exploration and plan files to implement. The verification agent reads them too, so it has much broader context on what is needed. He keeps a few HTML files for different parts or stages of the plan (an implementation plan, UI explorations, a component listing every design) instead of one plan, and keeps them as references.
- **Review and explain PRs through a rendered HTML artifact.** Ask for the actual diff with inline margin annotations color-coded by severity, focused on the part of the code you know least. Use it to understand code the agent wrote, to review code, or to explain a PR to whoever reviews yours.
- **For things that are hard to describe in text, have the agent build a throwaway editor or prototype, and end it with an export.** A single-purpose HTML file, such as draggable ticket buckets, a feature-flag editor that warns when a prerequisite is off, or sliders for tuning an animation, gets a "copy as JSON" or "copy as prompt" button. That button turns what you did in the UI back into something to paste into Claude Code or commit, so you stay in the loop and the loop gets much tighter. Claude can also sketch a design in HTML and then write it in React, Swift or another target.
- **Turn scattered context into reports and explainers.** Claude Code can pull context from the file system, MCPs such as Slack and Linear, your browser and your git history, and synthesize it into a long HTML document, an interactive explainer or a deck with SVG diagrams. The post's examples are feature summaries, weekly status reports and incident reports.
- **Know what the artifact is for, start by prompting from scratch, and build a skill later.** Simply asking for "an HTML file" or "an HTML artifact" is enough. The main thing is knowing what you want the artifact to do and how you will use it. Over time it may make sense to build a skill around recurring patterns.
- **Accept extra tokens for output people will actually read.** Markdown often uses fewer tokens, but the author finds that HTML's expressiveness and the much higher likelihood of him reading it give better output overall.
- **Pick output formats that keep a human engaged with the agent's choices.** The author's stated real reason for HTML is that as Claude took on more he noticed he was reading plans less closely, and he wanted a way to stay engaged with its choices rather than hand them off. He says he feels more in the loop now than ever.

## Perishable details
- The author says HTML's extra token use is not really noticeable in the 1MM context window of Opus 4.7, so whether the cost trade-off holds depends on the model and context size.
- The post leans on product specifics: Claude Design is built on HTML, Claude in Chrome and MCPs feed Claude Code context, and it argues Claude Code beats Claude.ai or Claude Design for this because of how much context it can ingest.

## Evidence
- None. The post is one author's personal experience and says so; its only figure is his own habit of not reading Markdown files longer than about 100 lines.

## Quotes
> "I’ve found that I tend to not actually read more than a 100-line Markdown file, and I certainly am not able to get anyone else in my organization to read it."

> "The chance of someone actually reading your spec, report, or PR writeup is much higher if it’s in HTML."

> "When I’m happy with the plan I’ll create a new session and pass in all of these files for it to implement."

> "When verifying I’ll also ask the verification agent to read in the files and it will have much broader context on what is needed."

> "The trick is always to end with an export: a "copy as JSON" or "copy as prompt" button that turns whatever I did in the UI back into something I can paste into Claude Code or commit to a file. You stay in the loop, but the loop gets much tighter."

> "While Markdown often uses fewer tokens, I’ve found that the added expressiveness of HTML and the much higher likelihood of me reading it means I get overall better output."

> "As Claude takes on more, I'd noticed I was reading plans less closely, and I wanted a way to stay engaged with its choices rather than just hand them off."

> "I’ve found that instead of having a single plan, I tend to have a few different HTML files for different parts/stages of the plan."

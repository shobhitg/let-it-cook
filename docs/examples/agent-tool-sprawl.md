# An agent with too many tools

> We're building an internal agent and the team keeps adding a new tool for every capability. It's at 40 tools and getting worse at picking the right one. What should we do?

Each answer comes from a fresh Claude Code session, one with let-it-cook installed and one without, in the eval run of 2026-11-02 (Claude Code 2.1.292 with its default model, graded by Sonnet). Both are shown in full and unedited, except that their headings are moved down two levels to fit this page.

**What a good answer covers**, taken from the source post rather than from the plugin:

1. Keep a high bar for adding a tool, because every tool is one more option the model has to weigh.
2. Add capability through progressive disclosure instead: files or skills the agent reads only when needed, or a subagent that does the searching in its own context and returns only the answer.

**How often answers covered all of it:** with let-it-cook, 3 of 3 runs; without, 3 of 3.

## Without the plugin

Adding a tool for every capability is a common way agents get worse at picking tools. Every tool's schema sits in context on every request, and similar-looking tools compete with each other. Here's what I'd do, in priority order.

#### 1. Consolidate first

Most 40-tool sets are really 8–15 tools that got split too finely. Audit the list for:

- **Same action on different objects.** `get_user`, `get_order`, `get_invoice` → `lookup(entity_type, id)`. One well-described tool with an enum parameter is easier to pick than five near-duplicates.
- **Same verb, different variants.** `search_docs`, `search_docs_by_date`, `search_docs_by_author` → one `search_docs` with optional filters.
- **Read-only tools that could be one general tool.** If many tools just fetch data, a single query or code-execution tool may cover them.
- **Tools nobody uses.** Log which tools are actually called. The long tail often accounts for under 5% of calls and is where most selection mistakes happen.

A useful rule: **keep a capability as its own dedicated tool only when the harness needs to do something specific with it.** That means gating it behind approval (sends, deletes, external writes), rendering a custom UI, auditing it, or marking it safe to run in parallel. If none of those apply, it can probably be a parameter on an existing tool.

#### 2. Fix the descriptions

When the model picks the wrong tool, the cause is often the descriptions, not the number of tools:

- Say **when to use this tool and when not to**: "Use for X. For Y, use `other_tool` instead." This matters most for pairs that overlap.
- Make names distinct and specific. Two tools whose names differ by one word will get confused.
- Put an enum or a short example on any parameter the model tends to fill in wrong.
- Set `strict: true` so arguments always match the schema.

#### 3. Use tool search when you still have many tools

If you still have dozens of tools after consolidating, and each request needs only a few, use the **tool search** server tool:

- Add `tool_search_tool_bm25_20251119` (or the `_regex_` variant).
- Mark the rarely used tools `defer_loading: true`. Keep the 3–5 core tools loaded.
- Claude searches the tool catalog and loads only the schemas it needs. Loaded schemas are appended to the context, so the prompt cache stays valid. Swapping tool lists per request would invalidate it.
- You can't defer every tool. The search tool and at least one other tool must stay loaded, or the API returns a 400.

This keeps the starting context small without taking capabilities away.

#### 4. Separate tools from instructions

Often a new tool is really "how to do task X," and the description has grown into a page of instructions. Move that guidance into **Skills**. Only a short description stays in context, and the full instructions load when a task needs them.

#### 5. Split by domain if the work divides cleanly

If the tools fall into clear groups (billing, infra, CRM…), have a top-level agent hand work to **subagents** that each get only their own group's tools. Each one picks from about 8 tools instead of 40.

#### 6. Measure before and after

Build a small eval set: around 50 real requests, each labeled with the right tool or tools. Score how often the agent picks correctly. Without it you can't tell whether consolidating helped, and the next new tool will quietly make things worse again. It's also worth agreeing as a team that adding a new tool requires showing it doesn't lower that score.

**My recommendation:** start with #1 and #2. They usually fix most of the problem and cost nothing. Add tool search only if you're still above roughly 15–20 tools afterward. If you send me the tool list (names and descriptions), I can suggest specific merges and flag the overlapping pairs. If you tell me your language, I can also write the tool-search setup.

## With let-it-cook

The core problem is that every new tool is one more option the model has to weigh on every turn. Stop adding tools by default, cut the 40 down, and add new capabilities in ways that don't put another tool in front of the model at the start.

#### What Anthropic's teams do

**1. Set a high bar for adding a tool.** Claude Code has about 20 tools, and its team still regularly asks whether it needs all of them. In their words: *"The bar to add a new tool is high, because this gives the model one more option to think about."* ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))

**2. Add capabilities with progressive disclosure instead of new tools.** Two ways they do this:
- **Deferred tools:** only a name or short description is loaded at first. The full schema loads when the agent searches for it.
- **Skills:** packaged instructions that point to other files and get loaded only when relevant. Many of your "one tool per capability" cases are probably a general tool (an HTTP call, a query, a script runner) plus know-how about how to use it. That know-how fits in a skill.

*"Progressive disclosure is now a common technique we use to add new functionality without adding a tool."* ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/), [Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/))

**3. Use subagents for bulky or specialized areas.** If a group of tools only matters for one area (docs lookup, billing, infra), give those tools to a subagent. The subagent works in its own context and returns only the answer, so the main agent sees one entry point instead of eight tools. ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))

**4. Fit tools to what the model can do, and merge where it makes sense.**
- Each tool should ask for one thing. Don't build tools that ask for two things at once.
- Use expressive parameters, such as an enum of statuses or modes, plus one clear instruction, instead of several near-duplicate tools or long example lists. With current models, examples tend to limit what the model tries.
- Put usage instructions once, in the tool description.
- Read transcripts to confirm the model actually understands how to call each tool.

([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/), [Context engineering](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/))

**5. Let the agent find its own context.** Some of your tools may exist only to fetch or pre-chew data. Claude Code moved from handing the model retrieved snippets to letting it search for itself. A few general search and read tools can replace many narrow fetchers. ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))

**6. Revisit tools as models improve.** *"As model capabilities increase, the tools that your models once needed might now be constraining them."* Some of the 40 were probably workarounds for older models. ([Seeing like an agent](https://claude.dev/blog/seeing-like-an-agent/))

**7. Keep the tool set fixed within a session.** If you start loading tools dynamically, defer their loading rather than adding or removing them mid-session. Changing the tool list breaks the prompt cache. Model state changes like "plan mode" as tools, not as a swap of the tool set. ([Prompt caching](https://claude.dev/blog/lessons-from-building-claude-code-prompt-caching-is-everything/))

#### Beyond claude.dev (general practice)

- **Measure before cutting.** Build a small eval set of real requests, each labeled with the correct tool or tools, and track how often the agent picks right. Then cut or merge tools and confirm the number goes up rather than guessing.
- **Audit the current 40.** For each tool, check how often it's actually called, which tools it gets confused with, and whether a general tool plus a skill could cover it. Overlapping names and descriptions are usually where selection goes wrong.
- **Change the team process.** A new tool should need a short justification: why a skill, a parameter on an existing tool, or a subagent won't work. Otherwise the count will just climb back up.

A realistic target is under 20 tools always loaded. The rest become deferred tools, skills or subagent-owned areas, with your eval set showing whether selection accuracy actually improved.

# CLAUDE.md

This file is the contract for any LLM working in this repository: what the repo is, how it is
structured, and the functions that operate it. What the repo *contains* is `index.md`'s job;
what's on the owner's plate is `dashboard.md`'s: **read both at every session start, and follow
the dashboard's header.**

> **Fresh clone?** If `index.md` doesn't exist yet, this repo hasn't been born: read
> `playbooks/bootstrap.md` and build it *with the owner* before doing anything else.

## 1. What this is
A personal knowledge base whose job is **context**: it holds what the LLM needs to be a helpful
assistant to the owner. The LLM also maintains it: the repo grows from conversations and the
owner's projects, and stays current and well-formed under the rules below, with the owner ruling
on judgment calls. Not a software project — plain Markdown, read both by agent tools and in
Obsidian (hence `[[wikilinks]]`).

- **Budget ~200 lines.** This file is loaded every session: keep it to what *every* session
  needs. Task-scoped guidance goes in a playbook (`playbooks/`); when a change would push past
  the budget, compress before extending.
- **Confidential:** the repo is personal data (identity, finances, health, family) —
  never publish, export, or paste contents into external systems without explicit owner approval.
- **Working style:** concise and direct. For open-ended or structural decisions, lead with a
  reasoned recommendation in prose, not a menu of options.

## 2. Structure
Content comes in two kinds:
- **Knowledge:** what the owner has learned or is learning, from study and work: durable concept
  notes that grow by cross-linking and never carry deadlines. As context, what the owner knows
  (their skill set) and how they think: explanations build on it and skip what it covers, and tasks
  that draw on it (a resume, a design, a target role's gaps) cite it; the gaps and the plans to
  close them are operational notes.
- **Operations:** what the owner runs: goals, processes, deadlines, next actions, in volatile notes
  that feed `dashboard.md` and go stale without maintenance. As context, the owner's actual
  situation, goals and decisions; a recorded decision isn't reopened unless the facts behind it
  changed.

Keep the wall between them: concepts (ideas that stay true) go in knowledge notes; processes
(steps, dates, status) go in operational notes. Each top-level **domain** folder holds one kind, a
knowledge or an operational domain; which domains exist right now is `index.md`'s job.

Alongside the domains sit four infrastructure folders this file defines: `functions/` (the
procedures of the functions beyond the baseline three, §5), `playbooks/` (the rules for one
recurring kind of work each), `log/` (the change log) and `in-progress/` (work under construction:
§2 In progress). Read a playbook before starting its work, together with the notes that work draws
on (the instance's operational notes, the knowledge it builds on); its rules add to this file's and
take precedence where they conflict.

**In progress (`in-progress/`):** the construction site for work with an exit (an active course, a
large ingestion, a parked multi-session task): a note, or a sub-folder with its own index for a
cluster, each with a banner stating the exit plan and a dated dashboard line for the exit. It is
exempt from the content gate and right-sizing (§3) but keeps its frontmatter, which its root line
copies; a single note is fine, and the folder goes when empty. At the exit, durable knowledge
refactors into permanent notes and the work is deleted.

## 3. Notes
**Format gate.** Every note (every `.md` file except this one, `AGENTS.md` and `README.md`) is
Markdown with this YAML frontmatter, and nothing more:

```yaml
---
title: <human title>
description: <one short line on what it owns (what's inside, not a summary), no ": " in it>
updated: YYYY-MM-DD
---
```

- **Dates** are absolute `YYYY-MM-DD`. In the frontmatter, `updated` is set to today (from
  environment context) on every content edit — never guess; a frontmatter-only sweep (retiring or
  backfilling a field) leaves it. In the body, a date belongs when it is part of the fact (a
  deadline, an event such as a filing or an approval, a settled call that shouldn't be reopened),
  and a fact that can change (a rule, a cutoff, a fee) carries `(verified: YYYY-MM-DD)`, the day it
  was last checked at source. When something was decided or written stays out: provenance lives in
  the log.
- **Right-sizing:** check a note as it passes **~200, 500 and 800 lines** (then every 300): two
  or more separate topics → split into linked notes (update the index); one long topic → keep it
  whole and record the check with `<!-- size checked: N -->` under the title.

**Content gate (quality bar):** capture the *ideas, intuition, and practical relevance* — not a
transcript; clean up obvious errors; stay faithful to the source. Keep what will recur: the
decisions made and where the owner disagreed (and why), not just conclusions; in knowledge notes,
the owner's own angle (intuitions, what confused them, links to their work), the part no LLM can
supply. Figures become text; code goes in fenced blocks. Write plainly: concise, plain words.

## 4. Indexing
**Used by:** Read (§5), to find a note; Update (§5), to file one: where it goes and what it's
named, whether a folder is created or split, which index lines change; Lint, to check the repo
against this section.

**Standard:** every note is reachable by following indexes down from `index.md` (the root, then
each sub-folder's index): few hops, each index short enough to scan, each line enough to choose
by. The rules below are the specific ways to meet it; where they don't settle a case, judge the
case against the standard.

**Indexes:** each maps one folder, one line per direct item (note or sub-folder), nothing deeper.
Other files (scripts, assets) aren't items: each sits beside the note that uses it and is linked
from it; a script is named after its note. Every folder with 2+ items has exactly one, named after
the folder (e.g. `ai/nlp/nlp.md`), with two exceptions:
- **Root index (`index.md`):** indexes the repo root *and* every top-level folder (none but
  `log/` has its own), so it runs two levels: each top-level folder, then its direct items.
  Budget ~100 lines.
- **`log/`:** the active log `log/log.md` is its index; the root links it, never lists it.

**Index lines:** `[[note]] — <its description>`, copied verbatim from the note's frontmatter (a
sub-folder's description lives in its index note's frontmatter, and its line copies that; a
top-level folder gets a bare heading in the root, with no description). An index is a map,
never a second source of truth: it changes **only** when an item is added, removed, renamed, or its
description changes. Status lives in the note, what's due on the dashboard.

**Names:** notes and folders, lowercase kebab-case, unique across the repo (wikilinks resolve
by name, and a folder's index takes its name).

The folder rules below are for the content folders, the domains. The infrastructure folders are
the four §2 defines; these rules don't apply to them.

**Hierarchy — how to propose structure:**
- **By subject, not by source:** folders follow how the owner looks for things, never by course,
  book or post (a course's material files into the subjects it teaches).
- **Names predict contents:** a folder's name, with its index line, should let a session predict
  whether a given note is inside: the subject's plain name, specific enough to route by, broad
  enough for what's coming (`language-tests/`, not `toefl/`); never a catch-all (`misc/`, `other/`).
- **Siblings don't overlap:** a folder's sub-folders split it into distinct subtopics; each note
  lives in the one it's mainly about and links to the rest.

**When to create or split:**
- **Created only with content:** a folder, at any level (a new domain included), is created only
  when there's content to file: never speculatively, never empty, and never for a single note
  (that only adds a level). New folders, splits and moves are proposed; the owner rules.
- **A domain's top level holds at most ~7 items**; past that, group notes into sub-folders,
  keeping at the top only the notes a session should see first (e.g. its fact base, its main
  plan).
- **Below the top level,** a folder is checked for a split as it passes ~15 items.
- **Moves, renames and merges:** a folder that drops to one note folds into its parent (its index
  goes); a move updates both indexes and rewrites path mentions in text (wikilinks survive, since
  names are unique); renaming a note or a heading rewrites every link and § pointer to it (one text
  search for `[[old-name` or `§Old heading`; the log keeps its old links).

## 5. Functions
Three baseline functions — **Read**, **Update**, **Close** — written out here. Other functions
get a one-line pointer here and are read only when that work starts.

**Read — find and use knowledge.** Start at `index.md` and follow the indexes down; read what the
answer needs and no more — a text search of the repo (e.g. `grep`) only when the indexes don't
resolve it. Ground answers in what's actually written, never generic, using each kind as §2
describes; cite each note the answer draws on (not every note opened) as repo path + § heading
(e.g. `career/job-search.md` §Pipeline), with the `verified:` date of any fact the answer
rests on that can change.

**Update — add or change knowledge** — when the owner asks, and unasked whenever the conversation
produces something worth keeping. Test: *would a future session answer differently because of
this?* (e.g. a changed operational fact, a decision + its why, a synthesis, feedback on how to
work). Facts and the owner's decisions → file directly; the LLM's own interpretations → offer
first; skip explorations that reached no conclusion, and hypotheticals. **Rule text (`CLAUDE.md`,
`playbooks/`, `functions/` with its scripts, the dashboard's and the log's headers) changes only
with the owner's explicit approval:** feedback on how to work becomes a proposed edit, never a
silent one. For source material (a document, a lecture), discuss the key takeaways before writing.

Every update:
- **Filing:** one home per fact — extend the note that owns the topic, or create one (wired into
  its index) if none does; elsewhere, link to that home instead of restating the fact.
  `[[wikilink]]` related notes to each other.
- **Editing:** update in place over appending duplicates; preserve the owner's own wording; don't
  fabricate facts — leave a `_(to fill)_` blank. If new information *contradicts* the note, stop
  and re-confirm with the owner before overwriting.
- **Gates:** pass both gates (format, content; §3) and the indexing rules (§4); if the edit
  changed what the note owns, rewrite its `description` and the index line that copies it.
- **Copies:** when a fact changes, search the repo for its old value and key terms (e.g. a
  number, a date, a name) and rewrite every place that still states it or a conclusion drawn
  from it, until no old version remains.
- **Dashboard:** keep `dashboard.md` current per its header.
- **Edit report:** end the reply with a standalone report: a bold `Edit report` label, then the
  task's `log/log.md` entry quoted as a `>` blockquote (entry text only, without the `## `
  marker), then the commit hash on its own line. On an amend-in-place, quote only what was added
  or reworded this round, verbatim, and note that the rest is unchanged. An unsealed mid-task
  update reports the notes touched and a one-liner the same way. Don't narrate the log and
  commit steps.

**Close — seal a task.** A task gets one `log/log.md` entry, and a **commit + push** (message
mirroring the entry) at each milestone: a finished step (e.g. a reviewed section, a ruled batch of
decisions), the task landing, or a pause. Not per edit or approval; never held for an unrelated
open question; never leave work uncommitted or unpushed at a pause. Each later milestone, or a
reopened task, **amends the entry in place** and commits again. Log entry, **a sentence or two when
fresh**: `## [YYYY-MM-DD] <op> | [[notes touched]] — one-liner` (`<op>` from the log header's
list), saying *what changed and the decision/why*, never the detail (it's in the notes) or the diff
(it's in git). Each amendment appends as an indented `Amend:` line of a sentence or two; an amended
entry may outgrow that, but never re-compress it. The active log holds the current quarter; at
quarter close, sweep it to `log/log-YYYY-qN.md`.

**Lint — repo health:** is the repo well-formed (links, indexes, sizes)? → `functions/lint.md`.

**Reflect — priorities review:** progress against the priorities, and should they change? →
`functions/reflect.md`.

Lint and Reflect are **owner-triggered only — never run unprompted** (a due dashboard line
raises them; the owner says go).

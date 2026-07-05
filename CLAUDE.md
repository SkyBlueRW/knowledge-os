# CLAUDE.md

This file is the contract for any LLM working in this repository: what the repo is, how it is
structured, and the functions that operate it. What the repo *contains* is `index.md`'s job —
start there and drill down.

> **Fresh clone?** If `index.md` doesn't exist yet, this repo hasn't been born: read
> `tools/bootstrap.md` and build the vault *with the owner* before doing anything else.

## 1. What this is
A personal knowledge base and the owner's acting assistant — not a software project. Everything
is plain Markdown, authored and edited mostly *by the LLM on the owner's behalf*, and read both
by agent tools and in Markdown editors such as Obsidian (hence `[[wikilinks]]`). Current
priorities live in `dashboard.md`, the owner's front page; `AGENTS.md` is a symlink to this
file so every tool picks up the same contract.

- **Budget ~150 lines.** This file is loaded every session: keep it to what *every* session
  needs. Task-scoped guidance goes in a `tools/` playbook with one routing line here; when a
  change would push past the budget, compress before extending.
- **Working style:** concise and direct. For open-ended or structural decisions, lead with a
  reasoned recommendation in prose, not a menu of options.
- **Advising the owner:** ground advice in their notes and actual goals — never generic.

## 2. Structure
Top-level folders are **domains**, and each serves one of the repo's two purposes:
**knowledge domains** hold what the owner studies — timeless concept notes that grow by
cross-linking and never carry deadlines; **life domains** hold what the owner runs — goals,
processes, deadlines, next actions — they feed `dashboard.md` and go stale without maintenance.
Keep the wall between them: a process is not a concept. Which domains exist right now is
`index.md`'s job.

Both kinds share **one vault** deliberately: the repo is private, and what the owner learns
stays linked from their goals as evidence — don't split it. New domains get created **only when
there's content to file** — never speculatively, never empty. Alongside the domains sit two
infrastructure folders this file defines: `tools/` (functions + playbooks; registry
`tools/tools.md`) and `log/` (the change log).

**Indexes (recursive rule):** every folder with **2+ notes** has an index note named after the
folder (root: `index.md`; domain: `<domain>.md`). An index is a *thin catalog*: one
`[[wikilink]]`ed line per note plus a line per sub-folder index — a map, never a second source
of truth. The hierarchy mirrors the folder tree; update the index whenever notes are added or
removed.

**Format gate.** Every note is Markdown with YAML frontmatter — nothing more is required; a
note's kind and role follow from where it sits and what it's named:

```yaml
---
title: <human title>
tags: [domain/subtopic]   # optional — only for a second axis the folder can't express
status: active | staging | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

- **Dates** are absolute `YYYY-MM-DD`; set `updated` to today (from environment context) on
  every edit — never guess the date.
- **Filing:** one home per fact — extend the note that owns the concept, or create one (wired
  into its index) if none does; never state the same fact in two places. `[[wikilink]]` related
  notes to each other.
- **Right-sizing:** a note that passes **~200 lines** or grows a second distinct concern splits
  into linked notes (update the index).
- **Editing:** update in place over appending duplicates; preserve the owner's own wording;
  don't fabricate personal facts — leave blanks. If new information *contradicts* the note,
  stop and re-confirm with the owner before overwriting.

**Content gate (quality bar):** capture the *ideas, intuition, and practical relevance* — not a
transcript; clean up obvious errors; keep it right-sized; stay faithful to the source;
cross-link liberally. Keep what will recur: the decisions made and where the owner disagreed
(and why), not just conclusions. In practice: a `## Contents` TOC for long notes, figures
converted to text, code in fenced blocks.

**Staging (work in progress):** any in-progress effort (an active course, a large ingestion, a
draft cluster) can get a temporary staging folder: index note with `status: staging` and a
banner stating the exit plan; deliberately **unwired from the permanent indexes**, and exempt
from both gates while active. Staging is a loan, not a home — at the end, durable knowledge is
refactored into proper notes in the permanent structure and the folder is deleted; transient
scaffolding goes with it.

## 3. Functions
Three baseline functions — **Read**, **Update**, **Close** — written out here. Everything else
is reached by name + link and read on use; the registry `tools/tools.md` lists them all.

**Read — find and use knowledge.** Start at `index.md` (or `dashboard.md` for what's on the
owner's plate) → domain index → the one note; read the least that answers — `grep` only when the
indexes don't resolve it. Ground answers in what's actually written and cite the notes used. A
Read that produces a real synthesis (a comparison, a connection, an analysis) becomes a
**passive Update** — offer to file it, so explorations compound instead of dying in chat.

**Update — add or change knowledge.** Two modes:
- *Active:* the owner directs content in — for source material, discuss key takeaways before
  writing.
- *Passive:* the conversation surfaces something durable — test: *would a future session answer
  differently because of this?* (a changed life fact, a decision + its why, a synthesis,
  collaboration feedback). Objective facts → update directly; interpretations → offer first;
  skip unconcluded explorations and hypotheticals; a contradiction with the target note → stop
  and re-confirm (per Editing).

Every update: file per the Filing rule; pass both gates (§2); update the domain index; if a
life note changed, refresh its `dashboard.md` pointer (the dashboard is a map — status, next
action, deadline, link, 1–2 lines per item — never a second copy); **end with a one-line report
in the reply — what changed → which note** — so the owner can judge correctness.

**Close — seal a task.** At task close, not per edit (a session may close several tasks): one
`log/log.md` entry + one **commit + push**, message mirroring the entry — never leave work
uncommitted or unpushed (the push is the only backup). Log entry — **1–2 lines**:
`## [YYYY-MM-DD] <op> | [[notes touched]] — one-liner`; the one-liner says *what changed and the
decision/why* — never the detail (in the notes) or the diff (in git). The active log holds the
current quarter; at quarter close sweep to `log/log-YYYY-qN.md` (the active log itself is
`log/`'s folder index).

**Lint — repo health.** Is the repo well-formed? The script detects (links, indexes, sizes),
the LLM remediates, judgment calls go on a punch-list the owner rules on → `tools/lint/lint.md`.

**Reflect — priorities review.** Reads `dashboard.md` (stated priorities) + the log since the
last reflect (what got done); suggests next steps per priority and discusses whether the
priorities should change; the owner rules → `tools/reflect.md`.

Both **owner-triggered only — never run unprompted.**

## 4. Playbooks — read before starting that kind of work
- **Bootstrap** (fresh repo → working vault, run once — retires itself when done) →
  `tools/bootstrap.md`.
- **Ingest** (absorb existing material — a folder, an export, a project) → `tools/ingest.md`.
- *Add the owner's own playbooks here as they emerge — one routing line each, procedure in
  `tools/`. Anything that recurs and has rules qualifies: course notes, the owner's writing
  voice, meeting prep, a weekly review.*

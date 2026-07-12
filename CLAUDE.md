# CLAUDE.md

This file is the contract for any LLM working in this repository: what the repo is, how it is
structured, and the functions that operate it. What the repo *contains* is `index.md`'s job —
start there and drill down.

> **Fresh clone?** If `index.md` doesn't exist yet, this repo hasn't been born: read
> `tools/bootstrap.md` and build the vault *with the owner* before doing anything else.

## 1. What this is
A personal knowledge base and the owner's acting assistant — not a software project. Everything
is plain Markdown, authored and edited mostly *by the LLM on the owner's behalf*, and read both
by agent tools and in Obsidian (hence `[[wikilinks]]`). Current priorities live in
`dashboard.md`, the owner's front page; `AGENTS.md` is an explicit pointer file to this
contract (not a symlink — those don't survive Windows checkouts) so every tool reads the same rules.

- **Budget ~150 lines.** This file is loaded every session: keep it to what *every* session
  needs. Task-scoped guidance goes in a `tools/` playbook with one routing line here; when a
  change would push past the budget, compress before extending.
- **Confidential:** the vault is personal data (identity, finances, health, family) — never
  publish, export, or paste contents into external systems without explicit owner approval.
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

Both kinds share **one vault** deliberately: the repo is private, and learning stays linked
from the owner's goals as evidence — don't split it. New domains get created **only when
there's content to file** — never speculatively, never empty. Alongside the domains sit two
infrastructure folders this file defines: `tools/` (functions + playbooks; registry `tools/tools.md`) and `log/` (the change log).

**Indexes (recursive rule):** every folder with **2+ notes** has an index note named after the
folder (root: `index.md`; domain: `<domain>.md`). An index is a *thin catalog*: one
`[[wikilink]]`ed line per note plus a line per sub-folder index — a map, never a second source
of truth. The hierarchy mirrors the folder tree. An index changes **only** when a note is
added, removed, renamed, or its stable one-line role changes — never for content or status
updates; a role line says what the note *owns*, posture lives on the dashboard.

**Format gate.** Every note is Markdown with YAML frontmatter — nothing more is required; a
note's kind and role follow from where it sits and what it's named:

```yaml
---
title: <human title>
tags: [domain/subtopic]   # optional — only for a second axis the folder can't express
status: active | staging | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
verified: YYYY-MM-DD      # optional, volatile life notes only: external claims last checked
review_after: YYYY-MM-DD  # optional: past this date, recheck the source before relying
---
```

- **Dates** are absolute `YYYY-MM-DD`; set `updated` to today (from environment context) on
  every edit — never guess. `updated` = the file changed; `verified` = claims rechecked at source.
- **Filing:** one home per fact — extend the note that owns the concept, or create one (wired
  into its index) if none does; never state the same fact in two places. `[[wikilink]]` related
  notes to each other.
- **Right-sizing:** a note that passes **~200 lines** or grows a second distinct concern splits
  into linked notes (update the index).
- **Editing:** update in place over appending duplicates; preserve the owner's own wording;
  don't fabricate personal facts — leave blanks. No ruling-dates in note bodies — provenance
  lives in the log; an inline date only when the date itself is the content (a deadline, an
  as-of fact, a don't-relitigate anchor). If new information *contradicts* the note,
  stop and re-confirm with the owner before overwriting.

**Content gate (quality bar):** capture the *ideas, intuition, and practical relevance* — not a
transcript; clean up obvious errors; keep it right-sized; stay faithful to the source;
cross-link liberally. Keep what will recur: the decisions made and where the owner disagreed
(and why), not just conclusions. In practice: a `## Contents` TOC for long notes, figures
converted to text, code in fenced blocks.

**Staging (work in progress):** any in-progress effort (an active course, a large ingestion, a
draft cluster) can get a temporary staging folder: index note with `status: staging` and a
banner stating the exit plan; deliberately **unwired from the permanent indexes**, and exempt
from both gates while active. Staging is a loan, not a home — at the end, durable knowledge
refactors into permanent notes, and the folder (with its scaffolding) is deleted.

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

Every update: file per the Filing rule; pass both gates and the index rule (§2); a changed
volatile fact → grep its old wording across life domains, indexes, dashboard and rewrite
every projection (old and new conclusions must never co-exist); if a life note changed,
**rewrite** its `dashboard.md` pointer — replace the bullet, never append to it (the
dashboard is a map — a **now / next / parked** posture tag leads each actionable item;
*parked* names what brings it back + at most a few-word why — an **external**-event trigger
also carries an absolute recheck-by date, since no session watches the world: a date fires,
"until X happens" doesn't; then next action, deadline, link, 1–2 lines per item — never a
second copy); **end the reply with a standalone report, visually set off: a bold
`Edit report` label, the task's `log/log.md` entry quoted as a `>` blockquote (entry text
only — drop the `## ` marker, it renders as a huge heading), commit hash on its own line** —
never woven into prose; the fixed label is what makes it instantly recognizable (the entry
already names the notes and the what/why, and quoting it lets the owner veto the permanent
record while the turn is warm); **on an amend-in-place, quote only the portion added or
reworded this round** — verbatim, never paraphrased — noting the remainder unchanged (it's
already-audited record). An unsealed mid-task update reports notes + a one-liner the same way.
No padding with log/commit mechanics.

**Close — seal a task.** At task close — not per edit, and **never batched to session end** (a
session may close several tasks): one `log/log.md` entry + one **commit + push**, message
mirroring the entry — never leave work uncommitted or unpushed (the push is the only backup).
The unit of Close is the **task, not the turn**: seal when a task lands and attention moves
on — never hold a seal on an unrelated open question; if the next turns reopen the same task,
**amend its log entry in place** and commit again (git records the drafts, the log records
settled tasks). Log entry — **1–2 lines when fresh**: `## [YYYY-MM-DD] <op> | [[notes touched]] — one-liner`;
the one-liner says *what changed and the decision/why* — never the detail (in the notes) or the diff (in git).
Amendments append, **each delta itself 1–2 lines**: an amended entry may grow past the
guideline by accretion — never re-compress it (that rewrites already-audited record and buries
the delta the owner audits). The active log holds the current quarter; at quarter close sweep
to `log/log-YYYY-qN.md` (the active log itself is `log/`'s folder index).

**Lint — repo health.** Is the repo well-formed? The script detects (links, indexes, sizes),
the LLM remediates, judgment calls go on a punch-list the owner rules on → `tools/lint/lint.md`.

**Reflect — priorities review.** Reads `dashboard.md` (stated priorities) + the log since the
last reflect (what got done); suggests next steps per priority and discusses whether the
priorities should change; the owner rules → `tools/reflect.md`.

Both **owner-triggered only — never run unprompted.**

## 4. Playbooks — read before starting that kind of work
- **Bootstrap** (fresh repo → working vault; run once — retires itself when done) → `tools/bootstrap.md`.
- **Ingest** (absorb existing material — a folder, an export, a project) → `tools/ingest.md`.
- *The owner's own playbooks go here as they emerge — one routing line each, procedure in
  `tools/`: anything that recurs and has rules (course notes, writing voice, a weekly review).*

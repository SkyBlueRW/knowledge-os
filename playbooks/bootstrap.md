---
title: Bootstrap — First Session, Fresh Clone to Working Repo
description: the first session on a fresh clone (introduce, read what exists, ask what's needed, build, retire the installer)
updated: 2026-11-08
---

# Bootstrap — First Session

Turns this seed into the owner's repo, **in conversation**: introduce, read what already exists,
ask only the necessary questions, build. Run once: if `index.md` already exists, the repo is born;
stop and use the normal functions instead (`CLAUDE.md` §5).

**Ground rules for the whole session:** one thing at a time, at the owner's pace; this is a
conversation, not a form. Never fabricate: what the owner doesn't say (or confirm) stays blank.
Use their wording. Create a domain **only when the session produced content for it**: no empty
folders for "later".

## 1. Introduce (brief)
Tell the owner what this repo becomes and how it's used, in a few sentences: *a private repo
holding what you know (knowledge: concept notes that grow by linking) and what you run
(operations: goals, deadlines, next actions), maintained by the LLM on your behalf; you talk, it
files, links and commits.* Give 2–3 concrete use cases so it clicks: tracking an application or
visa process end to end; course or study notes that compound; asking "what's on my plate?" and
getting an answer from your own notes; every session opening with what's due. Confirm the repo is
(or will be) **private** before any personal fact is written.

## 2. Start from what exists
Ask: **"Is there anything I should read first: a resume or CV, a notes folder, an export, a
project directory?"**
- If yes: read it (**read-only**, never touch the originals) and play back what was learned as
  **inferences to confirm, not facts**, since documents go stale ("this says you're at X doing Y,
  still current?"). Corrections and confirmations become the seed content.
- Keep the first session bounded: survey enough to inform the questions below and seed the repo.
  A **large source** (a whole vault, years of notes) gets its full treatment in a follow-up
  [[ingest]] session (`playbooks/ingest.md`): note the source and move on.
- If no: skip; the questions below carry the whole load.

## 3. Ask the necessary questions
Walk the areas below, **skipping whatever step 2 already answered** and confirming what it
implied. Let the owner skip freely.
- **Identity** → `about-me.md` at the root: who they are, what they do, where; what the next
  couple of years should look like; the 3–5 facts an assistant should *always* know.
- **What they run (operations):** work or career (role, direction) · any application or legal
  process underway (licensing, visas, a move: these are deadline machines) · learning with stakes
  (a degree, an exam, a certification) · health, finance or family projects. For each area
  engaged: the goal, current status, next action, any hard date. Group into 1–3 operational
  domains (fewer is better).
- **What they know (knowledge):** what they study, or want organized knowledge on. Create a
  knowledge domain only if real content emerged; otherwise leave it for the first actual note.
- **Rank:** play back the operational areas and ask the owner to rank them. Record the ranking
  *they* settle on; [[reflect]] tests it against reality later.

## 4. Build (all files in one pass, then review together)
- **`about-me.md`:** identity, goals, the always-relevant facts.
- **The notes the session produced,** one per distinct concern (goal, status, next action,
  dates). Folders follow `CLAUDE.md` §4: a domain gets its folder at its second note (until then
  its one note sits at the root), and sub-folders wait until a domain's top level passes ~7 items.
- **`dashboard.md`:** fill the shipped skeleton per its header. Priorities: the owner's ranking,
  each → its owning note. Dated: each time-sensitive item, dated by when to raise it. Recurring:
  `Lint (every 2 wks) → [[lint]]`, `Reflect (monthly) → [[reflect]]` and `Log sweep to
  log/log-YYYY-qN.md (quarterly) → [[log]]`, each dated to its first check-in.
- **`index.md`:** the root index per `CLAUDE.md` §4. Frontmatter; the root notes (`about-me`,
  `dashboard`, any lone domain note); `## Knowledge domains` and `## Operational domains`, each
  folder under a bare heading (`### career/`) with its items under it; `## Infrastructure` with
  `playbooks/` and `functions/`. Link `[[log]]`, don't list it. Every line copies its note's
  `description`.
- **`log/log.md`:** keep the shipped header; bootstrap is its first entry (`create`).
- Every note passes the format gate: `title`, `description`, `updated`, each value plain YAML
  (no `: ` inside).

Walk the owner through what was built; fix wording they object to on the spot.

## 5. Verify and seal
- Run `python3 functions/lint.py` (Windows: `python functions\lint.py`). A fresh bootstrap should
  come out clean; fix what doesn't, and never create filler to silence a check.
- **Retire the installer (confirm first).** The repo is born; the installation material has done
  its job and would only mislead later sessions. Tell the owner what gets removed and get their OK,
  then: delete this file and its line in `index.md`; drop the fresh-clone banner from `CLAUDE.md`;
  drop the Bootstrap row and the Upgrading section from the README, and rewrite its top (intro and
  Quickstart) as the front door of *this* repo (what it is, whose it is, how to talk to it),
  keeping the usage examples and the how-it-works reference, with one line crediting the
  [knowledge-os](https://github.com/SkyBlueRW/knowledge-os) seed. If the owner declines, leave
  everything: the run-once guard keeps a re-run safe.
- **Close** (`CLAUDE.md` §5): log entry, commit, push. Confirm the remote is set up and
  **private**: the push is the only backup.
- Point the owner at the rhythm from here: talk to the LLM as things happen (Update); each session
  opens with what's due on the dashboard; point it at new material as it appears ([[ingest]]);
  lint and reflect come up on the dashboard and run when the owner says go.

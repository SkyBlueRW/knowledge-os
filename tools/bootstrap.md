---
title: Bootstrap — First Session, Fresh Repo → Working Vault
status: active
created: 2026-07-04
updated: 2026-07-04
---

# Bootstrap — First Session

Turns this seed into the owner's vault, **in conversation** — introduce, read what already
exists, ask only the necessary questions, build. Run once: if `index.md` already exists, this
repo is born; stop and use the normal functions instead (CLAUDE.md §3).

**Ground rules for the whole session:** one thing at a time, at the owner's pace — this is a
conversation, not a form. Never fabricate: what the owner doesn't say (or confirm) stays
blank. Use their wording. Create a domain **only when the session produced content for it** —
no empty folders for "later."

## 1. Introduce (brief)
Tell the owner what this repo becomes and how it's used, in a few sentences: *a private vault
holding what you study (knowledge domains: timeless concept notes) and what you run (life
domains: goals, deadlines, next actions), maintained by the LLM on your behalf — you talk, it
files, links, and commits.* Give 2–3 concrete use cases so it clicks: tracking an application
or visa process end-to-end; keeping course or study notes that compound; asking "what's on my
plate?" and getting an answer from your own notes; a periodic "reflect" that checks what you
did against what you said mattered. Confirm the repo is (or will be) **private** before any
personal fact is written.

## 2. Start from what exists
Ask: **"Is there anything I should read first — a resume or CV, a notes folder, an export, a
project directory?"**
- If yes: read it (**read-only** — never touch the originals) and play back what was learned
  as **inferences to confirm, not facts** — documents go stale ("this says you're at X doing
  Y — still current?"). Corrections and confirmations become the seed content.
- Keep the first session bounded: survey enough to inform the questions below and seed the
  vault. A **large source** (a whole vault, years of notes) gets its full treatment in a
  follow-up [[ingest]] session (`tools/ingest.md`) — note the source and move on.
- If no: skip — the questions below carry the whole load.

## 3. Ask the necessary questions
Walk the areas below, **skipping whatever step 2 already answered** and confirming what it
implied. Let the owner skip freely.
- **Identity** → `profile/about-me.md`: who they are, what they do, where; what the next
  couple of years should look like; the 3–5 facts an assistant should *always* know.
- **What they run (life domains):** work/career (role, direction) · any application or legal
  process underway (immigration, licensing, visas — these are deadline machines) · learning
  with stakes (degree, exam, certification) · health / finance / family projects. For each
  area engaged: the goal, current status, next action, any hard date. Group into 1–3 life
  domains (fewer is better).
- **What they study (knowledge domains):** what they're learning or want organized knowledge
  on. Only create a knowledge domain if real content emerged; otherwise leave it for the
  first actual note.
- **Rank:** play back the life areas and ask the owner to rank them. Record the ranking
  *they* settle on; reflect (CLAUDE.md §3) will test it against reality later.

## 4. Build (all files in one pass, then review together)
- `profile/about-me.md` — identity, goals, the always-relevant facts.
- One folder per life domain that has content: a domain index + the notes the session
  produced (goal, status, next action, dates — one note per distinct concern).
- Knowledge domains only where content emerged.
- `dashboard.md` — the front page: ranked priorities, time-sensitive items (soonest first,
  with dates), each line pointing to its owning note. A map, never a second copy.
- `index.md` — the root index: one line per domain index, plus `dashboard`, `log`, `tools`.
- `log/log.md` — the change log (header per CLAUDE.md §3 Close), with bootstrap as its first
  entry.
- Every note passes the format gate (frontmatter, real dates) — CLAUDE.md §2.

Walk the owner through what was built; fix wording they object to on the spot.

## 5. Verify and seal
- Run `python3 tools/lint/lint.py` — a fresh bootstrap should come out clean; fix what
  doesn't.
- **Close** (CLAUDE.md §3): log entry + commit + push. Confirm the remote is set up and
  **private** — the push is the only backup.
- Point the owner at the rhythm from here: talk to the LLM as things happen (Update), point
  it at new material as it appears ([[ingest]]), ask for **lint** occasionally (health), ask
  for **reflect** when they want a priorities check.

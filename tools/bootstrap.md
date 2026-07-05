---
title: Bootstrap — First Session, Fresh Repo → Working Vault
status: active
created: 2026-07-04
updated: 2026-07-04
---

# Bootstrap — First Session

Turns this seed into the owner's vault, **in conversation** — the LLM interviews, the owner
answers, the LLM files. Run once: if `index.md` already exists, this repo is born; stop and use
the normal functions instead (CLAUDE.md §3).

**Ground rules for the whole session:** one area at a time, at the owner's pace — this is a
conversation, not a form. Never fabricate: what the owner doesn't say stays blank. Use their
wording. Create a domain **only when the interview produced content for it** — no empty folders
for "later."

## 1. Orient (2 minutes)
Tell the owner what this repo becomes, in two sentences: *a private vault holding what you
study (knowledge domains: timeless concept notes) and what you run (life domains: goals,
deadlines, next actions), maintained by the LLM on your behalf* — and that this session builds
the starting structure from a short interview. Confirm the repo is (or will be) **private**
before any personal fact is written.

## 2. Interview — identity
Who they are, in the dimensions that will matter for advising them later: name, what they do,
where they are, what the next couple of years are supposed to look like. Ask for the 3–5 facts
they'd want an assistant to always know. → drafts `profile/about-me.md`.

## 3. Interview — what they run (life domains)
Walk the common areas one at a time and let them skip freely: **work/career** (current role,
direction), **any application or legal process underway** (immigration, licensing, visas —
these are deadline machines), **learning with stakes** (a degree, an exam, a certification),
**health / finance / family projects** — anything with a goal, a deadline, or a next action.
For each area the owner engages with, get: the goal, the current status, the next action, and
any hard date. Group what emerged into 1–3 life domains (fewer is better; a domain earns a
folder only with content).

## 4. Interview — what they study (knowledge domains)
What they're learning or want organized knowledge on. If they have existing notes elsewhere,
don't migrate now — note the source and plan a follow-up [[ingest]] session (`tools/ingest.md`;
a large ingestion is **staging** work, CLAUDE.md §2). Only create a knowledge domain if real
content came out of the conversation; otherwise leave it for the first actual note.

## 5. Rank priorities
Play back the life areas and ask the owner to rank them. Disagreement and "it depends" are
fine — record the ranking *they* settle on; reflect (CLAUDE.md §3) will test it against
reality later.

## 6. Build (all files in one pass, then review together)
- `profile/about-me.md` — identity, goals, the always-relevant facts.
- One folder per life domain that has content: a domain index + the notes the interview
  produced (goal, status, next action, dates — one note per distinct concern).
- Knowledge domains only if §4 produced content.
- `dashboard.md` — the front page: ranked priorities, time-sensitive items (soonest first, with
  dates), each line pointing to its owning note. A map, never a second copy.
- `index.md` — the root index: one line per domain index, plus `dashboard`, `log`, `tools`.
- `log/log.md` — the change log (header per CLAUDE.md §3 Close), with bootstrap as its first
  entry.
- Every note passes the format gate (frontmatter, real dates) — CLAUDE.md §2.

Walk the owner through what was built; fix wording they object to on the spot.

## 7. Verify and seal
- Run `python3 tools/lint/lint.py` — a fresh bootstrap should come out clean; fix what doesn't.
- **Close** (CLAUDE.md §3): log entry + commit + push. Confirm the remote is set up and
  **private** — the push is the only backup.
- Point the owner at the rhythm from here: talk to the LLM as things happen (Update), ask for
  **lint** occasionally (health), ask for **reflect** when they want a priorities check.

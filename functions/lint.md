---
title: Lint — Repo Health Check
description: repo health check (links, indexes, sizes)
updated: 2026-11-08
---

# Lint — Repo Health Check

The repo's hygiene function. **Division of labor: the script detects, the LLM remediates, the
owner rules on judgment calls.** Detection is deterministic and token-free; quota is spent only on the
fixes that need judgment. Priorities review (next steps, stated-vs-revealed effort) is a
separate function — [[reflect]] — not part of lint.

## Invocation
- **"lint"** → tier 1 only.
- **"lint \<domain\>"** (e.g. "lint career") → tier 1 + tier 2 scoped to that folder.
  Repo-wide tier 2 is discouraged — run it one domain at a time to bound the cost.

## Tier 1 — mechanical (script-detected)
Run the read-only detector (always exits 0; prints a Markdown report):

```bash
python3 functions/lint.py   # macOS / Linux
python functions\lint.py    # Windows (python3 usually doesn't exist there)
```

Thirteen checks: frontmatter (exactly `title`, `description`, `updated` in strict flat key-value
grammar, each value plain YAML: no `: ` or ` #` inside, no quotes or reserved first character; empty, duplicate, malformed or retired keys are defects; missing descriptions listed by
folder) · inline `(verified: …)` dates (real, not in the future) · broken wikilinks (near-match
suggestions; a link to a deleted or renamed note) + duplicate basenames · dangling-placeholder
tally (ranked; repeated danglers = note-creation candidates) · orphan notes (log-timeline links
don't count as inbound) · index sync per CLAUDE.md §4 (the root lists every top-level folder's
direct items and links `log/`; each deeper folder with 2+ items has its index listing its direct
items; index lines link only direct items and copy descriptions verbatim; no index file in a
top-level folder; root over ~100 lines) · names (lowercase kebab-case notes and folders) · folder
census, domains only (top level over ~7 items, a deeper folder past ~15, single-note folders) ·
oversize notes (a note passing an unchecked size checkpoint, ~200 / 500 / 800, then every 300 — 2+
topics → split; one long topic → keep it and record `<!-- size checked: N -->` under the title;
`in-progress/` exempt; CLAUDE.md >200) · dashboard hygiene (>50 lines; a `-` line not led by
`YYYY-MM-DD · `; an item over one line; items out of date order within a section; due/overdue
lines; past dates mid-line; a `§section` pointer with no matching heading) · in progress (every
item has a dashboard line) · path mentions (a backticked repo path that no longer exists: moved, or
another repo's) · temporal integrity (>1 dated Status block in a note).

## Tier 2 — content health (LLM-read, per domain)
Read the domain's notes and look for:
- the same concept explained in 2+ notes (candidates for one shared atomic note);
- quality-bar drift — transcript-like notes, or a note grown a second distinct concern;
- missing cross-links between obviously related notes;
- claims that look superseded or stale (especially ones depending on the outside world);
- status or timing leaking into a `description` (and so its index line): a description says what
  a note owns; status lives in the note, what's due on the dashboard;
- the wall: deadlines or steps inside a knowledge note, or a concept explained inside an
  operational note;
- provenance dates in a note body (when something was decided or written: that lives in the log);
- a fact that can change (a rule, a cutoff, a fee) without its `(verified: YYYY-MM-DD)`.

## Flow (both tiers)
1. Run the script; read the report.
2. **Triage:** fix trivially mechanical items directly (link typos, missing index lines,
   malformed frontmatter); a missing `description` is drafted and offered, since it reads what a
   note owns. Everything needing judgment goes on a short **ranked punch-list**, each
   item with a recommendation — fix / split / merge / create / delete / **do nothing** (the
   thresholds are look-triggers, not obligations).
3. **Present the punch-list to the owner before applying — hard rule.** The owner rules; apply
   what they approve.
4. A surfaced contradiction is usually a genuinely new circumstance, a drift in the owner's
   preferences, or a slipped long-term value — **name which, and log it**. Lint is a reflection
   pass, not just hygiene.
5. Roll the dashboard's `Lint` line forward two weeks, then finish with a **Close** (`op: lint`) —
   one log entry + commit + push, per CLAUDE.md.

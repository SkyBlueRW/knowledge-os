---
title: Lint — Repo Health Check
status: active
created: 2026-07-04
updated: 2026-07-15
---

# Lint — Repo Health Check

The repo's hygiene function. **Division of labor: the script detects, the LLM remediates, the
owner rules on judgment calls.** Detection is deterministic and token-free; quota is spent only
on the fixes that need judgment. Priorities review (next steps, stated-vs-revealed effort) is a
separate function — [[reflect]] — not part of lint.

## Invocation
- **"lint"** → tier 1 only.
- **"lint \<domain\>"** (e.g. "lint health") → tier 1 + tier 2 scoped to that folder.
  Repo-wide tier 2 is discouraged — run it one domain at a time to bound the cost.

## Tier 1 — mechanical (script-detected)
Run the read-only detector (always exits 0; prints a Markdown report):

```bash
python3 tools/lint/lint.py   # macOS / Linux
python tools\lint\lint.py    # Windows (python3 usually doesn't exist there)
```

Ten checks: frontmatter validity (strict flat key-value grammar: empty required values, duplicate
keys, and malformed block lines are defects; incl. the optional `verified`/`review_after` fields) · broken
wikilinks (near-match suggestions) + duplicate basenames · dangling-placeholder tally (ranked;
repeated danglers = note-creation candidates) · orphan notes (log-timeline links don't count as
inbound) · index sync incl. parent wiring, on exact parsed link targets (staging subtrees
informational) · oversize notes (>200 lines; CLAUDE.md >150; long permanent notes also flagged if missing a `## Contents` TOC) · dashboard hygiene (past dates;
bullets >2 lines — the map rule) · staging inventory · folder census (>10 notes, or single-note
folders) · temporal integrity (expired `review_after`; >1 dated Status block in a note).

## Tier 2 — content health (LLM-read, per domain)
Read the domain's notes and look for:
- the same concept explained in 2+ notes (candidates for one shared atomic note);
- quality-bar drift — transcript-like notes, or a note grown a second distinct concern;
- missing cross-links between obviously related notes;
- claims that look superseded or stale (especially ones depending on the outside world);
- volatile posture or satisfied timing triggers leaking into permanent index role lines (a role
  line says what a note *owns*; posture lives on the dashboard).

## Flow (both tiers)
1. Run the script; read the report.
2. **Triage:** fix trivially mechanical items directly (link typos, missing index lines,
   frontmatter fields). Everything needing judgment goes on a short **ranked punch-list**, each
   item with a recommendation — fix / split / merge / create / delete / **do nothing** (the
   thresholds are look-triggers, not obligations).
3. **Present the punch-list to the owner before applying — hard rule.** The owner rules; apply
   what they approve.
4. A surfaced contradiction is usually a genuinely new circumstance, a drift in the owner's
   preferences, or a slipped long-term value — **name which, and log it**. Lint is a reflection
   pass, not just hygiene.
5. Finish with a **Close** (`op: lint`) — one log entry + commit + push, per CLAUDE.md.

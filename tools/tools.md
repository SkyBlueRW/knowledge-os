---
title: Tools — Repo Functions
status: active
created: 2026-07-04
updated: 2026-07-04
---

# Tools — Repo Functions & Playbooks

Registry of the repo's operational docs, deliberately **tool-agnostic**: any LLM reaches one via
CLAUDE.md → this registry → the doc. Invoke in plain language ("run lint", "reflect", "bootstrap
me"); no tool-specific mechanism (slash commands, skills) is required. Two kinds:

## Functions — procedure (+ script where earned)
- [[bootstrap]] — first session on a fresh clone: introduce → read the owner's existing
  material if any (inferences played back to confirm) → ask the necessary questions → build
  `about-me`, the first domains, `dashboard.md`, `index.md`, `log/` → lint → Close. Run once;
  ends by retiring itself and the install-facing docs (owner-confirmed).
- [[ingest]] — absorb existing material (a folder, an export, a project): survey → map played
  back → enriching interview (still true? which version? what was the why?) → staged if large →
  decomposed into proper notes. The source stays read-only.
- [[lint]] (`tools/lint/`) — repo health check. `lint.py` detects (tier 1: deterministic,
  token-free); the LLM remediates and runs the per-domain tier-2 content pass; punch-list is
  presented before fixes; the owner rules on judgment calls.
- [[reflect]] — priorities review, on demand: read the dashboard (stated priorities) + the log
  since the last reflect (what got done) → suggested next steps + a priorities discussion,
  owner rules. No script (evidence fits in context).

## Playbooks — pure procedure, read before starting the task
*None yet — they emerge from the owner's recurring work.* When a kind of task recurs and has
rules (course notes, the owner's writing voice, meeting prep, a weekly review), write the
procedure here as `tools/<name>.md`, list it in this section, and add one routing line to
CLAUDE.md §4.

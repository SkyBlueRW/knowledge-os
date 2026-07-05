---
title: Ingest — Absorb Existing Material
status: active
created: 2026-07-04
updated: 2026-07-04
---

# Ingest — Absorb Existing Material

Brings a pre-existing body of material into the vault — a folder of documents, a Notion or
Obsidian export, a project directory, old course notes. **Interrogate, don't copy:** the source
is evidence to question, and the vault gets the distilled result — ideas, decisions, and the
why — never a pasted transcript. Runs any time after bootstrap, and again whenever a new source
appears.

**Ground rules:** the source is **read-only** — never edit or delete the owner's originals.
What the owner doesn't confirm stays unfiled or blank; never fabricate context around old
material. New domains only when the source actually produces content for them.

## 1. Survey
Read the source and play back a **map of what was found** before writing anything:
- the topics and clusters it contains, and which are substantial vs thin;
- overlaps (the same thing said in several places — which copy looks authoritative?);
- claims that look **stale** or superseded, especially ones about the outside world;
- what seems **missing** — referenced but absent, or obviously incomplete;
- proposed destinations: which existing domains it feeds, and any new domain it would justify.

The owner corrects the map before anything is filed.

## 2. Interview — enrich what the source can't say
Old material records conclusions; the valuable context usually isn't written down. Ask,
cluster by cluster:
- *"This says X — is it still true?"* (stale claims get updated or dropped, not imported)
- *"These overlap — which is the version you trust?"*
- *"There's a decision here — what was the reasoning, and did you ever disagree with it?"*
- *"What do you actually reach for from this pile? What's dead weight?"*

The answers — the why, the corrections, the owner's own wording — are what makes the ingested
notes better than the source.

## 3. Stage or file
- **Small source** (a few notes' worth): file directly into the proper domains per the normal
  Update function.
- **Large source:** create a **staging folder** (CLAUDE.md §2) with `status: staging` and an
  exit plan in its banner; work through it across sessions at the owner's pace. Staging is a
  loan — the folder is deleted at the end.

## 4. Decompose
Durable content becomes proper notes in the permanent structure, passing both gates
(CLAUDE.md §2): one home per fact, right-sized, cross-linked; concepts land in knowledge
domains, anything with a goal / deadline / next action lands in a life domain and gets a
`dashboard.md` pointer. Binaries (PDFs, slides) may sit alongside notes where useful, but the
notes must stand without them.

## 5. Verify and seal
Run `python3 tools/lint/lint.py`; wire every new note into its index; **Close** (log entry +
commit + push). For a multi-session staging ingest, Close each session and log the staging
exit when the folder is deleted.

---

*Adopting an existing vault wholesale (e.g. a live Obsidian vault that should itself become
this repo) is the same procedure with the vault as source — survey, interview, then migrate
cluster by cluster through staging rather than all at once.*

---
title: Reflect — Priorities Review
status: active
created: 2026-07-04
updated: 2026-07-04
---

# Reflect — Priorities Review

**Read the dashboard (stated priorities) and the log (what actually got done), then: suggest
next steps, and discuss whether the priorities should change.** Ends in a conversation with the
owner ruling — never batch fixes. Boundary with [[lint]]: lint asks *is the repo well-formed*;
reflect asks *is the life content still true and honestly prioritized*.

**Owner-triggered only, on demand — no fixed cadence.**

## Inputs (no script — evidence fits in context)

1. `dashboard.md` — the stated priorities and their next actions.
2. `log/log.md` entries **since the last `reflect` entry** (span into the `log-YYYY-qN.md`
   archives if needed; if reflect has never run, the owner names the window).

## The pass

1. **What got done.** Cluster the window's log entries by domain/priority — the picture of
   where effort actually went.
2. **Next steps.** For each dashboard priority, given what's now done: what's the highest-
   leverage next action? Confirm, sharpen, or replace the next actions listed.
3. **Priority discussion.** Where stated order and demonstrated effort diverge, ask *which is
   wrong — the order or the effort?* Dashboard items with no log movement in the window and no
   deferred marker get the same question: still real, or delete / defer explicitly? Recommend
   a re-ranking if the evidence supports one; the owner rules.

While reading, flag (don't fix) external claims that look stale — rules, rates, thresholds,
processing times due for re-verification.

**The log is a proxy, not a record.** It captures what touched the *repo*; real effort can
leave no entries. A silent domain has two readings — nothing happened, or the notes are
behind — and reflect asks which, rather than concluding "no progress." One answer is a
priority question, the other a capture gap to backfill.

## Output

A short agenda — **cap ~5 items**, each: *evidence → question → recommended next step*, the
owner rules. The agenda is ephemeral (lives in the conversation, not a note). **No edits during
the run**; accepted recommendations become ordinary Updates afterwards.

## Verdicts (what persists)

- Each verdict is filed **into the owning note** — dashboard reorder, next-action change,
  re-verification task — per the normal Update function.
- A consciously parked item gets the marker **`(deferred — revisit <absolute date or YYYY-Qn>)`**
  on its dashboard line, so later reflects skip it until then. Use sparingly.
- One `reflect` log entry records the verdicts (it also anchors the next run's window);
  then Close.

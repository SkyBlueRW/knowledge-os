# knowledge-os

A seed for a **knowledge base run by an LLM**: your notes, your goals, your deadlines, in plain
Markdown, maintained by an AI agent on your behalf. The repo is the agent's long-term context, and
the agent keeps it current.

This is not a template of empty folders to fill in. It's the **operating contract and tools** your
LLM reads to build *your* repo: clone it, open an agent CLI, and the first session is an
interview. The LLM asks about your life and work, then creates your profile, your domains, your
dashboard and your change log from the conversation.

## Quickstart

**You need:** git and a GitHub account (or any private git host) · an agent CLI installed and
logged in ([Claude Code](https://claude.com/claude-code) requires a subscription; any agent that
reads files and runs git works) · Python 3 for the lint script.

1. **Create a private repo from this template** (GitHub: *Use this template*, or clone and
   re-init). **Private matters:** this repo will hold your real life.
2. Open an agent CLI in the repo. [Claude Code](https://claude.com/claude-code) reads `CLAUDE.md`
   natively; other tools pick up the same contract via `AGENTS.md`, a pointer file that routes
   them to it.
3. Say: **"Read CLAUDE.md and bootstrap me."** It introduces itself, asks if you have existing
   material to start from (a resume, a notes folder, a project), then asks only the questions that
   material didn't answer. Skip freely.
4. From then on, just talk to it as things happen. It files, links and commits; you rule.

## What using it looks like

After bootstrap, the interface is just telling your agent things, in the repo, as they happen. A
week might contain:

- *You open a session.* Before your task, it raises what the dashboard dates today or earlier
  ("the visa renewal packet is due Friday"), then gets on with what you asked.
- *"Passed the certification exam, results came in this morning."* It files the fact in the
  owning note, clears or re-dates the dashboard line, commits. You're done.
- *"What's on my plate this week?"* It answers from your dashboard and your actual notes, citing
  them: not from memory, not generically.
- *"Compare the two apartment options we discussed."* It answers, then offers to file the
  comparison so the thinking isn't lost when the chat ends.
- *"I've got a folder of old notes from my degree."* Point it there: **ingest** surveys the
  material, asks you what's still true and which version to trust, and files the distilled result
  (see [`playbooks/ingest.md`](playbooks/ingest.md)).
- *"Run lint."* A health check: it fixes the mechanical, you rule on the judgment calls.
- *"Reflect."* It compares what you said matters against what actually got done, and comes back
  with next steps and honest questions about your priorities.

Two facts make the delegation comfortable: every change ends with a short report you can veto,
and everything is git, so nothing it does is unrecoverable.

## How it works

- **`CLAUDE.md` is the contract,** the one file loaded every session: what the repo is, its
  structure, how notes are written and indexed, and the functions that run it. Everything else is
  read on demand.
- **Two kinds of content.** *Knowledge* is what you know: concept notes that grow by
  cross-linking and never carry deadlines. *Operations* is what you run: goals, processes,
  deadlines, in notes that feed the dashboard and go stale without upkeep. A wall keeps them
  apart, so each gets the right upkeep. The same split works for a work repo: your field, and
  your projects.
- **Indexes built for finding.** Every note is reachable by following indexes down from
  `index.md`, and each index line copies the note's own one-line description, so the agent picks
  the right note without opening the wrong ones. Text search is the fallback.
- **Location over metadata.** Frontmatter is three fields: `title`, `description`, `updated`.
  Work under construction lives in `in-progress/` instead of carrying a status, and a fact that
  can change carries its own `(verified: date)`.
- **A dated dashboard, no scheduler.** Each line points to its note and is dated by when to raise
  it. Every session raises what's due, and lines are updated in the same turn as the decision.
  It's plain instructions, so it works in any agent tool.
- **Sealed at milestones.** Each task gets one log entry, amended as the task grows, and a
  commit and push at each milestone. The log is the memory of *why*; git is the memory of *what*.

## Layout

```
CLAUDE.md        the contract (AGENTS.md routes other tools to it)
index.md         the map of the repo, built at bootstrap
dashboard.md     what's due, by date
about-me.md      who you are, built at bootstrap
<your domains>/  knowledge and operations folders, created as content arrives
functions/       lint (with lint.py) and reflect, run when you say so
playbooks/       the rules for one kind of work each: bootstrap, ingest, then your own
in-progress/     work under construction, each item with an exit (created when needed)
log/             the change log
```

## The functions

| Function | What it does |
|---|---|
| **Read** | Answers from your notes: follows the indexes down from `index.md` and cites what it used. |
| **Update** | Files what changes, when you say so or when a conversation surfaces something worth keeping. |
| **Close** | Seals a task: one log entry, a commit and push at each milestone. |
| **Lint** | [`functions/lint.md`](functions/lint.md): a script detects (links, index drift, sizes, dashboard dates), the LLM fixes the mechanical, you rule on judgment calls. |
| **Reflect** | [`functions/reflect.md`](functions/reflect.md): what you said matters (dashboard) vs what got done (log), then next steps. On your command. |
| **Bootstrap** | [`playbooks/bootstrap.md`](playbooks/bootstrap.md): the first session on a fresh clone. Runs once, then retires itself and rewrites this README as your repo's front door. |
| **Ingest** | [`playbooks/ingest.md`](playbooks/ingest.md): absorbs existing material (a folder, an export, a project) through a survey, an enriching interview, then distilled notes. |

All of it is tool-agnostic plain Markdown: no plugins, no proprietary format. It works with any
agent that can read files and run git, and Obsidian reads it too (hence the `[[wikilinks]]`).

## Upgrading from v0

v0 (July 2026) kept its procedures in `tools/`, called operations "life domains", staged work
with a `status` field, and had no `description`. To upgrade a v0 repo:

1. Copy in this release's `CLAUDE.md`, `functions/` and `playbooks/ingest.md`. Move your own
   playbooks from `tools/` into `playbooks/`, then delete `tools/`.
2. Replace the headers of `dashboard.md` and `log/log.md` with this release's (they're rule text).
3. Ask your agent: **"Run lint and migrate this repo to v1."** Lint flags each retired frontmatter
   field with what replaced it, every missing `description`, undated dashboard lines and index
   drift. The agent fixes the mechanical items, drafts descriptions for you to skim, and asks
   before moving anything (a staging folder becomes `in-progress/`).

## Privacy

The repo this seed grows will contain personal facts. Keep it **private**, and know what your
agent tooling sends where. The `.gitignore` excludes local agent settings by default.

## License

MIT, see [LICENSE](LICENSE).

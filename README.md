# knowledge-os

A seed for a **personal knowledge base run by an LLM** — your notes, your goals, your
deadlines, in plain Markdown, maintained by an AI agent on your behalf.

This is not a vault of empty folders to fill in. It's the **operating contract and tools** your
LLM reads to build *your* vault: clone it, open an agent CLI, and the first session is an
interview — the LLM asks about your life and work, then creates your profile, your domains,
your dashboard, and your change log from the conversation.

## Quickstart

**You need:** git and a GitHub account (or any private git host) · an agent CLI installed and
logged in — [Claude Code](https://claude.com/claude-code) requires a subscription; any agent
that reads files and runs git works · Python 3 for the lint script.

1. **Create a private repo from this template** (GitHub: *Use this template*, or clone and
   re-init). **Private matters** — this repo will hold your real life.
2. Open an agent CLI in the repo — [Claude Code](https://claude.com/claude-code) reads
   `CLAUDE.md` natively; other tools pick up the same contract via the `AGENTS.md` symlink.
3. Say: **"Read CLAUDE.md and bootstrap me."** It introduces itself, asks if you have
   existing material to start from (a resume, a notes folder, a project), then asks only the
   questions that material didn't answer. Skip freely.
4. From then on, just talk to it as things happen. It files, links, and commits; you rule.

## What using it looks like

After bootstrap, the interface is just telling your agent things — in the repo, as they
happen. A week might contain:

- *"Passed the certification exam — results came in this morning."* → It files the fact in
  the owning note, refreshes the dashboard, commits. You're done.
- *"What's on my plate this week?"* → It reads your dashboard and answers from your actual
  notes, citing them — not from memory, not generically.
- *"Compare the two apartment options we discussed."* → It answers, then offers to file the
  comparison so the thinking isn't lost when the chat ends.
- *"I've got a folder of old notes from my degree."* → Point it there: **ingest** surveys the
  material, asks you what's still true and which version to trust, and files the distilled
  result — see [`tools/ingest.md`](tools/ingest.md).
- *"Run lint."* → Health check; it fixes the mechanical, you rule on the judgment calls.
- *"Reflect."* → It compares what you said matters against what actually got done, and comes
  back with next steps and honest questions about your priorities.

Two facts make the delegation comfortable: every change ends with a one-line report you can
veto, and everything is git — nothing it does is unrecoverable.

## How it works

- **`CLAUDE.md` is the contract** — the one file loaded every session. It defines the
  structure, the quality gates, and the functions. Everything else is read on demand.
- **Two kinds of domains, one vault.** *Knowledge domains* hold what you study — timeless
  concept notes that never carry deadlines. *Life domains* hold what you run — goals,
  processes, next actions; they feed `dashboard.md` and go stale without maintenance. The wall
  between them is the design's load-bearing idea: a process is not a concept.
- **Thin indexes.** Every folder with 2+ notes gets a one-line-per-note index. Indexes are
  maps, never second copies — the LLM navigates by drilling down, not by grepping blindly.
- **Everything is sealed.** Each finished task ends with a 1–2 line log entry and a
  commit + push. The log is the repo's memory of *why*; git is the memory of *what*.

## The functions

| Function | What it does |
|---|---|
| **Bootstrap** | First session on a fresh clone: intro → read what you have → necessary questions → working vault. Run once. |
| **Ingest** | Absorb existing material (a folder, an export, a project): survey → enriching interview → distilled notes. |
| **Read** | Answer from the notes: index → domain → note; cite what was used. |
| **Update** | File what changes — directed by you, or offered when a conversation surfaces something durable. |
| **Close** | Seal a task: log entry + commit + push. |
| **Lint** | Health check: a script detects (broken links, index drift, oversize notes), the LLM fixes, you rule on judgment calls. |
| **Reflect** | Priorities review: what you said matters (dashboard) vs what actually got done (log) → next steps, on your command. |

Procedures live in [`tools/`](tools/tools.md); the LLM reads them on use. All of it is
tool-agnostic plain Markdown — no plugins, no proprietary format, works with any agent that can
read files and run `git`.

## Privacy

The vault this seed grows will contain personal facts. Keep the repo **private**, and know
what your agent tooling sends where. The `.gitignore` excludes local agent settings by
default.

## License

MIT — see [LICENSE](LICENSE).

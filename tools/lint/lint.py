#!/usr/bin/env python3
"""Tier-1 lint detector for the knowledge repo.

Read-only: scans the repo's Markdown notes and prints a grouped Markdown
report. Detection only — remediation is judgment work done by the LLM and
the owner (procedure: tools/lint/lint.md). Always exits 0.
"""

import re
import subprocess
from collections import Counter, defaultdict
from datetime import date
from difflib import get_close_matches
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[2]

REQUIRED_KEYS = ("title", "status", "created", "updated")  # tags optional
STATUSES = {"active", "staging", "archived"}
NO_FRONTMATTER = {"CLAUDE.md", "AGENTS.md", "README.md"}  # contract (+ symlink) + repo front page
ORPHAN_EXEMPT = {"index", "dashboard", "log", "CLAUDE", "AGENTS", "README"}
MAX_NOTE_LINES = 200
MAX_CLAUDE_MD_LINES = 150  # CLAUDE.md's own budget
MAX_FOLDER_NOTES = 10

WIKILINK = re.compile(r"\[\[([^\]|#\n]+)(?:#[^\]|\n]*)?(?:\|[^\]\n]*)?\]\]")
ISO_DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
MONTH_NAMES = (
    "January|February|March|April|May|June|July|August|September|October|"
    "November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec"
)
MDY = re.compile(rf"\b({MONTH_NAMES})\.?\s+(\d{{1,2}}),?\s+(\d{{4}})\b")
DMY = re.compile(rf"\b(\d{{1,2}})\s+({MONTH_NAMES})\.?,?\s+(\d{{4}})\b")
MONTH_NUM = {m[:3].lower(): i % 12 + 1 for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), start=0)}


def strip_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, text
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = {}
            for line in lines[1:i]:
                m = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
                if m:
                    fm[m.group(1)] = m.group(2).strip()
            return fm, "\n".join(lines[i + 1:])
    return None, text


def parse_iso(s):
    try:
        return date.fromisoformat(s)
    except (ValueError, TypeError):
        return None


class Note:
    def __init__(self, path):
        self.path = path
        self.rel = PurePosixPath(path.relative_to(REPO).as_posix())
        self.stem = path.stem
        text = path.read_text(encoding="utf-8")
        self.n_lines = text.count("\n") + 1
        self.fm, self.body = parse_frontmatter(text)
        self.links = [t.strip() for t in WIKILINK.findall(strip_code(self.body))]


def load_notes():
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        cwd=REPO, capture_output=True, text=True, check=True).stdout
    notes = []
    for line in out.splitlines():
        p = REPO / line
        if p.is_file() and not p.is_symlink():
            notes.append(Note(p))
    return sorted(notes, key=lambda n: str(n.rel))


def main():
    today = date.today()
    notes = load_notes()
    stems = Counter(n.stem for n in notes)
    stem_set = set(stems)
    by_dir = defaultdict(list)
    for n in notes:
        by_dir[n.rel.parent].append(n)

    staging_roots = {n.rel.parent for n in notes
                     if n.fm and n.fm.get("status") == "staging"
                     and n.stem == n.rel.parent.name}

    def in_staging(rel):
        return any(rel.parts[:len(r.parts)] == r.parts for r in staging_roots)

    frontmatter, broken, orphans, index_sync = [], [], [], []
    oversize, dash_dates, staging_inv, census, staging_info = [], [], [], [], []
    placeholders = []

    # 1. frontmatter
    for n in notes:
        if n.path.name in NO_FRONTMATTER:
            continue
        if n.fm is None:
            frontmatter.append(f"`{n.rel}` — missing frontmatter")
            continue
        issues = []
        missing = [k for k in REQUIRED_KEYS if k not in n.fm]
        if missing:
            issues.append("missing " + ", ".join(missing))
        s = n.fm.get("status")
        if s and s not in STATUSES:
            issues.append(f"status `{s}` not in enum")
        cd, ud = parse_iso(n.fm.get("created")), parse_iso(n.fm.get("updated"))
        if n.fm.get("created") and not cd:
            issues.append(f"created `{n.fm['created']}` not YYYY-MM-DD")
        if n.fm.get("updated") and not ud:
            issues.append(f"updated `{n.fm['updated']}` not YYYY-MM-DD")
        if cd and ud and ud < cd:
            issues.append("updated before created")
        for label, d in (("created", cd), ("updated", ud)):
            if d and d > today:
                issues.append(f"{label} `{d}` is in the future")
        if issues:
            frontmatter.append(f"`{n.rel}` — " + "; ".join(issues))

    # 2+3. wikilinks: broken (near-match) vs dangling placeholders (tallied)
    inbound = defaultdict(set)
    unresolved = defaultdict(set)
    for n in notes:
        is_log = n.stem == "log" or n.stem.startswith("log-")
        for t in n.links:
            if t in stem_set:
                if t != n.stem and not is_log:  # log links don't rescue orphans
                    inbound[t].add(n.stem)
            elif not is_log:  # append-only timeline may link deleted notes
                unresolved[t].add(str(n.rel))
    for t, srcs in sorted(unresolved.items()):
        close = get_close_matches(t, stem_set, n=1, cutoff=0.75)
        where = ", ".join(f"`{s}`" for s in sorted(srcs))
        if close:
            broken.append(f"`[[{t}]]` in {where} — did you mean `[[{close[0]}]]`?")
        else:
            placeholders.append((len(srcs), t, where))
    placeholders.sort(key=lambda x: (-x[0], x[1]))
    for stem, c in sorted(stems.items()):
        if c > 1:
            broken.append(f"duplicate basename `{stem}` ({c} files) — breaks wikilink addressing")

    # 4. orphans
    for n in notes:
        if n.stem in ORPHAN_EXEMPT or n.stem.startswith("log-") or n.rel.parts[0] == "tools":
            continue
        if n.stem not in inbound:
            line = f"`{n.rel}` — no inbound links"
            (staging_info if in_staging(n.rel) else orphans).append(line)

    # 5. index sync
    for d, dnotes in sorted(by_dir.items()):
        idx_name = "index" if d == PurePosixPath(".") else d.name
        idx = next((n for n in dnotes if n.stem == idx_name), None)
        content = [n for n in dnotes
                   if n.stem != idx_name and n.path.name not in NO_FRONTMATTER]
        target = staging_info if in_staging(d) else index_sync
        if idx is None:
            if len(dnotes) >= 2:
                target.append(f"`{d}/` has {len(dnotes)} notes but no `{idx_name}.md` index")
            continue
        for n in content:
            if f"[[{n.stem}" not in idx.body:
                target.append(f"`{n.rel}` not listed in its index `{idx.rel}`")
        if d != PurePosixPath(".") and d not in staging_roots and not in_staging(d):
            parent = d.parent
            pidx_name = "index" if parent == PurePosixPath(".") else parent.name
            pidx = next((n for n in by_dir.get(parent, []) if n.stem == pidx_name), None)
            if pidx is None:
                index_sync.append(f"`{d}/` has an index but `{parent}/` has no parent index to list it")
            elif f"[[{idx.stem}" not in pidx.body:
                index_sync.append(f"`[[{idx.stem}]]` not listed in parent index `{pidx.rel}`")

    # 6. oversize
    for n in notes:
        if n.stem == "log" or n.stem.startswith("log-"):
            continue
        limit = MAX_CLAUDE_MD_LINES if n.path.name == "CLAUDE.md" else MAX_NOTE_LINES
        if n.n_lines > limit:
            line = f"`{n.rel}` — {n.n_lines} lines (limit ~{limit})"
            (staging_info if in_staging(n.rel) else oversize).append(line)

    # 7. dashboard past dates
    dash = next((n for n in notes if n.stem == "dashboard"), None)
    if dash:
        body = strip_code(dash.body)
        found = {(parse_iso(m.group(1)), m.group(0)) for m in ISO_DATE.finditer(body)}
        for m in MDY.finditer(body):
            mo, day, yr = MONTH_NUM[m.group(1)[:3].lower()], int(m.group(2)), int(m.group(3))
            found.add((date(yr, mo, min(day, 28) if day > 28 else day), m.group(0)))
        for m in DMY.finditer(body):
            day, mo, yr = int(m.group(1)), MONTH_NUM[m.group(2)[:3].lower()], int(m.group(3))
            found.add((date(yr, mo, min(day, 28) if day > 28 else day), m.group(0)))
        for d, s in sorted(found):
            if d and d < today:
                dash_dates.append(f"“{s}” is in the past — deadline missed, or stale context?")

    # 8. staging inventory
    for n in notes:
        if n.fm and n.fm.get("status") == "staging":
            staging_inv.append(f"`{n.rel}` — staging since {n.fm.get('created', '?')}"
                               " (past its exit point?)")

    # 9. folder census
    for d, dnotes in sorted(by_dir.items()):
        # log/ grows by design; profile/ is single-note (about-me) by design
        if d == PurePosixPath(".") or d.parts[0] in ("tools", "log", "profile") or in_staging(d):
            continue
        c = len([n for n in dnotes if n.stem != d.name])
        has_children = any(o != d and o.parts[:len(d.parts)] == d.parts for o in by_dir)
        if c > MAX_FOLDER_NOTES:
            census.append(f"`{d}/` — {c} notes (natural sub-clusters, or fine as flat?)")
        elif c == 1 and not has_children:
            census.append(f"`{d}/` — single-note folder (speculative, or awaiting growth?)")

    print(f"# Lint report — {today} · {len(notes)} notes scanned")

    def section(title, items, note=""):
        print(f"\n## {title}")
        if note:
            print(f"*{note}*")
        for i in items:
            print(f"- {i}")
        if not items:
            print("- ✅ none")

    section("1. Frontmatter", frontmatter)
    section("2. Broken wikilinks / duplicate basenames", broken)
    section("3. Dangling placeholders (ranked — top = note-creation candidates)",
            [f"`[[{t}]]` ×{c} — in {w}" for c, t, w in placeholders])
    section("4. Orphan notes", orphans, "log-timeline links don't count as inbound")
    section("5. Index sync", index_sync)
    section("6. Oversize notes", oversize)
    section("7. Dashboard past dates", dash_dates)
    section("8. Staging inventory", staging_inv)
    section("9. Folder census", census)
    section("Staging subtree (informational only)", staging_info,
            "exempt from index-wiring rules by design; listed for awareness")


if __name__ == "__main__":
    main()

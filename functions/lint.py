#!/usr/bin/env python3
"""Tier-1 lint detector for the knowledge repo.

Read-only: scans the repo's Markdown notes and prints a grouped Markdown
report. Detection only — remediation is judgment work done by the LLM and
the owner (procedure: functions/lint.md). Always exits 0.
"""

import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from difflib import get_close_matches
from pathlib import Path, PurePosixPath

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to a legacy code page

REPO = Path(__file__).resolve().parents[1]
ROOT = PurePosixPath(".")

REQUIRED_KEYS = ("title", "description", "updated")  # CLAUDE.md §3 format gate: these, nothing more
RETIRED_KEYS = {
    "status": "retired in v1: `in-progress/` marks work under construction; a note is current or deleted",
    "tags": "retired in v1: no second axis the folders can't express",
    "created": "retired in v1: git and the log record creation",
    "verified": "retired in v1: a fact that can change carries an inline `(verified: YYYY-MM-DD)`",
    "type": "retired: kind and role follow from location and name",
    "review_after": "retired in v1: a date that must fire is a dashboard line",
}
NO_FRONTMATTER = {"CLAUDE.md", "AGENTS.md"}  # the contract file (+ its pointer file)
NOT_NOTES = {"README.md"}  # the repo's front page on GitHub, outside the note system
INFRA = {"functions", "playbooks", "log", "in-progress"}  # CLAUDE.md §2 infrastructure folders
ORPHAN_EXEMPT = {"index", "dashboard", "log", "CLAUDE", "AGENTS"}
SIZE_FIRST, SIZE_SECOND, SIZE_STEP = 200, 500, 300  # size checks at 200, 500, 800, 1100, ...
MAX_CLAUDE_MD_LINES = 200  # CLAUDE.md's own budget
MAX_ROOT_INDEX_LINES = 100  # index.md budget
MAX_DOMAIN_TOP = 7  # a domain's top level holds at most ~7 items
MAX_DEEP_ITEMS = 15  # below the top level, a folder is checked for a split past ~15 items
MAX_DASH_LINES = 50  # the dashboard is read every session start — a dated index, not notes
MAX_DASH_ITEM_LINES = 1  # the header's rule: one line per item

WIKILINK = re.compile(r"\[\[([^\]|#\n]+)(?:#[^\]|\n]*)?(?:\|[^\]\n]*)?\]\]")
INDEX_LINE = re.compile(r"^\s*-\s+\[\[([^\]|#\n]+)(?:#[^\]|\n]*)?(?:\|[^\]\n]*)?\]\](.*)$")
VERIFIED = re.compile(r"\(verified:\s*([^)]*)\)")
KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
INLINE_CODE = re.compile(r"`([^`\n]+)`")
PATHLIKE = re.compile(r"^[A-Za-z0-9_][\w.-]*(?:/[\w.-]+)*/?$")
PLACEHOLDER = re.compile(r"YYYY|<|>|\*|\.\.\.")
NOT_PLAIN_YAML = re.compile(r":(\s|$)|\s#|^[][{}&*!|>%@`\"',]|^[-?:](\s|$)")  # a value plain YAML rejects or reads differently
SECTION_PTR = re.compile(r"\[\[([^\]|#\n]+)[^\]\n]*\]\]\s*§\s*([^·\[\n]+)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.M)
ISO_DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")
DASH_ITEM = re.compile(r"^- (\d{4}-\d{2}-\d{2}) · ")  # every dashboard item leads with its date
SIZE_MARK = re.compile(r"<!--\s*size checked:\s*(\d+)\s*-->")  # a kept-whole note records its last check
STATUS_BLOCK = re.compile(r"\*\*Status\s*[—–-]+\s*\d{4}-\d{2}-\d{2}")
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
    """Returns (fm dict, body, defects). The repo's schema is flat key: value —
    anything else in the block is a defect, not silently ignored."""
    if not text.startswith("---"):
        return None, text, []
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm, defects = {}, []
            for line in lines[1:i]:
                if not line.strip() or line.lstrip().startswith("#"):
                    continue
                m = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
                if not m:
                    defects.append(f"malformed frontmatter line `{line.strip()}`")
                    continue
                if m.group(1) in fm:
                    defects.append(f"duplicate key `{m.group(1)}`")
                fm[m.group(1)] = m.group(2).strip()
            return fm, "\n".join(lines[i + 1:]), defects
    return None, text, []


def size_checkpoint(n_lines):
    """Highest size checkpoint a note has passed: 0, 200, 500, 800, 1100, ..."""
    if n_lines <= SIZE_FIRST:
        return 0
    if n_lines <= SIZE_SECOND:
        return SIZE_FIRST
    return SIZE_SECOND + SIZE_STEP * ((n_lines - SIZE_SECOND - 1) // SIZE_STEP)


def in_git_history(pathspec):
    """True if any commit ever touched a path matching pathspec (a moved, renamed or deleted file)."""
    out = subprocess.run(["git", "log", "--all", "-1", "--format=%h", "--", pathspec],
                         cwd=REPO, capture_output=True, text=True).stdout
    return bool(out.strip())


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
        self.fm, self.body, self.fm_defects = parse_frontmatter(text)
        self.links = [t.strip() for t in WIKILINK.findall(strip_code(self.body))]


def load_notes():
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        cwd=REPO, capture_output=True, text=True, check=True).stdout
    notes = []
    for line in out.splitlines():
        p = REPO / line
        if p.is_file() and not p.is_symlink() and line not in NOT_NOTES:
            notes.append(Note(p))
    return sorted(notes, key=lambda n: str(n.rel))


def main():
    today = date.today()
    notes = load_notes()
    stems = Counter(n.stem for n in notes)
    stem_set = set(stems)
    by_stem = {}
    for n in notes:
        by_stem.setdefault(n.stem, n)
    by_dir = defaultdict(list)
    dirs = set()
    for n in notes:
        by_dir[n.rel.parent].append(n)
        p = n.rel.parent
        while p != ROOT:
            dirs.add(p)
            p = p.parent

    def children(d):
        return sorted(c for c in dirs if c.parent == d)

    def is_infra(d):
        return d != ROOT and d.parts[0] in INFRA

    def is_log(n):
        return n.stem == "log" or n.stem.startswith("log-")

    def in_progress(rel):
        return rel.parts[0] == "in-progress"

    def index_of(d):
        """A folder's own index note, named after it (top-level folders have none: the root indexes them)."""
        return next((n for n in by_dir.get(d, []) if n.stem == d.name), None)

    def items(d):
        """Direct items of folder d: its notes (minus its own index and the contract files) + sub-folders."""
        own = "index" if d == ROOT else d.name
        ns = [n for n in by_dir.get(d, []) if n.path.name not in NO_FRONTMATTER and n.stem != own]
        return ns, children(d)

    frontmatter, dates_inline, broken, orphans, index_sync, names = [], [], [], [], [], []
    census, oversize, dash_dates, dash_due, prog_flags, prog_inv, temporal = [], [], [], [], [], [], []
    paths = []
    placeholders, desc_missing = [], defaultdict(list)

    # 1. frontmatter: exactly the format gate's keys
    for n in notes:
        if n.path.name in NO_FRONTMATTER:
            continue
        if n.fm is None:
            frontmatter.append(f"`{n.rel}` — missing frontmatter")
            continue
        issues = list(n.fm_defects)
        for k in REQUIRED_KEYS:
            if k not in n.fm:
                if k == "description":
                    desc_missing[str(n.rel.parent)].append(n.stem)
                else:
                    issues.append(f"missing `{k}`")
            elif not n.fm[k]:
                issues.append(f"empty `{k}`")
        for k, v in n.fm.items():
            if k in REQUIRED_KEYS and v and NOT_PLAIN_YAML.search(v):
                issues.append(f"`{k}` isn't plain YAML (a `: ` or ` #` inside, quotes, or a reserved first character): rephrase")
        for k in n.fm:
            if k in REQUIRED_KEYS:
                continue
            issues.append(f"`{k}` is {RETIRED_KEYS[k]}" if k in RETIRED_KEYS
                          else f"`{k}` isn't in the format gate (title, description, updated)")
        raw = n.fm.get("updated")
        ud = parse_iso(raw)
        if raw and not ud:
            issues.append(f"updated `{raw}` not YYYY-MM-DD")
        elif ud and ud > today:
            issues.append(f"updated `{ud}` is in the future")
        if issues:
            frontmatter.append(f"`{n.rel}` — " + "; ".join(issues))

    # 2. inline (verified: YYYY-MM-DD) markers
    for n in notes:
        if n.path.name in NO_FRONTMATTER or is_log(n):
            continue
        for m in VERIFIED.finditer(strip_code(n.body)):
            raw = m.group(1).strip()
            d = parse_iso(raw)
            if not d:
                dates_inline.append(f"`{n.rel}` — `(verified: {raw})` is not YYYY-MM-DD")
            elif d > today:
                dates_inline.append(f"`{n.rel}` — `(verified: {d})` is in the future")

    # 3+4. wikilinks: broken (near-match) vs dangling placeholders (tallied)
    inbound = defaultdict(set)
    unresolved = defaultdict(set)
    for n in notes:
        for t in n.links:
            if t in stem_set:
                if t != n.stem and not is_log(n):  # log links don't rescue orphans
                    inbound[t].add(n.stem)
            elif not is_log(n):  # append-only timeline may link deleted notes
                unresolved[t].add(str(n.rel))
    for t, srcs in sorted(unresolved.items()):
        close = get_close_matches(t, stem_set, n=1, cutoff=0.75)
        where = ", ".join(f"`{s}`" for s in sorted(srcs))
        if close:
            broken.append(f"`[[{t}]]` in {where} — did you mean `[[{close[0]}]]`?")
        elif in_git_history(f":(glob)**/{t}.md"):
            broken.append(f"`[[{t}]]` in {where} — points to a deleted or renamed note: re-point or drop it")
        else:
            placeholders.append((len(srcs), t, where))
    placeholders.sort(key=lambda x: (-x[0], x[1]))
    for stem, c in sorted(stems.items()):
        if c > 1:
            broken.append(f"duplicate basename `{stem}` ({c} files) — breaks wikilink addressing")

    # 5. orphans
    for n in notes:
        if n.stem in ORPHAN_EXEMPT or is_log(n):
            continue
        if n.stem not in inbound:
            orphans.append(f"`{n.rel}` — no inbound links")

    # 6. index sync (CLAUDE.md §4): root two levels, deeper folders one; lines copy descriptions
    def expect_listed(idx, ns, subs):
        listed = set(idx.links)
        for n in ns:
            if n.stem not in listed:
                index_sync.append(f"`{n.rel}` not listed in `{idx.rel}`")
        for s in subs:
            si = index_of(s)
            if si and si.stem not in listed:
                index_sync.append(f"`{s}/` (its `[[{si.stem}]]`) not listed in `{idx.rel}`")

    def check_lines(idx, allowed, scope):
        for line in idx.body.splitlines():
            m = INDEX_LINE.match(line)
            if not m:
                continue
            t = m.group(1).strip()
            if t not in stem_set:
                continue  # reported under broken links
            if t not in allowed:
                index_sync.append(f"`{idx.rel}` lists `[[{t}]]`, which isn't a direct item ({scope})")
                continue
            desc = (by_stem[t].fm or {}).get("description")
            rest = m.group(2)
            if desc and " — " in rest and rest.split(" — ", 1)[1].strip() != desc.strip():
                index_sync.append(f"`{idx.rel}` — the line for `[[{t}]]` doesn't copy its description verbatim")

    root = next((n for n in by_dir.get(ROOT, []) if n.stem == "index"), None)
    if root is None:
        index_sync.append("no root `index.md`")
    else:
        if root.n_lines > MAX_ROOT_INDEX_LINES:
            index_sync.append(f"`index.md` — {root.n_lines} lines (budget ~{MAX_ROOT_INDEX_LINES})")
        ns, _ = items(ROOT)
        expect_listed(root, ns, [])
        allowed = {n.stem for n in ns} | {"log"}
        for t in children(ROOT):
            ti = index_of(t)
            if t.name == "log":
                if "log" not in root.links:
                    index_sync.append("`index.md` doesn't link `[[log]]`")
                continue
            if ti:
                allowed.add(ti.stem)  # reported once below, not again as a stray line
                index_sync.append(f"`{ti.rel}` — a top-level folder has no index (the root indexes it): retire it")
            tns, tsubs = items(t)
            expect_listed(root, tns, tsubs)
            allowed |= {n.stem for n in tns} | {index_of(s).stem for s in tsubs if index_of(s)}
        check_lines(root, allowed, "the root runs two levels: top-level folders, then their direct items")
    for d in sorted(dirs):
        if len(d.parts) < 2 or d.parts[0] == "log":
            continue
        ns, subs = items(d)
        idx = index_of(d)
        if idx is None:
            if len(ns) + len(subs) >= 2:
                index_sync.append(f"`{d}/` has {len(ns) + len(subs)} items but no `{d.name}.md` index")
            continue
        expect_listed(idx, ns, subs)
        allowed = {n.stem for n in ns} | {index_of(s).stem for s in subs if index_of(s)}
        check_lines(idx, allowed, "an index goes one level down")

    # 7. names: notes and folders lowercase kebab-case
    for n in notes:
        if n.path.name not in NO_FRONTMATTER and not KEBAB.match(n.stem):
            names.append(f"`{n.rel}` — note name isn't lowercase kebab-case")
    for d in sorted(dirs):
        if not KEBAB.match(d.name):
            names.append(f"`{d}/` — folder name isn't lowercase kebab-case")

    # 8. folder census: domains only (CLAUDE.md §4 folder rules; infrastructure folders exempt)
    for d in sorted(dirs):
        if is_infra(d):
            continue
        ns, subs = items(d)
        c = len(ns) + len(subs)
        top = len(d.parts) == 1
        cap = MAX_DOMAIN_TOP if top else MAX_DEEP_ITEMS
        if c > cap:
            census.append(f"`{d}/` — {c} items, past ~{cap} "
                          + ("at a domain's top level: group into sub-folders" if top else ": split check"))
        if len(ns) == 1 and not subs:
            census.append(f"`{d}/` — single-note folder: fold it into its parent")

    # 9. oversize: CLAUDE.md past its budget; a note passing an unchecked size checkpoint
    #    (one long topic is kept whole; `<!-- size checked: N -->` under the title records each check)
    for n in notes:
        if is_log(n) or in_progress(n.rel) or n.path.name == "AGENTS.md":
            continue
        if n.path.name == "CLAUDE.md":
            if n.n_lines > MAX_CLAUDE_MD_LINES:
                oversize.append(f"`{n.rel}` — {n.n_lines} lines (budget ~{MAX_CLAUDE_MD_LINES}) — compress before extending")
            continue
        passed = size_checkpoint(n.n_lines)
        recorded = max([int(m) for m in SIZE_MARK.findall(n.body)] + [0])
        if not passed or passed <= recorded:
            continue
        toc = "; swap its `## Contents` TOC for the comment" if re.search(r"^## Contents\s*$", n.body, re.M) else ""
        oversize.append(f"`{n.rel}` — {n.n_lines} lines, past the {passed} check (last: {recorded or 'never'}) — "
                        f"2+ topics → split; one topic → keep, record `<!-- size checked: {passed} -->` under the title{toc}")

    # 10. dashboard: budget · every item date-led · overlong items · due/overdue · stale mid-line dates
    dash = next((n for n in notes if n.stem == "dashboard"), None)
    if dash:
        if dash.n_lines > MAX_DASH_LINES:
            dash_dates.append(f"{dash.n_lines} lines (budget {MAX_DASH_LINES}) — merge, drop or re-date lines")
        items_, cur, section_name = [], None, ""  # [first line, line count, section]; top-level `- ` bullets
        for line in dash.body.splitlines():
            if line.startswith("## "):
                section_name = line[3:].strip()
            if line.startswith("- "):
                cur = [line, 1, section_name]
                items_.append(cur)
            elif cur and line.startswith(" ") and line.strip():
                cur[1] += 1
            else:
                cur = None
        rest = []  # item text with the lead date removed, scanned for stale mid-line dates
        prev = {}  # section → last item date, for the sorted-by-date rule
        for first, count, sec_name in items_:
            m = DASH_ITEM.match(first)
            label = re.sub(r"[*_`]", "", first[m.end():] if m else first[2:]).strip()[:60]
            d = parse_iso(m.group(1)) if m else None
            if m and d is None:
                dash_dates.append(f"“{label}…” — `{m.group(1)}` is not a real date")
            elif d is None:
                dash_dates.append(f"“{label}…” — not led by a `YYYY-MM-DD · ` date (every item is dated)")
            elif d < today:
                dash_due.append(f"{d} · {label}… — overdue")
            elif d == today:
                dash_due.append(f"{d} · {label}… — due today")
            if d and sec_name in prev and d < prev[sec_name]:
                dash_dates.append(f"“{label}…” — {d} sits after {prev[sec_name]} in §{sec_name} (sort by date)")
            if d:
                prev[sec_name] = d  # compare neighbours: one flag at the break, not a cascade
            if count > MAX_DASH_ITEM_LINES:
                dash_dates.append(f"“{label}…” — {count} lines (one line per item)")
            rest.append(first[m.end():] if m else first)
            for t, sec in SECTION_PTR.findall(first):  # a § pointer must still match a heading
                t, sec = t.strip(), sec.strip().rstrip(".,;")
                target = by_stem.get(t)
                if not target or not sec:
                    continue  # a missing note is reported under broken links
                norm = lambda x: re.sub(r"[*_`]", "", x).strip().lower()
                if not any(norm(h).startswith(norm(sec)) or norm(sec) in norm(h)
                           for h in HEADING.findall(re.sub(r"```.*?```", "", target.body, flags=re.S))):
                    dash_dates.append(f"“{label}…” — `[[{t}]] §{sec}`: no such heading in the note (renamed?)")
        body = strip_code("\n".join(rest))
        found = {(parse_iso(m.group(1)), m.group(0)) for m in ISO_DATE.finditer(body)}
        for m in MDY.finditer(body):
            mo, day, yr = MONTH_NUM[m.group(1)[:3].lower()], int(m.group(2)), int(m.group(3))
            found.add((date(yr, mo, min(day, 28)), m.group(0)))
        for m in DMY.finditer(body):
            day, mo, yr = int(m.group(1)), MONTH_NUM[m.group(2)[:3].lower()], int(m.group(3))
            found.add((date(yr, mo, min(day, 28)), m.group(0)))
        for d, s in sorted(found, key=lambda x: (x[0] or date.min, x[1])):
            if d and d < today:
                dash_dates.append(f"“{s}” mid-line is in the past — stale context?")

    # 11. in progress: each item (a note, or a cluster's index) dates its exit on the dashboard
    prog = PurePosixPath("in-progress")
    if prog in dirs:
        ns, subs = items(prog)
        for n in ns + [index_of(s) for s in subs if index_of(s)]:
            prog_inv.append(f"`{n.rel}` — {n.n_lines} lines")
            if not dash or n.stem not in dash.links:
                prog_flags.append(f"`{n.rel}` — no dashboard line links it (every in-progress item dates its exit)")

    # 12. temporal integrity: stacked dated-status blocks
    for n in notes:
        if n.fm is None or in_progress(n.rel):
            continue
        n_status = len(STATUS_BLOCK.findall(strip_code(n.body)))
        if n_status > 1:
            temporal.append(f"`{n.rel}` — {n_status} dated Status blocks — rewrite one current "
                            "state in place (history lives in the log)")

    # 13. path mentions: a backticked repo path that no longer exists (CLAUDE.md §4 Moves and merges)
    top_entries = {p.name for p in REPO.iterdir()}

    def was_in_repo(path):
        out = subprocess.run(["git", "log", "--all", "-1", "--format=%h", "--", path],
                             cwd=REPO, capture_output=True, text=True).stdout
        return bool(out.strip())

    for n in notes:
        if is_log(n) or n.path.name in NO_FRONTMATTER or in_progress(n.rel):
            continue  # in-progress notes record moves on purpose
        seen = set()
        for m in INLINE_CODE.finditer(re.sub(r"```.*?```", "", n.body, flags=re.S)):
            s = m.group(1).strip()
            if "/" not in s or s in seen or PLACEHOLDER.search(s) or not PATHLIKE.match(s):
                continue
            last = s.rstrip("/").split("/")[-1]
            if not (s.endswith("/") or "." in last):
                continue  # a path names a folder (trailing `/`) or a file (an extension)
            seen.add(s)
            if (REPO / s).exists():
                continue
            if s.split("/")[0] not in top_entries and not was_in_repo(s):
                continue  # never in this repo: another repo's path
            paths.append(f"`{n.rel}` mentions `{s}`, which no longer exists (moved?)")

    print(f"# Lint report — {today} · {len(notes)} notes scanned")

    def section(title, items, note=""):
        print(f"\n## {title}")
        if note:
            print(f"*{note}*")
        for i in items:
            print(f"- {i}")
        if not items:
            print("- ✅ none")

    section("1. Frontmatter (title, description, updated — nothing more)", frontmatter)
    n_missing = sum(len(v) for v in desc_missing.values())
    section(f"1b. Missing `description` ({n_missing} notes, by folder)",
            [f"`{d}/` — {len(s)}: {', '.join(s)}" for d, s in sorted(desc_missing.items())])
    section("2. Inline `(verified: …)` dates", dates_inline)
    section("3. Broken wikilinks / duplicate basenames", broken)
    section("4. Dangling placeholders (ranked — top = note-creation candidates)",
            [f"`[[{t}]]` ×{c} — in {w}" for c, t, w in placeholders])
    section("5. Orphan notes", orphans, "log-timeline links don't count as inbound")
    section("6. Index sync (root two levels · deeper folders one · lines copy descriptions)", index_sync)
    section("7. Names (lowercase kebab-case)", names)
    section("8. Folder census (domains only: top level ~7 · deeper ~15 · single-note folders)", census)
    section("9. Oversize notes (unchecked size checkpoint 200/500/800/… · CLAUDE.md over budget)", oversize)
    section("10. Dashboard hygiene (budget · undated or overlong items · stale dates)", dash_dates)
    section("10b. Dashboard lines due (raise with the owner)", dash_due)
    section("11. In progress without a dashboard line", prog_flags)
    section("11b. In progress (informational)", prog_inv, "exempt from the content gate, right-sizing and the folder rules")
    section("12. Temporal integrity (stacked status blocks)", temporal)
    section("13. Path mentions (backticked repo paths that no longer exist)", paths)


if __name__ == "__main__":
    main()

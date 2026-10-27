#!/usr/bin/env python3
"""Build the distributable plugin in plugin/ from the .claude/ source tree.

The .claude/ tree is written for use in place (open Claude Code in this repo),
so it refers to its own files as .claude/kb/..., .claude/skills/..., etc. An
installed plugin lives in the plugin cache instead, so this build copies the
tree and rewrites those references to ${CLAUDE_PLUGIN_ROOT}/..., which Claude
Code substitutes in skill, command, and agent content. SDD workspace paths
(.claude/sdd/features, reports, board, archive) and .claude/storage stay
project-relative on purpose: they are written into the user's project.

Usage:
    python scripts/build-plugin.py           # rebuild plugin/
    python scripts/build-plugin.py --check   # exit 1 if plugin/ is stale
"""

from __future__ import annotations

import argparse
import filecmp
import re
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / ".claude"
OUT = REPO / "plugin"

EXCLUDE = [
    re.compile(p)
    for p in (
        r"^settings(\.local)?\.json$",
        r"^storage(/|$)",
        r"^sdd/(features|reports|board|archive|drafts)(/|$)",
        r"^agents/README\.md$",
        r"^agents/_template\.md$",
        r"^commands/(.+/)?README\.md$",
        r"(^|/)__pycache__(/|$)",
        r"\.pyc$",
    )
]

REWRITE_SUFFIXES = {".md", ".yaml", ".yml"}
PLUGIN_PATH = re.compile(
    r"(?<![\w~/.$])\.claude/"
    r"(?=agents\b|commands\b|skills\b|kb\b|\.claude-plugin\b"
    r"|sdd/(?:templates|architecture)\b|sdd/README\.md|sdd/_index\.md)"
)
FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)


def excluded(rel: str) -> bool:
    return any(p.search(rel) for p in EXCLUDE)


def rewrite(text: str, suffix: str) -> str:
    if suffix == ".md":
        match = FRONTMATTER.match(text)
        if match:
            head, body = text[: match.end()], text[match.end():]
            return head + PLUGIN_PATH.sub("${CLAUDE_PLUGIN_ROOT}/", body)
    return PLUGIN_PATH.sub("${CLAUDE_PLUGIN_ROOT}/", text)


def build(out: Path) -> tuple[int, int]:
    if out.exists():
        shutil.rmtree(out)
    copied = rewritten = 0
    for src in sorted(SRC.rglob("*")):
        rel = src.relative_to(SRC).as_posix()
        if src.is_dir() or excluded(rel):
            continue
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in REWRITE_SUFFIXES:
            text = src.read_text(encoding="utf-8")
            new = rewrite(text, src.suffix)
            dst.write_bytes(new.encode("utf-8"))
            rewritten += new != text
        else:
            shutil.copyfile(src, dst)
        copied += 1
    return copied, rewritten


def same_tree(a: Path, b: Path) -> bool:
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.funny_files:
        return False
    _, mismatch, errors = filecmp.cmpfiles(a, b, cmp.common_files, shallow=False)
    if mismatch or errors:
        return False
    return all(same_tree(a / d, b / d) for d in cmp.common_dirs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="fail if plugin/ is out of date")
    args = parser.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            fresh = Path(tmp) / "plugin"
            build(fresh)
            if OUT.exists() and same_tree(fresh, OUT):
                print("plugin/ is up to date")
                return 0
        print("plugin/ is stale: run python scripts/build-plugin.py and commit the result")
        return 1

    copied, rewritten = build(OUT)
    print(f"built {OUT.relative_to(REPO)}/: {copied} files, {rewritten} with rewritten paths")
    return 0


if __name__ == "__main__":
    sys.exit(main())

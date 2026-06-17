#!/usr/bin/env python3
"""Check local Markdown links and images without external dependencies."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_RESOURCE_RE = re.compile(
    r"""<(?:img|source)\b[^>]*\b(?:src|srcset)=["']([^"']+)["']""",
    re.IGNORECASE,
)
SKIP_PREFIXES = (
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "#",
    "app://",
)


def iter_markdown_files(root: Path) -> list[Path]:
    ignored = {".git", ".venv", "node_modules", "__pycache__"}
    files: list[Path] = []
    for path in root.rglob("*.md"):
        if any(part in ignored for part in path.parts):
            continue
        files.append(path)
    return files


def clean_target(raw: str) -> str:
    target = raw.strip().split()[0]
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    return unquote(target.split("#", 1)[0])


def check_file(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    in_fence = False
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in LINK_RE.finditer(line):
            target = clean_target(match.group(1))
            if not target or target.startswith(SKIP_PREFIXES):
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                rel = path.relative_to(root)
                errors.append(f"{rel}:{lineno}: missing local link target: {target}")
        for match in HTML_RESOURCE_RE.finditer(line):
            target = clean_target(match.group(1))
            if not target or target.startswith(SKIP_PREFIXES):
                continue
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                rel = path.relative_to(root)
                errors.append(f"{rel}:{lineno}: missing local HTML resource target: {target}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    root = args.root.resolve()
    errors: list[str] = []
    for md in iter_markdown_files(root):
        errors.extend(check_file(md, root))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Markdown local links are valid!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

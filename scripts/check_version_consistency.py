#!/usr/bin/env python3
"""Check that repository version mentions match the installable skill VERSION."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "fdu-final-paper-skill"
VERSION_FILE = SKILL_DIR / "VERSION"
VERSION_RE = re.compile(r"^v\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$")


def require_contains(path: Path, needle: str, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if needle not in text:
        errors.append(f"{path.relative_to(ROOT)} must contain: {needle}")


def main() -> int:
    errors: list[str] = []

    if not VERSION_FILE.is_file():
        errors.append(f"Missing version source: {VERSION_FILE.relative_to(ROOT)}")
        version = ""
    else:
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
        if not VERSION_RE.match(version):
            errors.append(
                f"{VERSION_FILE.relative_to(ROOT)} must contain a semantic version like v1.2.3"
            )

    if version:
        require_contains(ROOT / "README.md", f"skill-{version}-", errors)
        require_contains(ROOT / "README.md", f"Current skill version: `{version}`", errors)
        require_contains(ROOT / "README.md", "`skills/fdu-final-paper-skill/VERSION`", errors)
        require_contains(ROOT / "README.zh-CN.md", f"skill-{version}-", errors)
        require_contains(ROOT / "README.zh-CN.md", f"当前 skill 版本：`{version}`", errors)
        require_contains(ROOT / "README.zh-CN.md", "`skills/fdu-final-paper-skill/VERSION`", errors)
        require_contains(ROOT / "CHANGELOG.md", f"## {version} -", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"Version references match {version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

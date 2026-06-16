#!/usr/bin/env python3
"""Repository smoke checks that should stay fast and deterministic."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "fdu-final-paper-skill"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing required path: {path.relative_to(ROOT)}")


def main() -> int:
    require(ROOT / "LICENSE")
    require(ROOT / "NOTICE")
    require(ROOT / "CONTRIBUTING.md")
    require(ROOT / ".gitignore")
    require(SKILL_DIR / "SKILL.md")
    require(SKILL_DIR / "references" / "fudan-2026-format-checklist.md")
    require(SKILL_DIR / "scripts" / "check_fudan_spec_update.py")

    if (ROOT / "embedded" / "claude-office-docx-skill").exists():
        raise SystemExit("Unlicensed DOCX vendoring must not be restored.")

    examples = sorted((ROOT / "examples").glob("*.md"))
    if len(examples) < 4:
        raise SystemExit("Expected at least 4 example markdown files.")

    prompts_path = ROOT / "evals" / "prompts.json"
    prompts = json.loads(prompts_path.read_text(encoding="utf-8"))
    if len(prompts) != 10:
        raise SystemExit(f"Expected exactly 10 eval prompts, found {len(prompts)}.")
    required_prompt_keys = {"id", "task_type", "prompt", "expected_checks"}
    for item in prompts:
        missing = required_prompt_keys - set(item)
        if missing:
            raise SystemExit(f"Eval prompt {item.get('id', '<missing id>')} missing {sorted(missing)}")

    run([sys.executable, "scripts/quick_validate.py", str(SKILL_DIR)])
    run([sys.executable, "scripts/check_markdown_links.py", "--root", str(ROOT)])
    run(
        [
            sys.executable,
            str(SKILL_DIR / "scripts" / "check_fudan_spec_update.py"),
            "--reference",
            str(SKILL_DIR / "references" / "fudan-2026-format-checklist.md"),
            "--offline",
        ]
    )

    print("Smoke tests passed!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Minimal skill folder validator for CI and local development."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$")


def parse_frontmatter(skill_md: Path) -> tuple[dict[str, str], list[str]]:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    errors: list[str] = []

    if not lines or lines[0].strip() != "---":
        return {}, ["SKILL.md must start with YAML frontmatter delimiter '---'"]

    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, ["SKILL.md frontmatter must end with delimiter '---'"]

    data: dict[str, str] = {}
    current_key: str | None = None
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if raw.startswith((" ", "\t")):
            if current_key and data.get(current_key) in {">", "|"}:
                continue
            if current_key:
                data[current_key] = (data[current_key] + " " + raw.strip()).strip()
            continue
        if ":" not in raw:
            errors.append(f"Invalid frontmatter line: {raw}")
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        data[key] = value
        current_key = key

    return data, errors


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = path.resolve()
    skill_md = skill_dir / "SKILL.md"

    if not skill_dir.is_dir():
        return [f"Skill path is not a directory: {skill_dir}"]
    if not skill_md.is_file():
        return [f"Missing SKILL.md: {skill_md}"]

    data, parse_errors = parse_frontmatter(skill_md)
    errors.extend(parse_errors)

    allowed = {"name", "description"}
    extra = sorted(set(data) - allowed)
    missing = sorted(allowed - set(data))
    if extra:
        errors.append(f"Unsupported frontmatter keys: {', '.join(extra)}")
    if missing:
        errors.append(f"Missing frontmatter keys: {', '.join(missing)}")

    name = data.get("name", "")
    if name and not NAME_RE.match(name):
        errors.append(f"Invalid skill name: {name}")
    if name and skill_dir.name != name:
        errors.append(f"Skill folder name '{skill_dir.name}' must match frontmatter name '{name}'")

    description = data.get("description", "")
    if not description:
        errors.append("Frontmatter description must not be empty")

    agents_yaml = skill_dir / "agents" / "openai.yaml"
    if not agents_yaml.is_file():
        errors.append("Missing recommended agents/openai.yaml")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_path", type=Path)
    args = parser.parse_args()

    errors = validate_skill(args.skill_path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Skill is valid!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

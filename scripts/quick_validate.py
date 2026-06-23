#!/usr/bin/env python3
"""Minimal skill folder validator for CI and local development."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover - exercised only in minimal Python envs
    yaml = None


NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$")
DESCRIPTION_MIN_CHARS = 120
DESCRIPTION_KEYWORD_GROUPS = [
    ("Fudan/FDU scope", ("fudan", "复旦")),
    ("thesis scope", ("thesis", "dissertation", "学位论文", "毕业论文")),
    ("writing or audit workflow", ("plan", "draft", "revise", "audit", "目录", "摘要", "合规")),
    ("file workflow", ("latex", "bibtex", "fduthesis", "docx")),
]
AGENTS_KEYWORD_GROUPS = [
    ("Fudan/FDU scope", ("fudan", "复旦")),
    ("thesis scope", ("thesis", "论文", "学位论文")),
    ("LaTeX workflow", ("latex", "fduthesis", "编译")),
    ("compliance workflow", ("compliance", "audit", "合规", "检查")),
]
VERSION_RE = re.compile(r"^v\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$")


def strip_quotes(value: str) -> str:
    return value.strip().strip('"').strip("'")


def parse_simple_yaml(text: str, source: str) -> tuple[dict[str, Any], list[str]]:
    """Fallback parser for this repo's small YAML subset."""
    data: dict[str, Any] = {}
    errors: list[str] = []
    lines = text.splitlines()
    index = 0

    while index < len(lines):
        raw = lines[index]
        if not raw.strip() or raw.lstrip().startswith("#"):
            index += 1
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent != 0:
            errors.append(f"{source}: unexpected indentation: {raw}")
            index += 1
            continue
        if ":" not in raw:
            errors.append(f"{source}: invalid YAML line: {raw}")
            index += 1
            continue

        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value in {">", "|"}:
            block_lines: list[str] = []
            block_indent: int | None = None
            index += 1
            while index < len(lines):
                block_raw = lines[index]
                if not block_raw.strip():
                    block_lines.append("")
                    index += 1
                    continue
                next_indent = len(block_raw) - len(block_raw.lstrip(" "))
                if next_indent == 0:
                    break
                if block_indent is None:
                    block_indent = next_indent
                block_lines.append(block_raw[block_indent:])
                index += 1
            data[key] = (
                "\n".join(block_lines).strip()
                if value == "|"
                else " ".join(line.strip() for line in block_lines if line.strip())
            )
            continue

        if value == "":
            nested: dict[str, str] = {}
            index += 1
            while index < len(lines):
                nested_raw = lines[index]
                if not nested_raw.strip():
                    index += 1
                    continue
                nested_indent = len(nested_raw) - len(nested_raw.lstrip(" "))
                if nested_indent == 0:
                    break
                stripped = nested_raw.strip()
                if ":" not in stripped:
                    errors.append(f"{source}: invalid nested YAML line: {nested_raw}")
                    index += 1
                    continue
                nested_key, nested_value = stripped.split(":", 1)
                nested[nested_key.strip()] = strip_quotes(nested_value.strip())
                index += 1
            data[key] = nested
            continue

        data[key] = strip_quotes(value)
        index += 1

    return data, errors


def parse_yaml_text(text: str, source: str) -> tuple[dict[str, Any], list[str]]:
    if yaml is not None:
        try:
            loaded = yaml.safe_load(text) or {}
        except Exception as exc:  # pragma: no cover - backend-specific details
            return {}, [f"{source}: YAML parse error: {exc}"]
        if not isinstance(loaded, dict):
            return {}, [f"{source}: YAML content must be a mapping"]
        return dict(loaded), []

    return parse_simple_yaml(text, source)


def parse_frontmatter(skill_md: Path) -> tuple[dict[str, Any], list[str]]:
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0].strip() != "---":
        return {}, ["SKILL.md must start with YAML frontmatter delimiter '---'"]

    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        return {}, ["SKILL.md frontmatter must end with delimiter '---'"]

    return parse_yaml_text("\n".join(lines[1:end]), "SKILL.md frontmatter")


def as_string(value: Any) -> str:
    return value if isinstance(value, str) else ""


def missing_keyword_groups(text: str, groups: list[tuple[str, tuple[str, ...]]]) -> list[str]:
    lowered = text.lower()
    missing: list[str] = []
    for label, keywords in groups:
        if not any(keyword.lower() in lowered for keyword in keywords):
            missing.append(label)
    return missing


def validate_description(description: str) -> list[str]:
    errors: list[str] = []
    if not description:
        return ["Frontmatter description must not be empty"]
    if description.strip() in {">", "|"}:
        errors.append("Frontmatter description was not parsed from its YAML block scalar")
    if len(description) < DESCRIPTION_MIN_CHARS:
        errors.append(
            f"Frontmatter description is too short ({len(description)} chars); "
            f"expected at least {DESCRIPTION_MIN_CHARS}"
        )
    missing = missing_keyword_groups(description, DESCRIPTION_KEYWORD_GROUPS)
    if missing:
        errors.append("Frontmatter description is missing trigger coverage for: " + ", ".join(missing))
    return errors


def validate_agents_yaml(agents_yaml: Path, skill_name: str) -> list[str]:
    if not agents_yaml.is_file():
        return ["Missing recommended agents/openai.yaml"]

    data, parse_errors = parse_yaml_text(agents_yaml.read_text(encoding="utf-8"), "agents/openai.yaml")
    if parse_errors:
        return parse_errors

    errors: list[str] = []
    interface = data.get("interface")
    if not isinstance(interface, dict):
        return ["agents/openai.yaml must contain an interface mapping"]

    required = ("display_name", "short_description", "default_prompt")
    values = {field: as_string(interface.get(field)).strip() for field in required}
    for field, value in values.items():
        if not value:
            errors.append(f"agents/openai.yaml interface.{field} must not be empty")

    default_prompt = values["default_prompt"]
    if skill_name and f"${skill_name}" not in default_prompt:
        errors.append(f"agents/openai.yaml default_prompt must reference ${skill_name}")

    interface_text = " ".join(values.values())
    missing = missing_keyword_groups(interface_text, AGENTS_KEYWORD_GROUPS)
    if missing:
        errors.append("agents/openai.yaml appears stale; missing interface coverage for: " + ", ".join(missing))

    return errors


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = path.resolve()
    skill_md = skill_dir / "SKILL.md"

    if not skill_dir.is_dir():
        return [f"Skill path is not a directory: {skill_dir}"]
    if not skill_md.is_file():
        return [f"Missing SKILL.md: {skill_md}"]

    version_file = skill_dir / "VERSION"
    if not version_file.is_file():
        errors.append("Missing VERSION file")
    else:
        version = version_file.read_text(encoding="utf-8").strip()
        if not VERSION_RE.match(version):
            errors.append("VERSION must contain a semantic version like v1.2.3")

    data, parse_errors = parse_frontmatter(skill_md)
    errors.extend(parse_errors)

    allowed = {"name", "description"}
    extra = sorted(set(data) - allowed)
    missing = sorted(allowed - set(data))
    if extra:
        errors.append(f"Unsupported frontmatter keys: {', '.join(extra)}")
    if missing:
        errors.append(f"Missing frontmatter keys: {', '.join(missing)}")

    name = as_string(data.get("name")).strip()
    if name and not NAME_RE.match(name):
        errors.append(f"Invalid skill name: {name}")
    if name and skill_dir.name != name:
        errors.append(f"Skill folder name '{skill_dir.name}' must match frontmatter name '{name}'")

    description = as_string(data.get("description")).strip()
    errors.extend(validate_description(description))

    agents_yaml = skill_dir / "agents" / "openai.yaml"
    errors.extend(validate_agents_yaml(agents_yaml, name))

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

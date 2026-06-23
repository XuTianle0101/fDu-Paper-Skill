#!/usr/bin/env python3
"""Validate eval prompts and rubric coverage in expected/model outputs."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROMPTS = ROOT / "evals" / "prompts.json"
DEFAULT_OUTPUTS = ROOT / "evals" / "expected"
REQUIRED_PROMPT_KEYS = {"id", "task_type", "prompt", "expected_checks"}
OPTIONAL_LIST_KEYS = {"behavior_checks", "forbidden_patterns"}
GLOBAL_RUBRICS = {
    "source declaration": (
        "source declaration",
        "sources used",
        "来源声明",
        "来源",
    ),
    "missing information": (
        "missing inputs",
        "missing information",
        "missing evidence",
        "缺失",
        "待补充",
        "unknowns",
    ),
    "claim-evidence risks": (
        "claim-evidence",
        "claim evidence",
        "evidence status",
        "unsupported",
        "证据",
    ),
    "compliance unknowns": (
        "compliance unknown",
        "department confirmation",
        "graduate school",
        "fudan 2026",
        "合规未知",
        "院系确认",
    ),
}
BEHAVIOR_RUBRICS = {
    "declare sources": (
        "source declaration",
        "sources used",
        "来源声明",
        "使用来源",
    ),
    "list unknowns": (
        "missing inputs",
        "missing information",
        "unknowns",
        "缺失",
        "未知",
        "待确认",
    ),
    "bound claims to evidence": (
        "claim-evidence",
        "evidence status",
        "unsupported",
        "证据",
        "不支持",
        "不可断言",
    ),
    "avoid unverified official conclusions": (
        "official",
        "final authority",
        "department confirmation",
        "研究生院",
        "院系确认",
        "正式说明",
    ),
    "avoid fabricated data": (
        "do not invent",
        "not supplied",
        "missing evidence",
        "未提供",
        "不得编造",
        "不可编造",
    ),
}
GLOBAL_FORBIDDEN_PATTERNS = [
    r"officially approved",
    r"officially compliant",
    r"approved by fudan",
    r"fully compliant with fudan",
    r"no department confirmation (?:is )?needed",
    r"无需.*(?:院系|研究生院).*确认",
    r"已通过.*(?:审核|审查|合规)",
    r"完全符合.*复旦",
    r"复旦(?:大学)?(?:已经|已).*批准",
]
MIN_FIXTURE_CHARS = 800


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold())


def contains_any(text: str, terms: tuple[str, ...]) -> bool:
    normalized = normalize(text)
    return any(normalize(term) in normalized for term in terms)


def matches_pattern(text: str, pattern: str) -> bool:
    return re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) is not None


def load_prompts(path: Path) -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    try:
        prompts = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [], [f"{path}: invalid JSON: {exc}"]
    if not isinstance(prompts, list):
        return [], [f"{path}: expected a list of prompt objects"]

    seen: set[str] = set()
    for index, item in enumerate(prompts, start=1):
        if not isinstance(item, dict):
            errors.append(f"{path}: item {index} must be an object")
            continue
        missing = REQUIRED_PROMPT_KEYS - set(item)
        if missing:
            errors.append(f"{path}: item {index} missing keys: {', '.join(sorted(missing))}")
        prompt_id = item.get("id")
        if not isinstance(prompt_id, str) or not prompt_id:
            errors.append(f"{path}: item {index} has invalid id")
        elif prompt_id in seen:
            errors.append(f"{path}: duplicate id: {prompt_id}")
        else:
            seen.add(prompt_id)
        expected_checks = item.get("expected_checks")
        if not isinstance(expected_checks, list) or not all(isinstance(check, str) for check in expected_checks):
            errors.append(f"{path}: item {index} expected_checks must be a list of strings")
        for key in OPTIONAL_LIST_KEYS:
            value = item.get(key, [])
            if not isinstance(value, list) or not all(isinstance(entry, str) for entry in value):
                errors.append(f"{path}: item {index} {key} must be a list of strings")
        behavior_checks = item.get("behavior_checks", [])
        for check in behavior_checks:
            if check not in BEHAVIOR_RUBRICS:
                errors.append(f"{path}: item {index} unknown behavior check: {check}")
        fixture_path = item.get("fixture_path")
        if fixture_path is not None:
            if not isinstance(fixture_path, str) or not fixture_path:
                errors.append(f"{path}: item {index} fixture_path must be a non-empty string")
            else:
                resolved_fixture = (path.parent / fixture_path).resolve()
                evals_root = path.parent.resolve()
                if not resolved_fixture.is_file():
                    errors.append(f"{path}: item {index} fixture_path does not exist: {fixture_path}")
                elif evals_root not in resolved_fixture.parents and resolved_fixture != evals_root:
                    errors.append(f"{path}: item {index} fixture_path must stay inside {evals_root}")
                else:
                    fixture_text = resolved_fixture.read_text(encoding="utf-8")
                    if len(fixture_text) < MIN_FIXTURE_CHARS:
                        errors.append(
                            f"{path}: item {index} fixture_path is too short "
                            f"({len(fixture_text)} chars); expected at least {MIN_FIXTURE_CHARS}"
                        )

    return prompts, errors


def validate_output(prompt: dict, outputs_dir: Path) -> list[str]:
    prompt_id = prompt["id"]
    output_path = outputs_dir / f"{prompt_id}.md"
    if not output_path.is_file():
        return [f"Missing eval output: {output_path.relative_to(ROOT)}"]

    text = output_path.read_text(encoding="utf-8")
    errors: list[str] = []
    for label, terms in GLOBAL_RUBRICS.items():
        if not contains_any(text, terms):
            errors.append(f"{output_path.relative_to(ROOT)}: missing global rubric coverage: {label}")

    for check in prompt.get("behavior_checks", []):
        terms = BEHAVIOR_RUBRICS[check]
        if not contains_any(text, terms):
            errors.append(f"{output_path.relative_to(ROOT)}: missing behavior check: {check}")

    for check in prompt["expected_checks"]:
        if normalize(check) not in normalize(text):
            errors.append(f"{output_path.relative_to(ROOT)}: missing expected check phrase: {check}")

    forbidden_patterns = GLOBAL_FORBIDDEN_PATTERNS + prompt.get("forbidden_patterns", [])
    for pattern in forbidden_patterns:
        if matches_pattern(text, pattern):
            errors.append(f"{output_path.relative_to(ROOT)}: forbidden pattern matched: {pattern}")

    return errors


def validate_outputs(prompts: list[dict], outputs_dir: Path) -> list[str]:
    errors: list[str] = []
    if not outputs_dir.is_dir():
        return [f"Outputs directory does not exist: {outputs_dir}"]

    prompt_ids = {item["id"] for item in prompts if isinstance(item.get("id"), str)}
    output_ids = {path.stem for path in outputs_dir.glob("*.md")}
    extras = sorted(output_ids - prompt_ids)
    if extras:
        errors.append("Unexpected eval output file(s): " + ", ".join(f"{item}.md" for item in extras))

    for prompt in prompts:
        if isinstance(prompt.get("id"), str) and isinstance(prompt.get("expected_checks"), list):
            errors.extend(validate_output(prompt, outputs_dir))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", type=Path, default=DEFAULT_PROMPTS)
    parser.add_argument("--outputs-dir", type=Path, default=DEFAULT_OUTPUTS)
    args = parser.parse_args()

    prompts, errors = load_prompts(args.prompts)
    if not errors:
        errors.extend(validate_outputs(prompts, args.outputs_dir))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Eval outputs satisfy rubric coverage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

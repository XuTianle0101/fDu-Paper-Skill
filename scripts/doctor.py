#!/usr/bin/env python3
"""Environment and installation doctor for fdu-final-paper-skill."""

from __future__ import annotations

import argparse
import importlib.util
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL_DIR = ROOT / "skills" / "fdu-final-paper-skill"
SKILL_NAME = "fdu-final-paper-skill"
MIN_PYTHON = (3, 8)
PDF_BACKENDS = [
    ("pypdf", "pypdf"),
    ("PyPDF2", "PyPDF2"),
    ("pdfplumber", "pdfplumber"),
    ("PyMuPDF", "fitz"),
]


class Doctor:
    def __init__(self) -> None:
        self.failures: list[str] = []
        self.warnings: list[str] = []

    def ok(self, message: str) -> None:
        print(f"[OK] {message}")

    def warn(self, message: str) -> None:
        self.warnings.append(message)
        print(f"[WARN] {message}")

    def fail(self, message: str) -> None:
        self.failures.append(message)
        print(f"[FAIL] {message}")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_python(doctor: Doctor) -> None:
    version = sys.version_info
    version_text = f"{version.major}.{version.minor}.{version.micro}"
    if (version.major, version.minor) >= MIN_PYTHON:
        doctor.ok(f"Python {version_text} at {sys.executable}")
    else:
        doctor.fail(f"Python {version_text} is too old; expected Python 3.8 or newer")
    doctor.ok(f"Platform: {platform.platform()}")


def check_skill_tree(doctor: Doctor, skill_dir: Path) -> None:
    if not skill_dir.is_dir():
        doctor.fail(f"Skill directory not found: {skill_dir}")
        return
    doctor.ok(f"Repository skill directory found: {skill_dir}")

    required = [
        "SKILL.md",
        "VERSION",
        "agents/openai.yaml",
        "scripts/read_reference_file.py",
        "scripts/compile_latex_project.py",
        "scripts/check_fudan_spec_update.py",
        "references/fudan-2026-format-checklist.md",
        "references/compliance-source-policy.md",
    ]
    for relative in required:
        path = skill_dir / relative
        if path.is_file():
            doctor.ok(f"Required file present: {relative}")
        else:
            doctor.fail(f"Required file missing: {path}")


def check_agents_yaml(doctor: Doctor, skill_dir: Path) -> None:
    agents_yaml = skill_dir / "agents" / "openai.yaml"
    if not agents_yaml.is_file():
        doctor.fail(f"agents/openai.yaml not found: {agents_yaml}")
        return

    text = read_text(agents_yaml)
    required_fragments = [
        "interface:",
        "display_name:",
        "short_description:",
        "default_prompt:",
        f"${SKILL_NAME}",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in text]
    if missing:
        doctor.fail("agents/openai.yaml missing: " + ", ".join(missing))
    else:
        doctor.ok("agents/openai.yaml has required interface fields")


def check_optional_pdf_backends(doctor: Doctor) -> None:
    available: list[str] = []
    missing: list[str] = []
    for label, module_name in PDF_BACKENDS:
        if importlib.util.find_spec(module_name) is None:
            missing.append(label)
        else:
            available.append(label)

    if available:
        doctor.ok("Python PDF backend(s) available: " + ", ".join(available))
    else:
        doctor.warn("No Python PDF backend found; install pypdf, PyPDF2, pdfplumber, or PyMuPDF for PDF text extraction")

    if missing:
        doctor.warn("Missing optional Python PDF backend(s): " + ", ".join(missing))


def check_pdftotext(doctor: Doctor) -> None:
    executable = shutil.which("pdftotext")
    if not executable:
        doctor.warn("Poppler pdftotext not found on PATH; scanned/image PDFs may need another PDF/OCR workflow")
        return

    doctor.ok(f"Poppler pdftotext found: {executable}")
    completed = subprocess.run(
        [executable, "-v"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    version_output = (completed.stdout or completed.stderr).strip().splitlines()
    if version_output:
        doctor.ok("pdftotext version: " + version_output[0])


def installed_skill_candidates() -> list[Path]:
    candidates: list[Path] = []
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        candidates.append(Path(codex_home) / "skills" / SKILL_NAME)
    candidates.append(Path.home() / ".codex" / "skills" / SKILL_NAME)
    unique: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.expanduser()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def check_installed_skill(doctor: Doctor, require_installed: bool) -> None:
    candidates = installed_skill_candidates()
    installed = [path for path in candidates if (path / "SKILL.md").is_file()]
    if installed:
        for path in installed:
            doctor.ok(f"Installed skill found: {path}")
        return

    message = (
        "Installed skill not found. Expected one of: "
        + "; ".join(str(path) for path in candidates)
    )
    if require_installed:
        doctor.fail(message)
    else:
        doctor.warn(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-dir", type=Path, default=DEFAULT_SKILL_DIR)
    parser.add_argument(
        "--require-installed",
        action="store_true",
        help="Fail if the skill is not installed in CODEX_HOME or ~/.codex/skills.",
    )
    args = parser.parse_args()

    doctor = Doctor()
    skill_dir = args.skill_dir.resolve()

    print("fdu-final-paper-skill doctor")
    print(f"Repository root: {ROOT}")
    check_python(doctor)
    check_skill_tree(doctor, skill_dir)
    check_agents_yaml(doctor, skill_dir)
    check_optional_pdf_backends(doctor)
    check_pdftotext(doctor)
    check_installed_skill(doctor, args.require_installed)

    print("")
    print(f"Summary: {len(doctor.failures)} failure(s), {len(doctor.warnings)} warning(s)")
    if doctor.failures:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

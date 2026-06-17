#!/usr/bin/env python3
"""Compile LaTeX thesis projects with FDU-friendly diagnostics."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


USEPACKAGE_RE = re.compile(r"\\usepackage(?:\s*\[[^\]]*\])?\s*\{([^{}]+)\}")
DOCUMENTCLASS_RE = re.compile(r"\\documentclass(?:\s*\[[^\]]*\])?\s*\{([^{}]+)\}")
INCLUDE_RE = re.compile(r"\\include\s*\{([^{}]+)\}")
OUTPUT_RE = re.compile(
    r"Output written on\s+[`'\"]?(.+?\.pdf)[`'\"]?\s+\((\d+)\s+pages?",
    re.IGNORECASE | re.DOTALL,
)
FATAL_LOG_PATTERNS = [
    re.compile(r"^! .+", re.MULTILINE),
    re.compile(r"Emergency stop", re.IGNORECASE),
    re.compile(r"Fatal error", re.IGNORECASE),
    re.compile(r"Undefined control sequence", re.IGNORECASE),
    re.compile(r"I can't write on file", re.IGNORECASE),
]
UNICODE_MATH_CONFLICTS = {
    "amssymb",
    "amsfonts",
    "mathptmx",
    "mathspec",
    "newtxmath",
    "pxfonts",
    "txfonts",
}


@dataclass(frozen=True)
class Diagnostic:
    level: str
    message: str
    action: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def strip_latex_comment(line: str) -> str:
    escaped = False
    for index, char in enumerate(line):
        if char == "\\":
            escaped = not escaped
            continue
        if char == "%" and not escaped:
            return line[:index]
        escaped = False
    return line


def uncommented_text(text: str) -> str:
    return "\n".join(strip_latex_comment(line) for line in text.splitlines())


def preamble_text(text: str) -> str:
    marker = r"\begin{document}"
    index = text.find(marker)
    return text if index == -1 else text[:index]


def parse_packages(preamble: str) -> set[str]:
    packages: set[str] = set()
    for match in USEPACKAGE_RE.finditer(preamble):
        for name in match.group(1).split(","):
            cleaned = name.strip().lower()
            if cleaned:
                packages.add(cleaned)
    return packages


def parse_documentclass(preamble: str) -> str:
    match = DOCUMENTCLASS_RE.search(preamble)
    return match.group(1).strip().lower() if match else ""


def find_includes(text: str) -> list[str]:
    return [match.group(1).strip() for match in INCLUDE_RE.finditer(text) if match.group(1).strip()]


def analyze_preamble(tex_path: Path) -> tuple[list[Diagnostic], list[str], set[str], str]:
    text = uncommented_text(read_text(tex_path))
    preamble = preamble_text(text)
    packages = parse_packages(preamble)
    documentclass = parse_documentclass(preamble)
    includes = find_includes(text)
    diagnostics: list[Diagnostic] = []

    fduthesis_like = "fduthesis" in documentclass
    unicode_math_loaded = fduthesis_like or "unicode-math" in packages
    conflicts = sorted(packages & UNICODE_MATH_CONFLICTS)
    if unicode_math_loaded and conflicts:
        diagnostics.append(
            Diagnostic(
                "ERROR",
                "fduthesis/unicode-math math setup conflicts with: " + ", ".join(conflicts),
                "Remove legacy math symbol/font packages such as amssymb and amsfonts; keep amsmath/mathtools if needed.",
            )
        )

    if fduthesis_like and "fontspec" in packages:
        diagnostics.append(
            Diagnostic(
                "WARN",
                "fduthesis usually owns fontspec/ctex font setup.",
                "Avoid reloading fontspec unless the template explicitly asks for it.",
            )
        )

    return diagnostics, includes, packages, documentclass


def print_preflight(diagnostics: list[Diagnostic], includes: list[str]) -> None:
    if diagnostics:
        print("Preflight diagnostics:")
        for item in diagnostics:
            print(f"  [{item.level}] {item.message}")
            print(f"    Action: {item.action}")
    else:
        print("Preflight diagnostics: no common fduthesis/LaTeX conflicts found.")

    if includes:
        print(f"Detected {len(includes)} \\include target(s).")


def resolved_output_dir(project_dir: Path, output_dir: str | None) -> Path | None:
    if not output_dir:
        return None
    raw = Path(output_dir)
    return raw if raw.is_absolute() else project_dir / raw


def ensure_output_dirs(project_dir: Path, output_dir: str | None, includes: list[str]) -> Path | None:
    out_dir = resolved_output_dir(project_dir, output_dir)
    if out_dir is None:
        return None

    out_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for include in includes:
        normalized = include.replace("\\", "/").strip()
        if not normalized:
            continue
        pure = PurePosixPath(normalized)
        if pure.is_absolute() or pure.parent == PurePosixPath("."):
            continue
        target = out_dir.joinpath(*pure.parent.parts)
        target.mkdir(parents=True, exist_ok=True)
        created.append(target)

    if created:
        rel = [relative_or_absolute(path, project_dir) for path in created]
        print("Prepared output subdirectories for \\include aux files: " + ", ".join(sorted(set(rel))))
    return out_dir


def choose_engine(engine: str, packages: set[str], documentclass: str) -> str:
    if engine != "auto":
        return engine
    if "fduthesis" in documentclass or "unicode-math" in packages or "fontspec" in packages or "ctex" in packages:
        return "xelatex"
    return "pdflatex"


def display_cmd(cmd: list[str]) -> str:
    return " ".join(f'"{part}"' if " " in part else part for part in cmd)


def run(cmd: list[str], cwd: Path) -> int:
    print("$ " + display_cmd(cmd))
    completed = subprocess.run(cmd, cwd=str(cwd))
    return completed.returncode


def latexmk_command(latexmk: str, engine: str, main_arg: str, output_dir: str | None) -> list[str]:
    engine_flag = {
        "xelatex": "-xelatex",
        "lualatex": "-lualatex",
        "pdflatex": "-pdf",
    }[engine]
    cmd = [
        latexmk,
        engine_flag,
        "-interaction=nonstopmode",
        "-file-line-error",
        "-halt-on-error",
    ]
    if output_dir:
        cmd.append(f"-outdir={output_dir}")
    cmd.append(main_arg)
    return cmd


def engine_command(engine_path: str, main_arg: str, output_dir: str | None) -> list[str]:
    cmd = [
        engine_path,
        "-interaction=nonstopmode",
        "-file-line-error",
        "-halt-on-error",
    ]
    if output_dir:
        cmd.append(f"-output-directory={output_dir}")
    cmd.append(main_arg)
    return cmd


def run_bibliography(project_dir: Path, out_dir: Path | None, main_stem: str) -> int:
    work_dir = out_dir or project_dir
    aux_path = work_dir / f"{main_stem}.aux"
    bcf_path = work_dir / f"{main_stem}.bcf"

    biber = shutil.which("biber")
    if bcf_path.exists() and biber:
        cmd = [biber]
        if out_dir:
            cmd.extend(["--input-directory", str(out_dir), "--output-directory", str(out_dir)])
        cmd.append(main_stem)
        return run(cmd, project_dir)

    bibtex = shutil.which("bibtex")
    if aux_path.exists() and bibtex:
        aux_text = aux_path.read_text(encoding="utf-8", errors="replace")
        if r"\bibdata" in aux_text or r"\citation" in aux_text:
            job = str(aux_path.with_suffix(""))
            return run([bibtex, job], project_dir)

    return 0


def compile_project(
    project_dir: Path,
    main_arg: str,
    engine: str,
    output_dir: str | None,
    out_dir: Path | None,
) -> int:
    latexmk = shutil.which("latexmk")
    if latexmk:
        return run(latexmk_command(latexmk, engine, main_arg, output_dir), project_dir)

    engine_path = shutil.which(engine)
    if not engine_path:
        print(f"error: neither latexmk nor {engine} is available on PATH.", file=sys.stderr)
        return 127

    first = run(engine_command(engine_path, main_arg, output_dir), project_dir)
    if first != 0:
        return first

    bib_code = run_bibliography(project_dir, out_dir, Path(main_arg).stem)
    if bib_code != 0:
        return bib_code

    code = 0
    for _ in range(2):
        code = run(engine_command(engine_path, main_arg, output_dir), project_dir)
        if code != 0:
            return code
    return code


def parse_pdf_from_log(log_path: Path, project_dir: Path) -> Path | None:
    if not log_path.exists():
        return None
    text = log_path.read_text(encoding="utf-8", errors="replace")
    matches = list(OUTPUT_RE.finditer(text))
    if not matches:
        return None
    raw = matches[-1].group(1).strip().strip("`'\"")
    path = Path(raw)
    return path if path.is_absolute() else project_dir / path


def candidate_logs(project_dir: Path, out_dir: Path | None, main_stem: str) -> list[Path]:
    candidates: list[Path] = []
    if out_dir:
        candidates.append(out_dir / f"{main_stem}.log")
    candidates.append(project_dir / f"{main_stem}.log")
    try:
        candidates.extend(project_dir.rglob(f"{main_stem}.log"))
    except OSError:
        pass
    return unique_existing(candidates)


def candidate_pdfs(project_dir: Path, out_dir: Path | None, main_stem: str, logs: list[Path]) -> list[Path]:
    candidates: list[Path] = []
    for log_path in logs:
        parsed = parse_pdf_from_log(log_path, project_dir)
        if parsed:
            candidates.append(parsed)
    if out_dir:
        candidates.append(out_dir / f"{main_stem}.pdf")
    candidates.append(project_dir / f"{main_stem}.pdf")
    try:
        candidates.extend(project_dir.rglob(f"{main_stem}.pdf"))
    except OSError:
        pass
    return unique_existing(candidates)


def unique_existing(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    result: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved in seen or not resolved.exists():
            continue
        seen.add(resolved)
        result.append(resolved)
    return result


def newest_fresh_pdf(candidates: list[Path], started_at: float) -> Path | None:
    fresh = [
        path
        for path in candidates
        if path.is_file() and path.stat().st_size > 0 and path.stat().st_mtime >= started_at - 1.0
    ]
    if not fresh:
        return None
    return max(fresh, key=lambda path: path.stat().st_mtime)


def log_has_output(logs: list[Path]) -> bool:
    for path in logs:
        text = path.read_text(encoding="utf-8", errors="replace")
        if OUTPUT_RE.search(text):
            return True
    return False


def log_has_fatal(logs: list[Path]) -> bool:
    for path in logs:
        text = path.read_text(encoding="utf-8", errors="replace")
        if any(pattern.search(text) for pattern in FATAL_LOG_PATTERNS):
            return True
    return False


def print_log_hints(logs: list[Path]) -> None:
    hints: list[str] = []
    for path in logs:
        text = path.read_text(encoding="utf-8", errors="replace")
        lowered = text.lower()
        if "already defined" in lowered and ("amssymb" in lowered or "amsfonts" in lowered or "bbbk" in lowered):
            hints.append("Remove amssymb/amsfonts when fduthesis or unicode-math is active.")
        if "i can't write on file" in lowered and ".aux" in lowered:
            hints.append("The output directory is missing subdirectories for \\include aux files; compile in project root or pre-create mirrored folders.")
        if "no file" in lowered and ".bbl" in lowered:
            hints.append("Run bibliography through latexmk, biber, or bibtex before the final two LaTeX passes.")

    if hints:
        print("Log hints:")
        for hint in sorted(set(hints)):
            print(f"  - {hint}")


def relative_or_absolute(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a LaTeX project and verify the actual PDF artifact.")
    parser.add_argument("--project-dir", default=".", help="Directory containing the LaTeX project.")
    parser.add_argument("--main", default="main.tex", help="Root .tex file relative to project-dir.")
    parser.add_argument(
        "--engine",
        choices=["auto", "xelatex", "lualatex", "pdflatex"],
        default="auto",
        help="LaTeX engine. auto prefers xelatex for fduthesis/unicode-math/ctex projects.",
    )
    parser.add_argument(
        "--output-dir",
        help="Optional output directory. The script prepares subdirectories needed by \\include.",
    )
    parser.add_argument(
        "--preflight-only",
        action="store_true",
        help="Only scan the preamble and include paths; do not run a compiler.",
    )
    parser.add_argument(
        "--strict-exit-code",
        action="store_true",
        help="Return the compiler exit code even when a fresh PDF artifact was produced.",
    )
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    main_path = Path(args.main)
    tex_path = main_path if main_path.is_absolute() else project_dir / main_path
    if not tex_path.exists():
        print(f"error: root TeX file not found: {tex_path}", file=sys.stderr)
        return 1

    main_arg = str(main_path if not main_path.is_absolute() else tex_path)
    diagnostics, includes, packages, documentclass = analyze_preamble(tex_path)
    print_preflight(diagnostics, includes)
    if args.preflight_only:
        return 2 if any(item.level == "ERROR" for item in diagnostics) else 0

    engine = choose_engine(args.engine, packages, documentclass)
    out_dir = ensure_output_dirs(project_dir, args.output_dir, includes)
    started_at = time.time()
    code = compile_project(project_dir, main_arg, engine, args.output_dir, out_dir)

    main_stem = tex_path.stem
    logs = candidate_logs(project_dir, out_dir, main_stem)
    print_log_hints(logs)
    pdfs = candidate_pdfs(project_dir, out_dir, main_stem, logs)
    fresh_pdf = newest_fresh_pdf(pdfs, started_at)
    has_output_line = log_has_output(logs)
    has_fatal = log_has_fatal(logs)

    if fresh_pdf and (code == 0 or (has_output_line and not has_fatal)):
        print("PDF: " + relative_or_absolute(fresh_pdf, project_dir))
        if code != 0:
            print(
                f"warning: compiler returned {code}, but a fresh PDF was verified from the log/artifact check.",
                file=sys.stderr,
            )
            return code if args.strict_exit_code else 0
        return 0

    if fresh_pdf:
        print("Partial PDF: " + relative_or_absolute(fresh_pdf, project_dir), file=sys.stderr)
    elif pdfs:
        newest = max(pdfs, key=lambda path: path.stat().st_mtime)
        print(
            "error: found only stale PDF candidates; newest is "
            + relative_or_absolute(newest, project_dir),
            file=sys.stderr,
        )
    else:
        print("error: no PDF artifact found after compilation.", file=sys.stderr)

    if has_fatal:
        print("error: LaTeX log contains fatal errors.", file=sys.stderr)
    return code if code != 0 else 1


if __name__ == "__main__":
    os.environ.setdefault("max_print_line", "1000")
    raise SystemExit(main())

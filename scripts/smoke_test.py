#!/usr/bin/env python3
"""Repository smoke checks that should stay fast and deterministic."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "fdu-final-paper-skill"


def run(cmd: list[str]) -> None:
    run_checked(cmd)


def format_command(cmd: list[str]) -> str:
    return " ".join(str(part) for part in cmd)


def run_checked(
    cmd: list[str],
    *,
    cwd: Path = ROOT,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and completed.returncode != 0:
        print("Smoke command failed.", file=sys.stderr)
        print(f"Command: {format_command(cmd)}", file=sys.stderr)
        print(f"CWD: {cwd}", file=sys.stderr)
        print(f"Return code: {completed.returncode}", file=sys.stderr)
        print("--- stdout ---", file=sys.stderr)
        print(completed.stdout or "<empty>", file=sys.stderr)
        print("--- stderr ---", file=sys.stderr)
        print(completed.stderr or "<empty>", file=sys.stderr)
        raise SystemExit(completed.returncode)
    return completed


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing required path: {path.relative_to(ROOT)}")


def main() -> int:
    require(ROOT / "LICENSE")
    require(ROOT / "NOTICE")
    require(ROOT / "CONTRIBUTING.md")
    require(ROOT / "CHANGELOG.md")
    require(ROOT / ".gitignore")
    require(SKILL_DIR / "SKILL.md")
    require(SKILL_DIR / "references" / "compliance-source-policy.md")
    require(SKILL_DIR / "references" / "fudan-2026-format-checklist.md")
    require(SKILL_DIR / "references" / "latex-compile-debugging.md")
    require(SKILL_DIR / "scripts" / "check_fudan_spec_update.py")
    require(SKILL_DIR / "scripts" / "compile_latex_project.py")
    require(SKILL_DIR / "scripts" / "read_reference_file.py")

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
    run([sys.executable, "scripts/check_eval_outputs.py"])

    run([sys.executable, "scripts/quick_validate.py", str(SKILL_DIR)])
    validator_spec = importlib.util.spec_from_file_location(
        "quick_validate", ROOT / "scripts" / "quick_validate.py"
    )
    if validator_spec is None or validator_spec.loader is None:
        raise SystemExit("Could not load quick_validate.py for frontmatter regression check.")
    validator = importlib.util.module_from_spec(validator_spec)
    validator_spec.loader.exec_module(validator)
    frontmatter, frontmatter_errors = validator.parse_frontmatter(SKILL_DIR / "SKILL.md")
    if frontmatter_errors:
        raise SystemExit("Frontmatter parser returned errors: " + "; ".join(frontmatter_errors))
    description = frontmatter.get("description")
    if not isinstance(description, str) or description.strip() in {">", "|"}:
        raise SystemExit("Frontmatter description block scalar was not parsed correctly.")
    if "Fudan University" not in description or "复旦学位论文" not in description:
        raise SystemExit("Frontmatter description lost expected trigger text.")

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

    with tempfile.TemporaryDirectory(prefix="fdu-skill-") as tmpdir:
        sample = Path(tmpdir) / "中文参考.txt"
        sample.write_text("复旦论文参考文件\nEnglish reference text", encoding="utf-8")
        env = os.environ.copy()
        env["FDU_REFERENCE_PATH"] = str(sample)
        completed = run_checked(
            [
                sys.executable,
                str(SKILL_DIR / "scripts" / "read_reference_file.py"),
                "--path-env",
                "FDU_REFERENCE_PATH",
                "--max-chars",
                "500",
            ],
            env=env,
        )
        if "复旦论文参考文件" not in completed.stdout:
            raise SystemExit("Reference reader failed to preserve Chinese text.")

        docx_sample = Path(tmpdir) / "英文与中文.docx"
        document_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p><w:r><w:t>DOCX中文内容</w:t></w:r></w:p>
    <w:p><w:r><w:t>English DOCX content</w:t></w:r></w:p>
  </w:body>
</w:document>
"""
        with zipfile.ZipFile(docx_sample, "w") as docx:
            docx.writestr("word/document.xml", document_xml)
        env["FDU_DOCX_PATH"] = str(docx_sample)
        completed = run_checked(
            [
                sys.executable,
                str(SKILL_DIR / "scripts" / "read_reference_file.py"),
                "--path-env",
                "FDU_DOCX_PATH",
                "--max-chars",
                "500",
            ],
            env=env,
        )
        if "DOCX中文内容" not in completed.stdout:
            raise SystemExit("Reference reader failed to extract DOCX text.")

        pdf_sample = Path(tmpdir) / "复旦PDF参考.pdf"
        pdf_sample.write_bytes(b"%PDF-1.4\n% smoke-test placeholder\n")

        fake_modules = Path(tmpdir) / "fake-pdf-modules"
        fake_modules.mkdir()
        for module_name in ("pypdf", "PyPDF2", "pdfplumber", "fitz"):
            (fake_modules / f"{module_name}.py").write_text(
                "raise ImportError('forced fallback for smoke test')\n",
                encoding="utf-8",
            )

        fake_bin = Path(tmpdir) / "fake-pdf-bin"
        fake_bin.mkdir()
        fake_pdftotext = fake_bin / "fake_pdftotext.py"
        fake_pdftotext.write_text(
            "import sys\n"
            "sys.stdout.buffer.write('PDF中文内容\\nEnglish PDF content\\n'.encode('utf-8'))\n",
            encoding="utf-8",
        )
        if os.name == "nt":
            launcher = fake_bin / "pdftotext.cmd"
            launcher.write_text(
                f'@echo off\n"{sys.executable}" "%~dp0fake_pdftotext.py" %*\n',
                encoding="utf-8",
            )
        else:
            launcher = fake_bin / "pdftotext"
            launcher.write_text(
                f"#!{sys.executable}\n"
                "from pathlib import Path\n"
                "import runpy\n"
                "runpy.run_path(str(Path(__file__).with_name('fake_pdftotext.py')), run_name='__main__')\n",
                encoding="utf-8",
            )
            launcher.chmod(0o755)

        env["FDU_PDF_PATH"] = str(pdf_sample)
        env["PATH"] = str(fake_bin) + os.pathsep + env.get("PATH", "")
        env["PYTHONPATH"] = str(fake_modules) + os.pathsep + env.get("PYTHONPATH", "")
        completed = run_checked(
            [
                sys.executable,
                str(SKILL_DIR / "scripts" / "read_reference_file.py"),
                "--path-env",
                "FDU_PDF_PATH",
                "--max-chars",
                "500",
            ],
            env=env,
        )
        if "PDF中文内容" not in completed.stdout or "pdf:pdftotext" not in completed.stdout:
            raise SystemExit(
                "Reference reader failed to extract PDF text through pdftotext fallback.\n"
                "--- stdout ---\n"
                + (completed.stdout or "<empty>")
                + "\n--- stderr ---\n"
                + (completed.stderr or "<empty>")
            )

    with tempfile.TemporaryDirectory(prefix="fdu-latex-") as tmpdir:
        project = Path(tmpdir) / "thesis"
        project.mkdir()
        (project / "chapters").mkdir()
        (project / "main.tex").write_text(
            r"""\documentclass{fduthesis}
\usepackage{amsmath}
\usepackage{amssymb}
\begin{document}
\include{chapters/intro}
\end{document}
""",
            encoding="utf-8",
        )
        (project / "chapters" / "intro.tex").write_text("正文", encoding="utf-8")

        completed = run_checked(
            [
                sys.executable,
                str(SKILL_DIR / "scripts" / "compile_latex_project.py"),
                "--project-dir",
                str(project),
                "--main",
                "main.tex",
                "--preflight-only",
            ],
            check=False,
        )
        if completed.returncode != 2 or "amssymb" not in completed.stdout:
            raise SystemExit(
                "LaTeX preflight did not flag fduthesis/amssymb conflict.\n"
                "--- stdout ---\n"
                + (completed.stdout or "<empty>")
                + "\n--- stderr ---\n"
                + (completed.stderr or "<empty>")
            )

        fake_bin = Path(tmpdir) / "fake-bin"
        fake_bin.mkdir()
        fake_latexmk = fake_bin / "fake_latexmk.py"
        fake_latexmk.write_text(
            """
from pathlib import Path
import sys

outdir = "."
main = "main.tex"
for arg in sys.argv[1:]:
    if arg.startswith("-outdir="):
        outdir = arg.split("=", 1)[1]
    elif arg.endswith(".tex"):
        main = arg

out = Path(outdir)
out.mkdir(parents=True, exist_ok=True)
if not (out / "chapters").is_dir():
    print("I can't write on file 'chapters/intro.aux'.", file=sys.stderr)
    raise SystemExit(1)

stem = Path(main).stem
(out / f"{stem}.pdf").write_bytes(b"%PDF-1.4\\n% fake\\n")
(out / f"{stem}.log").write_text(
    f"Output written on {outdir}/{stem}.pdf (1 page, 12 bytes).\\n",
    encoding="utf-8",
)
raise SystemExit(12)
""".lstrip(),
            encoding="utf-8",
        )
        if os.name == "nt":
            launcher = fake_bin / "latexmk.cmd"
            launcher.write_text(f'@echo off\n"{sys.executable}" "%~dp0fake_latexmk.py" %*\n', encoding="utf-8")
        else:
            launcher = fake_bin / "latexmk"
            launcher.write_text(
                f"#!{sys.executable}\n"
                "from pathlib import Path\n"
                "import runpy\n"
                "runpy.run_path(str(Path(__file__).with_name('fake_latexmk.py')), run_name='__main__')\n",
                encoding="utf-8",
            )
            launcher.chmod(0o755)

        tex_text = (project / "main.tex").read_text(encoding="utf-8")
        tex_text = tex_text.replace("\\usepackage{amssymb}\n", "")
        (project / "main.tex").write_text(tex_text, encoding="utf-8")

        env = os.environ.copy()
        env["PATH"] = str(fake_bin) + os.pathsep + env.get("PATH", "")
        completed = run_checked(
            [
                sys.executable,
                str(SKILL_DIR / "scripts" / "compile_latex_project.py"),
                "--project-dir",
                str(project),
                "--main",
                "main.tex",
                "--engine",
                "xelatex",
                "--output-dir",
                "build",
            ],
            env=env,
            check=False,
        )
        if completed.returncode != 0:
            raise SystemExit(
                "LaTeX helper treated a verified fresh PDF as failure.\n"
                + completed.stdout
                + completed.stderr
            )
        if "PDF: build" not in completed.stdout or "compiler returned 12" not in completed.stderr:
            raise SystemExit("LaTeX helper did not report verified build PDF with wrapper warning.")

    print("Smoke tests passed!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

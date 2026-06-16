#!/usr/bin/env python3
"""Extract text from reference PDFs, DOCX files, and text-like files.

The script is designed for thesis workflows where file paths may contain CJK
characters. If a shell mangles a path, pass it through an environment variable:

  python read_reference_file.py --path-env REF_FILE
"""

from __future__ import annotations

import argparse
import glob as globlib
import os
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable
from xml.etree import ElementTree as ET


TEXT_EXTENSIONS = {
    ".bib",
    ".csv",
    ".json",
    ".latex",
    ".log",
    ".md",
    ".rst",
    ".tex",
    ".text",
    ".tsv",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

DOCX_PARTS = [
    ("word/document.xml", "Main document"),
    ("word/footnotes.xml", "Footnotes"),
    ("word/endnotes.xml", "Endnotes"),
    ("word/comments.xml", "Comments"),
    ("word/header1.xml", "Header 1"),
    ("word/header2.xml", "Header 2"),
    ("word/header3.xml", "Header 3"),
    ("word/footer1.xml", "Footer 1"),
    ("word/footer2.xml", "Footer 2"),
    ("word/footer3.xml", "Footer 3"),
]

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


class ExtractionError(RuntimeError):
    """Raised when no extraction backend can handle a file."""


@dataclass
class ExtractionResult:
    path: Path
    method: str
    text: str
    warnings: list[str]
    error: str | None = None


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def parse_page_spec(spec: str | None) -> set[int] | None:
    if not spec:
        return None

    pages: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            start_raw, end_raw = chunk.split("-", 1)
            start = int(start_raw)
            end = int(end_raw)
            if start < 1 or end < start:
                raise ValueError(f"Invalid page range: {chunk}")
            pages.update(range(start - 1, end))
        else:
            page = int(chunk)
            if page < 1:
                raise ValueError(f"Invalid page number: {chunk}")
            pages.add(page - 1)
    return pages


def selected(page_index: int, pages: set[int] | None) -> bool:
    return pages is None or page_index in pages


def expand_path(raw: str) -> Path:
    trimmed = raw.strip()
    if (trimmed.startswith('"') and trimmed.endswith('"')) or (
        trimmed.startswith("'") and trimmed.endswith("'")
    ):
        trimmed = trimmed[1:-1]
    return Path(os.path.expandvars(os.path.expanduser(trimmed)))


def split_path_list(raw: str) -> list[str]:
    if "\n" in raw:
        return [line.strip() for line in raw.splitlines() if line.strip()]
    return [part.strip() for part in raw.split(os.pathsep) if part.strip()]


def gather_paths(args: argparse.Namespace) -> tuple[list[Path], list[str]]:
    raw_paths = list(args.files)
    warnings: list[str] = []

    for env_name in args.path_env:
        value = os.environ.get(env_name)
        if value:
            raw_paths.append(value)
        else:
            warnings.append(f"Environment variable {env_name!r} is not set.")

    for env_name in args.list_env:
        value = os.environ.get(env_name)
        if value:
            raw_paths.extend(split_path_list(value))
        else:
            warnings.append(f"Environment variable {env_name!r} is not set.")

    for pattern in args.glob:
        matches = sorted(globlib.glob(pattern))
        if matches:
            raw_paths.extend(matches)
        else:
            warnings.append(f"Glob pattern matched no files: {pattern}")

    paths: list[Path] = []
    seen: set[Path] = set()
    for raw in raw_paths:
        path = expand_path(raw)
        key = path.resolve() if path.exists() else path.absolute()
        if key not in seen:
            seen.add(key)
            paths.append(path)

    return paths, warnings


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x00", "")
    while "\n\n\n\n" in text:
        text = text.replace("\n\n\n\n", "\n\n\n")
    return text.strip()


def read_text_file(path: Path, encoding: str | None) -> tuple[str, str, list[str]]:
    encodings = [encoding] if encoding else [
        "utf-8-sig",
        "utf-8",
        "gb18030",
        "gbk",
        "big5",
        "utf-16",
        "latin-1",
    ]
    errors: list[str] = []

    for candidate in encodings:
        try:
            return path.read_text(encoding=candidate), f"text:{candidate}", []
        except UnicodeDecodeError as exc:
            errors.append(f"{candidate}: {exc}")

    raise ExtractionError("Could not decode text file. Tried " + "; ".join(errors))


def paragraph_text(paragraph: ET.Element) -> str:
    pieces: list[str] = []
    for node in paragraph.iter():
        if node.tag == f"{W}t" and node.text:
            pieces.append(node.text)
        elif node.tag == f"{W}tab":
            pieces.append("\t")
        elif node.tag in {f"{W}br", f"{W}cr"}:
            pieces.append("\n")
    return "".join(pieces).strip()


def table_text(table: ET.Element) -> str:
    rows: list[str] = []
    for row in table.findall(f".//{W}tr"):
        cells: list[str] = []
        for cell in row.findall(f"{W}tc"):
            paragraphs: list[str] = []
            for paragraph in cell.findall(f"{W}p"):
                text = paragraph_text(paragraph)
                if text:
                    paragraphs.append(text)
            cells.append(" / ".join(paragraphs))
        if any(cells):
            rows.append("\t".join(cells))
    return "\n".join(rows)


def body_text(root: ET.Element) -> str:
    body = root.find(f"{W}body")
    elements = list(body) if body is not None else list(root)
    blocks: list[str] = []

    for element in elements:
        if element.tag == f"{W}p":
            text = paragraph_text(element)
        elif element.tag == f"{W}tbl":
            text = table_text(element)
        else:
            nested = [paragraph_text(paragraph) for paragraph in element.findall(f".//{W}p")]
            text = "\n".join(item for item in nested if item)
        if text:
            blocks.append(text)

    return "\n\n".join(blocks)


def extract_docx(path: Path) -> tuple[str, str, list[str]]:
    sections: list[str] = []
    warnings: list[str] = []

    try:
        with zipfile.ZipFile(path) as docx:
            names = set(docx.namelist())
            for part, label in DOCX_PARTS:
                if part not in names:
                    continue
                try:
                    root = ET.fromstring(docx.read(part))
                except ET.ParseError as exc:
                    warnings.append(f"Skipped malformed DOCX part {part}: {exc}")
                    continue
                text = body_text(root)
                if text:
                    sections.append(f"[{label}]\n{text}")
    except zipfile.BadZipFile as exc:
        raise ExtractionError(f"Not a valid DOCX/ZIP file: {exc}") from exc

    if not sections:
        raise ExtractionError("DOCX contained no extractable text.")

    return "\n\n".join(sections), "docx:stdlib-ooxml", warnings


def extract_pdf_with_pypdf(path: Path, pages: set[int] | None) -> tuple[str, str, list[str]]:
    try:
        try:
            from pypdf import PdfReader  # type: ignore
        except ImportError:
            from PyPDF2 import PdfReader  # type: ignore
    except ImportError as exc:
        raise ExtractionError(f"pypdf/PyPDF2 unavailable: {exc}") from exc

    reader = PdfReader(str(path))
    warnings: list[str] = []
    if getattr(reader, "is_encrypted", False):
        try:
            reader.decrypt("")
        except Exception as exc:  # pragma: no cover - backend dependent
            warnings.append(f"PDF is encrypted and empty-password decrypt failed: {exc}")

    blocks: list[str] = []
    for index, page in enumerate(reader.pages):
        if not selected(index, pages):
            continue
        text = page.extract_text() or ""
        if text.strip():
            blocks.append(f"[Page {index + 1}]\n{text.strip()}")

    if not blocks:
        raise ExtractionError("pypdf/PyPDF2 extracted no text.")
    return "\n\n".join(blocks), "pdf:pypdf", warnings


def extract_pdf_with_pdfplumber(path: Path, pages: set[int] | None) -> tuple[str, str, list[str]]:
    try:
        import pdfplumber  # type: ignore
    except ImportError as exc:
        raise ExtractionError(f"pdfplumber unavailable: {exc}") from exc

    blocks: list[str] = []
    with pdfplumber.open(path) as pdf:
        for index, page in enumerate(pdf.pages):
            if not selected(index, pages):
                continue
            text = page.extract_text() or ""
            if text.strip():
                blocks.append(f"[Page {index + 1}]\n{text.strip()}")

    if not blocks:
        raise ExtractionError("pdfplumber extracted no text.")
    return "\n\n".join(blocks), "pdf:pdfplumber", []


def extract_pdf_with_pymupdf(path: Path, pages: set[int] | None) -> tuple[str, str, list[str]]:
    try:
        import fitz  # type: ignore
    except ImportError as exc:
        raise ExtractionError(f"PyMuPDF unavailable: {exc}") from exc

    blocks: list[str] = []
    with fitz.open(path) as document:
        for index, page in enumerate(document):
            if not selected(index, pages):
                continue
            text = page.get_text("text") or ""
            if text.strip():
                blocks.append(f"[Page {index + 1}]\n{text.strip()}")

    if not blocks:
        raise ExtractionError("PyMuPDF extracted no text.")
    return "\n\n".join(blocks), "pdf:pymupdf", []


def extract_pdf_with_pdftotext(path: Path, pages: set[int] | None) -> tuple[str, str, list[str]]:
    command = ["pdftotext", "-layout", "-enc", "UTF-8"]
    warnings: list[str] = []

    if pages:
        ordered = sorted(pages)
        if ordered == list(range(ordered[0], ordered[-1] + 1)):
            command.extend(["-f", str(ordered[0] + 1), "-l", str(ordered[-1] + 1)])
        else:
            warnings.append("pdftotext fallback can only honor a contiguous page range.")

    command.extend([str(path), "-"])

    try:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except FileNotFoundError as exc:
        raise ExtractionError(f"pdftotext unavailable: {exc}") from exc

    if completed.returncode != 0:
        raise ExtractionError(completed.stderr.strip() or "pdftotext failed.")

    if not completed.stdout.strip():
        raise ExtractionError("pdftotext extracted no text.")

    return completed.stdout, "pdf:pdftotext", warnings


def extract_pdf(path: Path, pages: set[int] | None) -> tuple[str, str, list[str]]:
    backends: list[Callable[[Path, set[int] | None], tuple[str, str, list[str]]]] = [
        extract_pdf_with_pypdf,
        extract_pdf_with_pdfplumber,
        extract_pdf_with_pymupdf,
        extract_pdf_with_pdftotext,
    ]
    errors: list[str] = []

    for backend in backends:
        try:
            return backend(path, pages)
        except ExtractionError as exc:
            errors.append(str(exc))

    raise ExtractionError("No PDF backend succeeded. " + " | ".join(errors))


def extract_file(path: Path, args: argparse.Namespace, pages: set[int] | None) -> ExtractionResult:
    if not path.exists():
        return ExtractionResult(path=path, method="missing", text="", warnings=[], error="File not found.")
    if not path.is_file():
        return ExtractionResult(path=path, method="not-file", text="", warnings=[], error="Path is not a file.")

    suffix = path.suffix.lower()
    try:
        if suffix == ".pdf":
            text, method, warnings = extract_pdf(path, pages)
        elif suffix == ".docx":
            text, method, warnings = extract_docx(path)
        elif suffix == ".doc":
            raise ExtractionError("Legacy .doc is binary; convert it to .docx before extraction.")
        elif suffix in TEXT_EXTENSIONS:
            text, method, warnings = read_text_file(path, args.encoding)
        else:
            text, method, warnings = read_text_file(path, args.encoding)
            warnings.append(f"Unknown extension {suffix or '<none>'}; treated as text.")
    except ExtractionError as exc:
        return ExtractionResult(path=path, method=suffix or "unknown", text="", warnings=[], error=str(exc))

    return ExtractionResult(path=path, method=method, text=clean_text(text), warnings=warnings)


def truncate(text: str, max_chars: int) -> tuple[str, str | None]:
    if max_chars <= 0 or len(text) <= max_chars:
        return text, None
    omitted = len(text) - max_chars
    return text[:max_chars].rstrip(), f"Output truncated after {max_chars} characters; omitted {omitted}."


def render_markdown(results: list[ExtractionResult], global_warnings: list[str], max_chars: int) -> str:
    lines = ["# Reference File Extraction", ""]
    for warning in global_warnings:
        lines.extend([f"> Warning: {warning}", ""])

    for index, result in enumerate(results, start=1):
        lines.extend(
            [
                f"## File {index}: {result.path.name}",
                "",
                f"- Path: `{result.path}`",
                f"- Method: `{result.method}`",
            ]
        )

        if result.error:
            lines.extend([f"- Error: {result.error}", ""])
            continue

        for warning in result.warnings:
            lines.append(f"- Warning: {warning}")

        text, note = truncate(result.text, max_chars)
        if note:
            lines.append(f"- Warning: {note}")

        lines.extend(["", "### Extracted Text", "", text, ""])

    return "\n".join(lines).rstrip() + "\n"


def render_plain(results: list[ExtractionResult], global_warnings: list[str], max_chars: int) -> str:
    chunks: list[str] = []
    for warning in global_warnings:
        chunks.append(f"Warning: {warning}")
    for result in results:
        header = f"===== {result.path} ({result.method}) ====="
        if result.error:
            chunks.append(f"{header}\nERROR: {result.error}")
            continue
        text, note = truncate(result.text, max_chars)
        if note:
            chunks.append(f"{header}\nWarning: {note}\n{text}")
        else:
            chunks.append(f"{header}\n{text}")
    return "\n\n".join(chunks).rstrip() + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read PDF, DOCX, and text reference files with UTF-8-safe output."
    )
    parser.add_argument("files", nargs="*", help="Reference file paths.")
    parser.add_argument(
        "--path-env",
        action="append",
        default=[],
        metavar="ENV",
        help="Read one file path from environment variable ENV. Repeat as needed.",
    )
    parser.add_argument(
        "--list-env",
        action="append",
        default=[],
        metavar="ENV",
        help="Read multiple paths from ENV, split by newlines or the OS path separator.",
    )
    parser.add_argument(
        "--glob",
        action="append",
        default=[],
        metavar="PATTERN",
        help="Add files matched by a glob pattern relative to the current directory.",
    )
    parser.add_argument("--pages", help="PDF pages to read, 1-based, e.g. 1-3,5.")
    parser.add_argument("--encoding", help="Force an encoding for text-like files.")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=60000,
        help="Maximum characters to output per file; use 0 for no limit.",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "plain"],
        default="markdown",
        help="Output format.",
    )
    parser.add_argument("-o", "--output", type=Path, help="Write UTF-8 output to this file.")
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        pages = parse_page_spec(args.pages)
    except ValueError as exc:
        parser.error(str(exc))

    paths, global_warnings = gather_paths(args)
    if not paths:
        parser.error("No input files provided. Use a path, --path-env, --list-env, or --glob.")

    results = [extract_file(path, args, pages) for path in paths]
    output = (
        render_markdown(results, global_warnings, args.max_chars)
        if args.format == "markdown"
        else render_plain(results, global_warnings, args.max_chars)
    )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    return 1 if any(result.error for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())

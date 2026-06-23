---
name: fdu-final-paper-skill
description: >
  Use when Codex needs to plan, outline, draft, revise, format-check, or audit
  a Fudan University master's or doctoral thesis/dissertation in Chinese,
  English, or bilingual form. Trigger for Chinese requests such as 复旦毕业论文,
  复旦学位论文, 硕士论文, 博士论文, 论文目录, 摘要润色, 绪论修改, 结论与展望, 答辩前检查,
  格式审查, 合规检查, 复旦 2026 论文规范, claim-evidence 对齐, LaTeX/BibTeX,
  fduthesis 编译调试, 自定义院系规范, 合规来源文件夹, or DOCX editing
  for Fudan degree-thesis files.
  Covers graduate thesis structure, chapter logic, abstract/front matter,
  references, appendices, publication records, acknowledgements,
  defense-readiness, LaTeX compilation diagnostics, default Fudan 2026 thesis
  compliance, and user-supplied compliance sources without assuming any
  particular research field.
---

# Fudan Graduate Thesis Skill

## Core Orientation

Use this skill as a general graduate thesis assistant for Fudan University. Do not assume a fixed discipline, chapter sequence, method type, or product-development pipeline. Let the user's degree type, school/department rules, research question, evidence, and target submission batch determine the structure.

Always treat official Fudan Graduate School and department documents as the final authority for cover pages, typography, binding, submission, secrecy, and fee forms. The bundled Fudan 2026.06 checklist is the default compliance and template baseline, not the only valid source. If the user supplies newer, stricter, department-specific, or supervisor-provided links, files, folders, templates, or extracted rule text, read those sources and use them for the relevant checks while recording how they relate to the default baseline.

When exact formatting or submission requirements matter, read `references/fudan-2026-format-checklist.md` and verify against:

- Fudan thesis specification page: https://gs.fudan.edu.cn/6b/9f/c2806a27551/page.htm
- Fudan Graduate School thesis-spec list: https://gs.fudan.edu.cn/2806/list.htm

Read `references/compliance-source-policy.md` when the user provides alternative compliance links, rule files, template files, folders, or glob patterns.

## Compliance Source Selection

Use the Fudan 2026.06 checklist as the default rule set when no other compliance source is provided. Accept user-supplied compliance links, PDFs, DOCX files, Markdown/text files, LaTeX template files, extracted rule text, folders, and glob patterns.

When sources conflict, prefer the current official Graduate School rule, then stricter or more specific current department/program rules, then user-provided supervisor or administrative instructions, then the bundled Fudan 2026.06 default. Treat old public samples and old templates as historical context only.

For local compliance files or folders, use the bundled reader before auditing:

```bash
python scripts/read_reference_file.py --glob "rules/**/*.pdf" -o extracted-compliance-sources.md
```

If the user provides a URL and network access is unavailable, ask them to upload the document or paste extracted text. Do not silently replace an unavailable custom source with the Fudan 2026.06 default; mark the source as unverified or missing.

Every compliance report should state which sources were used, whether Fudan 2026.06 was the default baseline or only a fallback for missing items, and which conflicts or unknowns need department or Graduate School confirmation.

## Optional External Skill Modules

This repository keeps optional implementation helpers outside the core skill so the installed skill stays lightweight and redistributable. Load them only when the task needs that format-specific workflow and the files are available in the current repository checkout.

- LaTeX paper/project workflow, when using this repository checkout: `../../embedded/latex-paper-skills/.codex/skills/`
  - Use when the user needs a LaTeX thesis or paper project, BibTeX checking, citation validation, issue-gated writing, compilation, or result back-filling.
  - Start from `paper-from-zero` when topic-to-paper routing is unclear, `arxiv-paper-writer` for review/survey papers, `empirical-paper-writer` for evidence-bearing experimental papers, `results-backfill` after verified results arrive, and `latex-rhythm-refiner` for post-draft prose rhythm.
  - For Fudan thesis tasks, reuse the LaTeX, BibTeX, citation-audit, planning, and QA mechanics only. Do not inherit ML/AI, arXiv, IEEEtran, page-limit, or two-column assumptions unless the user explicitly asks for them. Use the official Fudan or department thesis template when formatting a degree thesis.
- Word DOCX workflow:
  - Use the active document/DOCX capability already available in the current Codex environment when the user needs to create, inspect, edit, comment on, or redline `.docx` thesis files.
  - If no DOCX skill or document plugin is available, produce a Markdown or LaTeX revision package and tell the user which DOCX-capable skill/plugin should be installed or enabled. Do not assume a vendored DOCX module exists in this repository.

## Reading User-Supplied Reference Files

Before analyzing user-provided reference files, prefer the bundled reader for `.pdf`, `.docx`, `.txt`, `.md`, `.tex`, `.bib`, and other text-like files:

```bash
python scripts/read_reference_file.py "path/to/reference.pdf" --max-chars 80000
```

When a path contains Chinese characters, spaces, or shell escaping fails, do not spend time retrying ad hoc commands. Pass the path through an environment variable and rerun:

```powershell
$env:FDU_REF_FILE = "D:\论文资料\参考文献\中文论文.docx"
python scripts/read_reference_file.py --path-env FDU_REF_FILE -o extracted-reference.md
```

```bash
export FDU_REF_FILE="/path/to/论文资料/reference.pdf"
python scripts/read_reference_file.py --path-env FDU_REF_FILE -o extracted-reference.md
```

Use `--pages 1-5` for long PDFs, `--max-chars 0` when full extraction is needed, and `--list-env` when the user supplies multiple files through one environment variable. PDF extraction requires at least one backend: `pypdf`/`PyPDF2`, `pdfplumber`, `PyMuPDF`, or Poppler `pdftotext`. If PDF extraction reports that no backend succeeded, treat the file as likely scanned or image-only and switch to an OCR-capable PDF workflow. If the input is legacy `.doc`, ask for or create a `.docx` conversion before relying on text extraction.

## LaTeX Compilation Debugging

Read `references/latex-compile-debugging.md` when the task involves LaTeX compilation, `fduthesis`, XeLaTeX/LuaLaTeX, BibTeX/Biber, package conflicts, wrapper scripts, output directories, `aux` files, or a generated PDF that a script reports as failed.

When the bundled scripts are available, prefer this helper before hand-rolling compile commands:

```bash
python scripts/compile_latex_project.py --project-dir . --main main.tex --engine auto
```

Use `--output-dir build` only when the user or project already uses a build directory. The helper pre-creates `\include` aux subdirectories and verifies the actual fresh PDF path instead of assuming the PDF is beside the root `.tex` file.

For Fudan thesis projects using `fduthesis` or `unicode-math`, do not add `amssymb`, `amsfonts`, or legacy math font packages while debugging symbol errors. Remove the duplicate math package first, then compile once and inspect the first fatal log error.

## Default Workflow

1. Identify the task: outline planning, section drafting, revision, compliance check, LaTeX project work, Word editing, or defense-readiness audit.
2. Capture thesis context: degree level, language, department rules, compliance/template sources, submission batch, title/topic, research object, methods, evidence, figures/tables, publication outputs, and supervisor requirements.
3. Build the thesis story before polishing sentences: problem -> gap -> objective -> method/material -> evidence -> findings -> contribution -> limitation.
4. Choose a chapter architecture that follows the evidence, not a discipline stereotype.
5. Draft or revise section by section with explicit claim-evidence checks.
6. Select the compliance source set, defaulting to Fudan 2026.06 when no override is supplied, then check front matter, abstract/keywords, figure/table lists, references, notes, appendices, and required declarations.
7. Finalize with a consistency audit: abstract, introduction objectives, chapter summaries, final conclusions, innovations, and limitations must say the same thing.

## Architecture and Section Writing References

Read `references/thesis-architecture.md` when the user asks for a thesis outline, chapter tree, table of contents, chapter sequence, whole-thesis structure, degree-level architecture, article-based dissertation plan, or practice/design/application-oriented thesis organization.

Read `references/section-writing.md` when the user asks to draft, revise, compare, or audit an abstract, introduction, method/theory/data/foundation chapter, core research chapter, final chapter, conclusion, contribution section, limitation section, or chapter summary.

## Writing Quality Checks

Read `references/writing-quality-checklist.md` when the task is paragraph revision, chapter drafting, or reviewer-style self-check. Core checks:

- One paragraph should carry one message.
- The first sentence should orient the reader.
- Every major claim needs evidence, citation, figure/table support, or a clear marker that evidence is missing.
- Terms, abbreviations, names, variables, and translated concepts must be consistent.
- Figures and tables should be introduced before they appear and interpreted after they appear.
- Unsupported claims should be weakened, marked as pending, or removed.

## Compliance Checks and Default Fudan 2026 Baseline

Read `references/fudan-2026-format-checklist.md` when the user asks for formatting, pre-submission checks, cover/front matter, references, notes, or a September 2026-or-later submission and does not provide a more specific compliance source. If the user provides custom compliance links, files, folders, or templates, also read `references/compliance-source-policy.md` and apply those sources according to their authority and scope.

When the repository scripts are available and network access is permitted, run `python scripts/check_fudan_spec_update.py --reference references/fudan-2026-format-checklist.md` from this skill folder before high-stakes compliance work. If the script reports a newer official specification, warn the user and treat the local checklist as stale until updated.

At minimum, check:

- Cover/title page includes the current required fields, including CLC and UDC when required.
- Chinese and English names, especially for international students or foreign teachers, match official identity/passport records.
- Abstracts and keywords match language and word-count requirements in the current rule.
- Lists of figures and tables are present when applicable.
- The main text includes conclusions.
- References follow the applicable GB/T 7714 rule; GB/T 7714-2025 takes effect on 2026-07-01.
- Notes use the required placement.
- Secrecy-related theses follow Graduate School procedures; do not reuse old public cover samples.

## Handling Missing Information

If the user asks for drafting but has not supplied evidence, write a structured scaffold with `[待补充：...]` markers. For English output, use `[TBD: ...]`. Never fabricate data, citations, approvals, fee details, supervisor signatures, publication records, or compliance facts.

## Output Contract

For outline or chapter-structure tasks, return:

1. A proposed chapter tree.
2. The purpose and evidence type for each chapter.
3. Fudan/default or custom compliance notes relevant to the task.
4. Missing inputs needed before final drafting.

For revision tasks, return:

1. Revised text.
2. A short explanation of structural changes.
3. Claim-evidence risks or missing information.
4. Format/compliance reminders only when relevant.

For file-producing tasks, create or edit the actual LaTeX/DOCX/Markdown files, run available validation, and report what was checked. For LaTeX compile tasks, report the exact command, root `.tex`, engine, output directory, verified PDF path, whether the PDF is fresh, and any remaining fatal errors or warnings. For DOCX work, use an installed external document workflow rather than a repository-vendored DOCX module.

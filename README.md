# Fudan Graduate Thesis Skill

Upload thesis -> get compliance report. Topic -> chapter plan. Draft -> claim-evidence audit.

`fdu-final-paper-skill` is a Codex skill for Fudan master's and doctoral theses. It helps an agent turn messy thesis material into a defensible chapter plan, revise Chinese/English academic prose, check claim-evidence alignment, and audit the thesis against Fudan's 2026.06 thesis specification.

![Compliance report screenshot](assets/product-screenshot.svg)

## Why Use It

- **Topic -> chapter plan**: turn a research topic, methods, data, and degree type into a chapter tree with evidence requirements.
- **Draft -> claim-evidence audit**: catch inflated contribution claims, unsupported conclusions, inconsistent terminology, and missing figure/table interpretation.
- **Upload thesis -> compliance report**: check front matter, abstracts, figure/table lists, references, notes, conclusions, appendices, and defense-readiness risks.
- **LaTeX/BibTeX ready**: reuse the optional LaTeX helper bundle for compilation, citation checks, and issue-gated writing.
- **DOCX friendly without vendoring risk**: use your installed document/DOCX plugin or skill for Word editing; this repository does not redistribute unclear-license DOCX code.

## One-Minute Install

Clone this repository, then copy only the skill folder into Codex's skills directory.

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/fdu-final-paper-skill "${CODEX_HOME:-$HOME/.codex}/skills/"
```

PowerShell:

```powershell
$target = if ($env:CODEX_HOME) { "$env:CODEX_HOME\skills" } else { "$HOME\.codex\skills" }
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -Recurse -Force .\skills\fdu-final-paper-skill $target
```

Validate the checkout:

```bash
python scripts/quick_validate.py skills/fdu-final-paper-skill
python scripts/smoke_test.py
```

## Three-Minute Demo

Try these prompts after installing the skill:

```text
Use $fdu-final-paper-skill to design a master's thesis chapter plan.
Topic: 基于多源遥感数据的城市热岛效应时空演化研究
Degree: 学术型硕士
Evidence: Landsat 2013-2023, MODIS LST, POI density, administrative boundary data
Submission batch: 2026-09
```

```text
Use $fdu-final-paper-skill to revise this Chinese abstract and mark claim-evidence risks:
<paste abstract>
```

```text
Use $fdu-final-paper-skill to audit my thesis for Fudan 2026 compliance.
Input files: thesis.pdf, thesis.tex, ref.bib
```

Replay the scripted terminal flow in [`assets/demo.cast`](assets/demo.cast), or read the concrete outputs in [`examples/`](examples/).

## Example Output

```markdown
## Compliance Summary

Status: Needs revision before submission

High-risk items:
- Cover/title page: CLC and UDC fields are missing for the 2026.06 template.
- Chinese and English abstracts: method order is inconsistent with Chapter 3-5.
- References: GB/T 7714 transition must be confirmed for the 2026-09 batch.

Next actions:
1. Download the current official template from Fudan Graduate School.
2. Align abstract claims with verified Chapter 4 tables.
3. Rebuild the figure/table lists after final PDF generation.
```

More examples:

- [`examples/chapter-plan.md`](examples/chapter-plan.md)
- [`examples/abstract-revision.md`](examples/abstract-revision.md)
- [`examples/fudan-2026-compliance-report.md`](examples/fudan-2026-compliance-report.md)
- [`examples/docx-latex-workflow.md`](examples/docx-latex-workflow.md)

## Repository Layout

```text
.
├── skills/fdu-final-paper-skill/       # the installable Codex skill
├── examples/                           # concrete input/output examples
├── evals/                              # 10 realistic eval prompts
├── scripts/                            # repo validation helpers
├── embedded/latex-paper-skills/        # optional MIT-licensed LaTeX helper bundle
├── assets/                             # README screenshot and demo cast
└── .github/workflows/ci.yml            # validation and Fudan spec watch
```

## Fudan Specification Watch

The skill includes a snapshot of the current Fudan Graduate School thesis-spec page and a checker:

```bash
python skills/fdu-final-paper-skill/scripts/check_fudan_spec_update.py \
  --reference skills/fdu-final-paper-skill/references/fudan-2026-format-checklist.md
```

GitHub Actions runs a scheduled check so maintainers can notice when the official page changes.

## License

MIT for this repository's original content. See [`NOTICE`](NOTICE) for third-party material and attribution.

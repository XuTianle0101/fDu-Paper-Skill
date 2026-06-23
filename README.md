# Fudan Graduate Thesis Skill

English | [简体中文](README.zh-CN.md)

[![CI](https://github.com/XuTianle0101/fDu-Paper-Skill/actions/workflows/ci.yml/badge.svg)](https://github.com/XuTianle0101/fDu-Paper-Skill/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/github/license/XuTianle0101/fDu-Paper-Skill)](LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/XuTianle0101/fDu-Paper-Skill?label=latest%20release)](https://github.com/XuTianle0101/fDu-Paper-Skill/releases)
![Skill Version](https://img.shields.io/badge/skill-v0.1.2-0f766e)
![Python](https://img.shields.io/badge/python-3.8%20%7C%203.11-3776ab)
![Fudan Baseline](https://img.shields.io/badge/Fudan%20baseline-2026.06-b91c1c)
![Markdown Links](https://img.shields.io/badge/markdown%20links-passing-15803d)

Current skill version: `v0.1.2`. The canonical version source is [`skills/fdu-final-paper-skill/VERSION`](skills/fdu-final-paper-skill/VERSION); see [`CHANGELOG.md`](CHANGELOG.md) for release notes.

Upload thesis -> get compliance report. Topic -> chapter plan. Draft -> claim-evidence audit.

`fdu-final-paper-skill` is a Codex skill for Fudan master's and doctoral theses. It helps an agent turn messy thesis material into a defensible chapter plan, revise Chinese/English academic prose, check claim-evidence alignment, and audit the thesis against Fudan's 2026.06 thesis specification by default, while allowing newer or department-specific compliance links, files, folders, and templates to override or supplement that baseline.

| Start Here | What You Get |
| --- | --- |
| **Paper format compliance check** | A Fudan 2026.06 baseline report with missing front matter, abstract, reference, appendix, and defense-readiness risks. |
| **Abstract / introduction polish** | Academic Chinese/English revisions that separate verified contribution claims from claims that need evidence. |
| **LaTeX compile diagnosis** | `fduthesis`-aware checks for package conflicts, output directories, stale PDFs, and BibTeX/Biber handoff problems. |

Real input -> output diff:

```diff
Input: "本文首次提出城市热岛综合评估框架，并证明模型显著优于现有方法。"
- 本文首次提出城市热岛综合评估框架，并证明模型显著优于现有方法。
+ 本文构建了面向城市热岛时空演化的综合评估框架，并在 Landsat 2013-2023、MODIS LST 与 POI 密度数据上验证了其适用性。
+ [Evidence risk] "首次" and "显著优于" need prior-art comparison, statistical tests, or softer wording before submission.
```

![Compliance report screenshot](assets/product-screenshot.svg)

## Trust and Privacy Boundaries

This project is not an official Fudan University service, and its compliance reports are not official approval, review, or submission decisions. Always treat current Fudan Graduate School, department, program, library, and supervisor instructions as the final authority.

Thesis files can contain unpublished research, personal information, supervisor comments, ethics approvals, funding details, or confidential material. Do not upload confidential theses, sensitive personal data, unpublished datasets, or restricted review materials to models, services, plugins, or hosted agents that you do not trust or are not authorized to use.

## Why Use It

- **Topic -> chapter plan**: turn a research topic, methods, data, and degree type into a chapter tree with evidence requirements.
- **Draft -> claim-evidence audit**: catch inflated contribution claims, unsupported conclusions, inconsistent terminology, and missing figure/table interpretation.
- **Upload thesis -> compliance report**: check front matter, abstracts, figure/table lists, references, notes, conclusions, appendices, and defense-readiness risks against the default Fudan 2026.06 baseline or user-supplied compliance sources.
- **LaTeX/BibTeX ready**: run Fudan-friendly compile diagnostics for `fduthesis`, output directories, and PDF artifact verification; reuse the optional LaTeX helper bundle for broader paper workflows.
- **DOCX friendly without vendoring risk**: use your installed document/DOCX plugin or skill for Word editing; this repository does not redistribute unclear-license DOCX code.

## One-Minute Install

Start with an agent that supports skills, such as Codex or Claude Code.

Then choose one install path:

1. Use the agent's built-in skill installer if it has one. Give it this GitHub repository and ask it to install `fdu-final-paper-skill`.
2. Or install by hand: clone this repository, then copy only `skills/fdu-final-paper-skill` into the agent's local `skills` folder.

Bash/macOS/Linux:

```bash
git clone https://github.com/XuTianle0101/fDu-Paper-Skill.git
cd fDu-Paper-Skill
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/fdu-final-paper-skill "${CODEX_HOME:-$HOME/.codex}/skills/"
```

PowerShell/Windows:

```powershell
git clone https://github.com/XuTianle0101/fDu-Paper-Skill.git
cd fDu-Paper-Skill
$target = if ($env:CODEX_HOME) { "$env:CODEX_HOME\skills" } else { "$HOME\.codex\skills" }
New-Item -ItemType Directory -Force -Path $target | Out-Null
Copy-Item -Recurse -Force .\skills\fdu-final-paper-skill $target
```

Restart the agent after installing, then try a prompt like:

```text
Use $fdu-final-paper-skill to audit my thesis outline for Fudan 2026 compliance.
```

Optional checkout validation for maintainers:

```bash
python3 scripts/quick_validate.py skills/fdu-final-paper-skill
python3 scripts/smoke_test.py
```

Commands in this README use `python3`; if your environment exposes only `python`, replace `python3` with `python`.

## Updating an Installed Skill

Installed Codex skills are copied into the local skills directory, so users who installed an earlier version should update their repository checkout and reinstall the skill folder.

```bash
git pull

rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/fdu-final-paper-skill"
cp -R skills/fdu-final-paper-skill "${CODEX_HOME:-$HOME/.codex}/skills/"
```

PowerShell:

```powershell
git pull

$skills = if ($env:CODEX_HOME) { "$env:CODEX_HOME\skills" } else { "$HOME\.codex\skills" }
$dest = Join-Path $skills "fdu-final-paper-skill"

Remove-Item -Recurse -Force $dest -ErrorAction SilentlyContinue
Copy-Item -Recurse -Force .\skills\fdu-final-paper-skill $skills
```

Restart Codex after reinstalling so the updated skill is loaded.

If the repository was installed from GitHub and you already have a local checkout:

```bash
cd path/to/fdu-final-paper-skill
git pull
rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/fdu-final-paper-skill"
cp -R skills/fdu-final-paper-skill "${CODEX_HOME:-$HOME/.codex}/skills/"
```

## Release Notifications

Important changes are recorded in [`CHANGELOG.md`](CHANGELOG.md). Maintainers should publish GitHub tags and Releases for user-facing updates, for example `v0.1.0`, `v0.1.1`, and `v0.1.2`.

Users who want update notifications can open the GitHub repository, choose **Watch -> Custom -> Releases**, and GitHub will notify them when a new release is published.

## Reading Reference Files Safely

The installed skill includes a reader for Chinese/English PDFs, DOCX files, and text-like references:

```bash
python3 skills/fdu-final-paper-skill/scripts/read_reference_file.py "path/to/reference.pdf" \
  -o extracted-reference.md
```

If a Chinese path is garbled by the shell, pass it through an environment variable instead:

```powershell
$env:FDU_REF_FILE = "D:\论文资料\参考文献\中文论文.docx"
python3 skills\fdu-final-paper-skill\scripts\read_reference_file.py --path-env FDU_REF_FILE `
  -o extracted-reference.md
```

Use `--pages 1-5` for long PDFs, `--max-chars 0` for full extraction, and `--list-env` for multiple files.

PDF extraction needs at least one optional backend: `pypdf`/`PyPDF2`, `pdfplumber`, `PyMuPDF`, or the `pdftotext` command from Poppler. DOCX and text extraction use the Python standard library.

## Custom Compliance Sources

Fudan 2026.06 remains the default compliance and template reference. You can also give the skill newer Graduate School links, department notices, supervisor instructions, template files, or a folder of rule documents. The agent should read those sources, state which ones were used, and use Fudan 2026.06 only as the default baseline or fallback for missing items.

Example prompt:

```text
Use $fdu-final-paper-skill to audit my thesis.
Default baseline: Fudan 2026.06.
Additional compliance sources:
- Department notice: docs/department-2026-defense-rules.pdf
- Template folder: templates/fudan-school-template/
- Official link: https://example.edu/department/thesis-rules
```

For local rule folders, extract the source set first when needed:

```bash
python3 skills/fdu-final-paper-skill/scripts/read_reference_file.py \
  --glob "docs/compliance/**/*.pdf" \
  --glob "docs/compliance/**/*.docx" \
  --glob "docs/compliance/**/*.md" \
  -o extracted-compliance-sources.md
```

## Smoother LaTeX Compilation

For `fduthesis` projects, start with the bundled compiler helper instead of hand-rolling wrapper logic:

```bash
python3 skills/fdu-final-paper-skill/scripts/compile_latex_project.py \
  --project-dir path/to/thesis --main main.tex --engine auto
```

If the project uses a build directory:

```bash
python3 skills/fdu-final-paper-skill/scripts/compile_latex_project.py \
  --project-dir path/to/thesis --main main.tex --engine auto --output-dir build
```

The helper flags common `fduthesis`/`unicode-math` conflicts such as `amssymb`, prepares `\include` aux subdirectories under the output directory, and verifies the actual fresh PDF path before reporting success or failure.

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

Watch the scripted terminal flow as [`GIF`](assets/demo.gif), [`MP4`](assets/demo.mp4), or the source [`cast`](assets/demo.cast); concrete outputs live in [`examples/`](examples/).

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
├── skills/.../references/              # default Fudan checklist and source policy
├── assets/                             # README screenshot and demo media
└── .github/workflows/ci.yml            # validation and Fudan spec watch
```

## Fudan Specification Watch

The skill includes a snapshot of the default Fudan Graduate School thesis-spec page and a checker:

```bash
python3 skills/fdu-final-paper-skill/scripts/check_fudan_spec_update.py \
  --reference skills/fdu-final-paper-skill/references/fudan-2026-format-checklist.md
```

GitHub Actions runs a scheduled check so maintainers can notice when the default official page changes. Custom department links or user-supplied files are evaluated during the user's audit task, not by the scheduled watcher.

## License

MIT for this repository's original content. See [`NOTICE`](NOTICE) for third-party material and attribution.

## Star History

<a href="https://www.star-history.com/?repos=XuTianle0101%2FfDu-Paper-Skill&type=date&legend=top-left">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=XuTianle0101/fDu-Paper-Skill&type=date&theme=dark&legend=top-left" />
    <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=XuTianle0101/fDu-Paper-Skill&type=date&legend=top-left" />
    <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=XuTianle0101/fDu-Paper-Skill&type=date&legend=top-left" />
  </picture>
</a>

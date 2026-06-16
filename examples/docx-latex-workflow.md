# Example: DOCX/LaTeX Workflow

## Prompt

```text
Use $fdu-final-paper-skill to prepare a revision workflow for my thesis.
Current files: thesis.docx, thesis.tex, ref.bib
Goal: produce tracked Word revision notes and a clean LaTeX/PDF validation checklist.
```

## Recommended Workflow

1. Extract thesis inventory.
   - DOCX path: use the active document/DOCX capability in the current Codex environment.
   - LaTeX path: inspect `thesis.tex`, included files, figures, tables, and `ref.bib`.
2. Build a thesis story chain.
   - `problem -> gap -> objective -> method/material -> evidence -> findings -> contribution -> limitation`
3. Produce a change plan before editing.
   - Separate wording edits, structural edits, evidence gaps, and compliance fixes.
4. Edit DOCX with tracked changes only if a DOCX-capable skill/plugin is installed.
   - If not installed, generate a Markdown revision memo with paragraph-level replacement text.
5. Run LaTeX checks.
   - Prefer `python scripts/compile_latex_project.py --project-dir . --main thesis.tex --engine auto` when the Fudan skill scripts are available.
   - If using `--output-dir build`, verify that `\include` aux subdirectories are prepared and that the PDF is checked at the actual output path.
   - For `fduthesis`/`unicode-math`, remove duplicate legacy math packages such as `amssymb` or `amsfonts` before retrying compilation.
   - Check citation keys in `thesis.tex` against `ref.bib`.
   - Confirm figure/table numbering after compilation.
6. Produce final reports.
   - `claim-evidence-audit.md`
   - `fudan-2026-compliance-report.md`
   - `revision-log.md`

## Output Contract

- Keep final claims bounded by supplied evidence.
- Do not fabricate results, citations, approvals, signatures, publication records, or department rules.
- For Fudan compliance, always cite the official Graduate School page as the authority and mark unknowns for department confirmation.
